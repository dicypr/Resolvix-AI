from __future__ import annotations

import asyncio
from datetime import datetime, timezone
import json
import pytest
import respx
import httpx
from fastapi import HTTPException
from fastapi.testclient import TestClient

from resolvix_contracts.models import (
    CallChannel,
    CallContext,
    CallOutcome,
    CreateTicketAction,
    Priority,
    SendSmsAction,
    TicketCreate,
    TicketType,
    TransferAction,
)
from resolvix_runtime.agora_control import AgoraController
from resolvix_runtime.agora_token import generate_rtc_token, RtcTokenBuilder
from resolvix_runtime.app import create_app
from resolvix_runtime.config import RuntimeSettings
from resolvix_runtime.executor import ActionExecutor
from resolvix_runtime.ops_client import OpsClient
from resolvix_runtime.sessions import SessionState, get_session_registry
from resolvix_runtime.telephony.mock import MockTelephony


# --- A-6: AccessToken2 Verification ---


def test_agora_token_builder_access_token_2():
    # Valid 32-char hex UUIDs
    app_id = "970ca35de60c4464bb03a650e680fb9d"
    app_cert = "5cfd2fd1755d40ecb729f39468aa3dbb"
    channel = "resolvix-channel-01"
    uid = 123456

    token = generate_rtc_token(app_id, app_cert, channel, uid)
    assert token.startswith("007"), f"Expected token to start with 007, got {token[:5]}"
    assert len(token) > 100

    # Agent uid token
    agent_token = generate_rtc_token(app_id, app_cert, channel, 1000)
    assert agent_token.startswith("007")

    # Missing cert returns mock token fallback
    mock_token = generate_rtc_token(app_id, "", channel, uid)
    assert mock_token == f"mock-token-{channel}-{uid}"


# --- A-7 & A-8: Join Payload Shape, Languages, Voices, Managed Mode ---


@pytest.mark.asyncio
async def test_agora_agent_join_payload_shape_and_voices():
    app_id = "970ca35de60c4464bb03a650e680fb9d"
    app_cert = "5cfd2fd1755d40ecb729f39468aa3dbb"

    settings = RuntimeSettings(
        port=8000,
        agora_app_id=app_id,
        agora_app_certificate=app_cert,
        agora_customer_id="cust-123",
        agora_customer_secret="secret-456",
        asr_vendor="deepgram",
        asr_api_key="dg-key-789",
        asr_language="multi",
        asr_model="nova-3",
        asr_credential_mode="byok",
        tts_vendor="elevenlabs",
        tts_api_key="el-key-999",
        tts_model="eleven_flash_v2_5",
        tts_voice_id="pNInz6obpgDQGcFmaJgB",
        tts_credential_mode="byok",
    )

    ops_client = OpsClient(settings)
    controller = AgoraController(settings, ops_client)

    captured_payloads = []

    async with respx.mock(base_url="https://api.agora.io", assert_all_called=False) as agora_mock:
        join_route = agora_mock.post(f"/api/conversational-ai-agent/v2/projects/{app_id}/join").mock(
            side_effect=lambda req: captured_payloads.append(json.loads(req.content))
            or respx.MockResponse(200, json={"agent_id": "agent-xyz-987", "status": "RUNNING"})
        )

        agent_id = await controller._start_agora_agent(
            channel="test-channel-99",
            call_id="call-web-abc",
            llm_url="https://resolvix.example.com/v1/chat/completions?call_id=call-web-abc",
            greeting="Namaste, main Resolvix AI hoon.",
            user_uid=555666,
        )

        assert agent_id == "agent-xyz-987"
        assert len(captured_payloads) == 1
        p = captured_payloads[0]

        # Check A-7: proper properties wrapper shape
        assert p["name"] == "resolvix-agent-call-web-abc"
        props = p["properties"]
        assert props["channel"] == "test-channel-99"
        assert props["token"].startswith("007")
        assert props["agent_rtc_uid"] == "1000"
        assert props["remote_rtc_uids"] == ["555666"]

        # Check A-8: Deepgram Nova-3 + language multi
        asr = props["asr"]
        assert asr["vendor"] == "deepgram"
        assert asr["params"]["language"] == "multi"
        assert asr["params"]["model"] == "nova-3"
        assert asr["params"]["key"] == "dg-key-789"

        # Check A-8: ElevenLabs flash v2.5 + real voice id
        tts = props["tts"]
        assert tts["vendor"] == "elevenlabs"
        assert tts["params"]["model_id"] == "eleven_flash_v2_5"
        assert tts["params"]["voice_id"] == "pNInz6obpgDQGcFmaJgB"
        assert tts["params"]["key"] == "el-key-999"


