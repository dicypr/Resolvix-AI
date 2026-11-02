# Resolvix AKGEC Cache-Augmented Knowledge Base (CAG)

This knowledge base is curated from the AKGEC website dataset for **Cache-Augmented Generation (CAG)** in Resolvix-AI.

## Key Metrics
- **Compiled KB Version:** `50a2239aa2ee`
- **Total Entries:** `57` approved entries
- **FAQ Semantic Cache:** `29` entries (121 question variants indexed)
- **Token Count:** `8334` tokens (Well within the 90,000 token budget)
- **Zero-Retrieval Latency:** Prompt prefix is cached by Groq (`cached_tokens > 0`), providing instant sub-300ms speech synthesis.

## Departments Covered
| Department | Key | Prefix | Entry Count | Topics |
|------------|-----|--------|-------------|--------|
| Helpdesk / General | `helpdesk` | `GEN` | 20 | College history, courses, intake, timings, director, accreditation, library, Wi-Fi, CoEs, sports, clubs |
| Admissions | `admissions` | `ADM` | 8 | B.Tech, MCA, M.Tech eligibility, UPTAC counselling, JEE rank scholarships, lateral entry |
| Accounts / Fees | `accounts` | `FEE` | 9 | Payment modes, caution money refund, late fees, insurance cover, receipts, fee fixation |
| Examination Cell | `exam_cell` | `EXM` | 7 | End-sem schedule, sessionals, PUT, admit cards, seating plans, re-evaluation, back papers |
| Hostel Office | `hostel` | `HST` | 8 | 6 hostels, Junior Boys, Girls hostels, mess timings, gate timings (10/11 PM), solar water, room change |
| Transport | `transport` | `TRN` | 3 | Bus routes (Delhi, Noida, Ghaziabad, Meerut), bus pass, morning/evening timings |
| Emergency On-Call | `emergency` | `EMG` | 2 | 24x7 ambulance, Dr. R.S.G. Hospital tie-up, security control room, 112 |

## Files
- `cag_kb.jsonl`: Raw JSONL entries conforming to `resolvix_contracts.models.KBEntry`.
- `cag_kb_export.json`: Export schema conforming to `resolvix_contracts.models.KBExport`.
- `cag_kb.csv`: Tabular spreadsheet format for human review and ops dashboard import.
- `cag_prompt_prefix.txt`: Byte-identical rendered prefix for Groq prompt cache.
