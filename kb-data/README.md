# Resolvix-AI Knowledge Base Data (`kb-data`)

This directory contains the verified, official knowledge base deliverables for **Resolvix-AI**, audited and aligned against Member C's provenance audit (`VERIFY_WITH_A.md`).

## Summary of Changes
- **Original Entries:** 57
- **Dropped Unverified Entries (6):** `HST-104` (Gate time), `HST-105` (Mess timings), `HST-107` (Room change Form H-4), `HST-108` (Outpass leave portal), `TRN-103` (Bus departure 5:10 PM), `FEE-104` (Late fee fine Rs 100/day).
- **Verified / Corrected Entries (25):** Citations updated with official URLs from `https://www.akgec.ac.in` and `https://erp.aktu.ac.in/`; text strictly aligned with crawled pages (discrepancies removed).
- **Active Deliverable Entries:** 51
- **Expanded / Scraped 74-entry dataset:** Preserved on dedicated branch `data-scraped`.

## Deliverable Files
1. **`akgec_kb_100series.jsonl`**: Primary JSONL file for Ops dashboard import (`status: "draft"`).
2. **`VERIFY_WITH_A.md`**: Item-by-item resolution report addressing Member C's 24 unverified + 7 discrepancy items.
3. **`cag_kb.jsonl`**: CAG reference file (`status: "approved"`).
4. **`cag_kb_export.json`**: Standard `KBExport` schema artifact.
5. **`cag_kb.csv`**: Review spreadsheet.
6. **`cag_prompt_prefix.txt`**: Deterministically compiled prefix (`version: 81298e89645f`, 9,256 tokens).