@pytest.mark.asyncio
async def test_agora_agent_managed_mode():
    app_id = "970ca35de60c4464bb03a650e680fb9d"
    app_cert = "5cfd2fd1755d40ecb729f39468aa3dbb"

    settings = RuntimeSettings(
        port=8000,
        agora_app_id=app_id,
        agora_app_certificate=app_cert,
        agora_customer_id="cust-123",
        agora_customer_secret="secret-456",
        asr_credential_mode="managed",
        tts_credential_mode="managed",
    )

    ops_client = OpsClient(settings)
    controller = AgoraController(settings, ops_client)

    captured_payloads = []

    async with respx.mock(base_url="https://api.agora.io", assert_all_called=False) as agora_mock:
        agora_mock.post(f"/api/conversational-ai-agent/v2/projects/{app_id}/join").mock(
            side_effect=lambda req: captured_payloads.append(json.loads(req.content))
            or respx.MockResponse(200, json={"agent_id": "agent-managed-01", "status": "RUNNING"})
        )

        await controller._start_agora_agent(
            channel="test-channel-managed",
            call_id="call-web-managed",
            llm_url="https://resolvix.example.com/v1/chat/completions",
            greeting="Hello",
            user_uid=112233,
        )

        props = captured_payloads[0]["properties"]
        assert props["asr"]["credential_mode"] == "managed"
        assert "key" not in props["asr"]["params"]
        assert props["tts"]["credential_mode"] == "managed"
        assert "key" not in props["tts"]["params"]


# --- A-9: Agent Join Failure Handling (Error instead of warning) ---


@pytest.mark.asyncio
async def test_agora_agent_join_failure_raises_502_and_closes_ops_call():
    app_id = "970ca35de60c4464bb03a650e680fb9d"
    app_cert = "5cfd2fd1755d40ecb729f39468aa3dbb"

    settings = RuntimeSettings(
        port=8000,
        ops_api_url="http://localhost:8100",
        service_key="test-key",
        agora_app_id=app_id,
        agora_app_certificate=app_cert,
        agora_customer_id="cust-123",
        agora_customer_secret="secret-456",
    )

    ops_client = OpsClient(settings)
    controller = AgoraController(settings, ops_client)

    closed_calls = []

    async with respx.mock(assert_all_called=False) as mock:
        # Agora returns 400 Bad Request
        mock.post(f"https://api.agora.io/api/conversational-ai-agent/v2/projects/{app_id}/join").mock(
            return_value=respx.MockResponse(400, json={"message": "Invalid token or UID", "code": 40001})
        )

        # Ops API records call end
        mock.post(url__regex=r"http://localhost:8100/v1/calls/.+/end").mock(
            side_effect=lambda req: closed_calls.append(json.loads(req.content))
            or respx.MockResponse(200, json={"status": "ended"})
        )

        with pytest.raises(HTTPException) as exc_info:
            await controller._start_agora_agent(
                channel="fail-channel",
                call_id="call-fail-001",
                llm_url="https://resolvix.example.com",
                greeting="Hello",
                user_uid=999,
            )

        assert exc_info.value.status_code == 502
        detail = exc_info.value.detail
        assert detail["error"]["code"] == "agent_join_failed"
        assert "400" in detail["error"]["message"]

        # Assert ops call end was posted
        assert len(closed_calls) == 1
        assert closed_calls[0]["outcome"] == "failed"


# --- Web Session End & Agent Leave API ---


