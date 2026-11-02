"""The shared fixtures for the parallel agents behave as documented."""
from datetime import datetime, timezone


def test_clients_and_roles(service_client, admin_client, staff_client, anon_client):
    assert service_client.get("/v1/tickets").status_code == 200
    assert anon_client.get("/v1/tickets").status_code == 401
    assert admin_client.get("/v1/auth/me").json()["role"] == "admin"
    me = staff_client.get("/v1/auth/me").json()
    assert (me["role"], me["department"]) == ("staff", "exam_cell")


def test_clock_freezes_ist_date_across_utc_midnight(ops_app, freeze_clock):
    freeze_clock(datetime(2026, 10, 30, 20, 0, tzinfo=timezone.utc))  # 01:30 IST on the 31st
    assert ops_app.state.clock.today_ist().isoformat() == "2026-10-31"
    freeze_clock(datetime(2026, 10, 31, 18, 29, tzinfo=timezone.utc))  # 23:59 IST still the 31st
    assert ops_app.state.clock.today_ist().isoformat() == "2026-10-31"


def test_default_clock_is_real(ops_app):
    assert ops_app.state.clock.today_ist().year >= 2026


def test_app_factory_overrides(app_factory):
    app = app_factory(notify_async=True)
    assert app.state.settings.sms_async is True


def test_fresh_clone_without_a_data_folder_starts(tmp_path):
    from resolvix_ops.app import create_app
    from resolvix_ops.config import Settings
    db = tmp_path / "missing" / "nested" / "x.db"
    app = create_app(Settings(_env_file=None, database_url=f"sqlite:///{db.as_posix()}", service_key="k" * 20,
                              session_secret="s" * 32, seed_users_on_startup=False, sms_poll_enabled=False))
    app.state.engine.dispose()
    assert db.exists()
