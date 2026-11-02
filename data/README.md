# Resolvix AKGEC Dataset & Knowledge Base

This directory contains the AKGEC chatbot dataset and the compiled **Cache-Augmented Generation (CAG)** Knowledge Base for Resolvix.

## Overview

Resolvix uses **Cache-Augmented Generation (CAG)** instead of traditional chunked vector RAG. All verified college knowledge is compiled into a deterministic system prompt prefix that is cached by Groq (`cached_tokens > 0`). This eliminates runtime vector database retrieval latency and provides instant (<300ms) factual answers.

Additionally, high-frequency query variants are indexed in an in-memory **FAQ Semantic Cache** for immediate sub-15ms answers without calling the LLM.

---

## Directory Structure

```
data/
├── README.md                          # This file
├── knowledge_base/                    # Production Cache-Augmented Knowledge Base
│   ├── README.md                      # KB documentation and token metrics
│   ├── cag_kb.jsonl                   # 57 approved entries conforming to KBEntry schema
│   ├── cag_kb_export.json             # KBExport format (version 50a2239aa2ee)
│   ├── cag_kb.csv                     # Tabular spreadsheet format for human review
│   └── cag_prompt_prefix.txt          # Rendered Groq system prompt prefix
├── raw/                               # Web scraped raw files and notebooks
│   ├── akg_data.csv                   # Web crawled page content chunks (CSV)
│   ├── akgec_markdown.csv             # Markdown-formatted crawl data (CSV)
│   ├── raw_data.txt                   # Unprocessed text scrape
│   ├── fit_data.txt                   # Structured markdown text extracts
│   ├── akg_links.txt                  # Full list of crawled URLs
│   ├── Eda.ipynb                      # Exploratory data analysis notebook
│   ├── Upload_data.ipynb              # Vector upload pipeline notebook
│   ├── markdown-csv.py                # HTML to markdown converter
│   └── web-markdown.py                # Web scraper to markdown utility
├── json_data/                         # Structured JSON datasets
│   ├── structured_rag_data_v8.json    # 843 categorised chunks with metadata
│   ├── rag_cleaned_combined.json      # 1,344 clean chunks with source URLs
│   ├── rag_cleaned_1.json             # Full 3,305 chunk deep corpus
│   └── indexing_data.py               # Pinecone indexing script
├── rag_app/                           # Original RAG FastAPI service
│   ├── fast_api.py                    # Query API endpoint
│   ├── model_rag.py                   # Retrieval and completion logic
│   ├── schema.py                      # Request/response schemas
│   ├── render.yaml                    # Deployment specification
│   ├── requirements.txt               # App dependencies
│   ├── README.md                      # Service documentation
│   └── .env.example                   # Environment configuration template
├── previous_work/                     # Legacy prototypes
│   ├── app.py                         # Streamlit / Flask prototype
│   ├── app-2.py                       # Alternate UI prototype
│   ├── cli.py                         # CLI query interface
│   └── requirements.txt               # Legacy dependencies
└── public/                            # Static frontend assets
    ├── AKGEC_icon.png                 # College crest icon
    ├── index.html                     # Web UI markup
    ├── script.js                      # Chatbot frontend logic
    └── styles.css                     # Responsive UI styling
```

---

## Knowledge Base Summary (CAG)

- **Total Approved Entries:** 57 entries
- **Compiled KB Version:** `50a2239aa2ee`
- **Total Prefix Tokens:** 8,334 / 90,000 budget
- **FAQ Semantic Cache Items:** 29 entries (121 question variants indexed)
- **Departments Covered:**
  - `helpdesk` (GEN): 20 entries (Campus history, programs, intake, timings, leadership, library, Wi-Fi, CoEs, sports, clubs, safety)
  - `admissions` (ADM): 8 entries (B.Tech, MCA, M.Tech eligibility, UPTAC counselling, JEE rank scholarships, lateral entry)
  - `accounts` (FEE): 9 entries (ERP payment, DD instructions, counselling fee adjustment, caution money refund, late fees, insurance)
  - `exam_cell` (EXM): 7 entries (End-sem schedule, sessionals, PUT, admit cards, seating plans, challenge evaluation, back papers)
  - `hostel` (HST): 8 entries (6 campus hostels, Junior Boys, Girls hostels, mess timings, gate closing 10/11 PM, solar water, outpass)
  - `transport` (TRN): 3 entries (Bus routes across Delhi/NCR, bus pass procedure, morning/evening timings)
  - `emergency` (EMG): 2 entries (24x7 ambulance, Dr. R.S.G. Hospital tie-up, security control room, 112)

---

## How to Use with Resolvix Brain

Set `KB_SOURCE` in your environment or `.env`:

```bash
# Load directly from the CAG knowledge base
KB_SOURCE="file:data/knowledge_base/cag_kb.jsonl"
```

Compile and test:

```bash
python -m resolvix_brain compile --source data/knowledge_base/cag_kb.jsonl
```