@pytest.mark.asyncio
async def test_agora_agent_leave_on_session_end():
    app_id = "970ca35de60c4464bb03a650e680fb9d"
    app_cert = "5cfd2fd1755d40ecb729f39468aa3dbb"

    settings = RuntimeSettings(
        port=8000,
        ops_api_url="http://localhost:8100",
        service_key="test-key",
        agora_app_id=app_id,
        agora_app_certificate=app_cert,
        agora_customer_id="cust-123",
        agora_customer_secret="secret-456",
    )

    leave_called = []

    async with respx.mock(assert_all_called=False) as mock:
        mock.post(f"https://api.agora.io/api/conversational-ai-agent/v2/projects/{app_id}/join").mock(
            return_value=respx.MockResponse(200, json={"agent_id": "agent-live-01", "status": "RUNNING"})
        )
        mock.post("http://localhost:8100/v1/calls").mock(
            return_value=respx.MockResponse(201, json={"status": "created"})
        )
        mock.post(url__regex=r"http://localhost:8100/v1/calls/.+/end").mock(
            return_value=respx.MockResponse(200, json={"status": "ended"})
        )
        mock.post(f"https://api.agora.io/api/conversational-ai-agent/v2/projects/{app_id}/agents/agent-live-01/leave").mock(
            side_effect=lambda req: leave_called.append(True) or respx.MockResponse(200, json={"status": "ok"})
        )

        app = create_app(settings)
        client = TestClient(app)

        # 1. Start web session
        resp_start = client.post("/api/sessions/web")
        assert resp_start.status_code == 200
        data = resp_start.json()
        call_id = data["call_id"]
        assert data["agent_id"] == "agent-live-01"

        # 2. End web session
        resp_end = client.post("/api/sessions/web/end", json={"call_id": call_id})
        assert resp_end.status_code == 200
        assert resp_end.json()["status"] == "ended"

        # Verify Agora leave API was invoked
        assert len(leave_called) == 1


# --- Emergency Path: SMS is Non-Blocking for Transfers ---


@pytest.mark.asyncio
async def test_emergency_path_does_not_wait_for_sms_to_transfer():
    settings = RuntimeSettings(
        port=8000,
        ops_api_url="http://localhost:8100",
        service_key="test-key",
    )
    ops_client = OpsClient(settings)
    telephony = MockTelephony(transfer_success=True)
    session = SessionState(call_id="call-emerg-001", channel=CallChannel.pstn)
    executor = ActionExecutor(ops_client, telephony, settings, session)

    events_order: list[str] = []

    async with respx.mock(base_url="http://localhost:8100", assert_all_called=False) as mock:
        mock.post("/v1/tickets").mock(
            return_value=respx.MockResponse(201, json={"ticket_id": "EM-1001", "created": True})
        )
        mock.post(url__regex=r"/v1/tickets/.+/events").mock(
            return_value=respx.MockResponse(201, json={"status": "stored"})
        )

        # SMS endpoint has an artificial delay simulating Twilio/DLT network roundtrip
        async def slow_sms(request):
            events_order.append("sms_started")
            await asyncio.sleep(0.1)
            events_order.append("sms_finished")
            return respx.MockResponse(202, json={"message_id": "sms-delayed", "status": "sent", "mode": "mock"})

        mock.post("/v1/notifications/sms").mock(side_effect=slow_sms)

        # 1. Create emergency ticket
        create_act = CreateTicketAction(
            ticket=TicketCreate(
                idempotency_key="em-k",
                call_id="call-emerg-001",
                type=TicketType.EMERGENCY,
                priority=Priority.P1,
                priority_reason="medical",
                department="emergency",
                summary="Student fainted",
                collected_fields={},
                caller_number="+919000000001",
                callback_number=None,
                callback_requested=False,
                transcript_excerpt="help",
                brief="Emergency",
            )
        )
        await executor.execute(create_act, blocking=True)
        assert session.emergency is True
        assert executor.ticket_id == "EM-1001"

        # 2. Dispatch SMS with blocking=False (as emitted by safety fixture)
        sms_act = SendSmsAction(
            idempotency_key="sms-k",
            to_number="+919999999999",
            template_id="staff_alert",
            vars={"ticket_id": "{{ticket_id}}"},
            consent="staff",
        )
        await executor.execute(sms_act, blocking=False)

        # 3. Transfer immediately executes
        transfer_act = TransferAction(
            department="emergency",
            to_number="+910000000900",
            reason="medical",
            brief="Emergency",
            requires_ticket=True,
        )
        events_order.append("transfer_started")
        await executor.execute(transfer_act, blocking=True)
        events_order.append("transfer_finished")

        # Transfer must have finished while slow SMS was still running in background!
        assert "transfer_started" in events_order
        assert "transfer_finished" in events_order
        assert "sms_finished" not in events_order  # Proof transfer did not block on SMS!

        # Cleanup pending tasks - now SMS completes
        await executor.wait_pending()
        assert "sms_finished" in events_order
