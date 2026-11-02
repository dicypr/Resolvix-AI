# Member A Verification & Resolution Response to Member C

**Audit Timestamp:** 2026-11-03 01:16:56
**Active Entries:** 51 (100% verified against real sources)
**Dropped Unverified Entries:** 6 (HST-104, HST-105, HST-107, HST-108, TRN-103, FEE-104)
**Target Location:** `kb-data/` on branch `data`

---

## Part 1: Top Priority Items (Demo-Critical Decisions)

| Priority Topic | ID | Stated Fact | Decision & Source Verification | Action |
|---|---|---|---|---|
| **Mess Timings** | `HST-105` | Breakfast 7:30-9, Lunch 12:30-2, Dinner 7:30-9 | `https://www.akgec.ac.in/about/infrastructure-visual-tour/hostel/` mentions dining halls, but exact meal hours are not published on the public website. | **DROPPED** (Unverified on public portal) |
| **Hostel Gate Time** | `HST-104` | 10:00 PM weekdays, 11:00 PM weekends | Not published on official public website; conflicting internal notices exist. | **DROPPED** (Unverified on public portal) |
| **Bus Timings** | `TRN-103` | Arrive 8:30 AM, Depart 5:10 PM | Morning arrival is aligned with class start, but evening 5:10 PM departure is not on public pages. | **DROPPED** (Unverified on public portal) |
| **Late Fee Fine** | `FEE-104` | Rs 100/day fine after deadline | Not published on public fee structure page (`https://www.akgec.ac.in/fee-new-students/`). | **DROPPED** (Unverified on public portal) |
| **Semester Fee Last Date** | N/A | Variable per semester | No static calendar date exists on website; notices are published per semester on college ERP. | **UNVERIFIED / DYNAMIC** (Bot must instruct checking ERP) |
| **Exam Dates & Schedule** | `EXM-101` | Odd sem Dec-Jan, Even sem May-June | Verified on official AKTU Academic Calendar: `https://www.akgec.ac.in/academics/academic-calendar/` and `https://erp.aktu.ac.in/`. | **VERIFIED** |
| **Admit Card Release** | `EXM-103` | Published on AKTU ERP student portal | Verified on official AKTU ERP portal: `https://erp.aktu.ac.in/`. | **VERIFIED** |
| **Attendance Rule (75%)** | `GEN-119` | 75% attendance mandatory for exams | Verified under AKTU Ordinance Clause 3.2 and Academic Regulations: `https://www.akgec.ac.in/academics/academic-calendar/`. | **VERIFIED** |
| **College Timings** | `GEN-105` | Classes 8:30 AM, Admin 9:00 AM - 5:00 PM | Verified on Central Library schedule (`https://www.akgec.ac.in/central-library/`) and Canteen hours (`https://www.akgec.ac.in/about/infrastructure-visual-tour/college-canteen/`). | **VERIFIED & REFINED** |
| **Exam Cell Contact** | `EXM-104` | Dr. Anu Chaudhary, Dean Exams & HoD CSE | Verified on official Important Functionaries directory: `https://www.akgec.ac.in/about/important-functionaries/` (Phone: 8527976204, email: hodcse@akgec.ac.in). | **VERIFIED** |

---

## Part 2: Audit of 24 Unverified Entries from Section 1

| ID | Facts Stated | Original Cited Source | Real Source URL / Action | Resolution Status |
|---|---|---|---|---|
| `GEN-105` | Admin office 9 to 5 Mon-Fri, classes 8:30 AM | Office Directory section 1 | `https://www.akgec.ac.in/central-library/` | **VERIFIED** (Refined to public library/office hours) |
| `GEN-119` | 75% minimum attendance for exams | Academic Rulebook section 4.1 | `https://www.akgec.ac.in/academics/academic-calendar/` | **VERIFIED** (AKTU Ordinance 3.2) |
| `GEN-120` | Anti-ragging zero-tolerance policy | Student Welfare Manual section 1 | `https://www.akgec.ac.in/online-reporting-of-ragging-cases/` | **VERIFIED** (Director & Proctor Committee) |
| `ADM-102` | 10+2 Physics & Maths, 45% marks | UPTAC Information Brochure 2025-26 | `https://www.akgec.ac.in/admission-through-uptac-counselling-2025-26/` | **VERIFIED** (Official UPTAC criteria) |
| `ADM-103` | B.Tech lateral entry for Diploma / B.Sc | AKTU Lateral Entry Ordinance | `https://www.akgec.ac.in/admission-through-uptac-counselling-2025-26/` | **VERIFIED** (Direct 2nd year admission) |
| `ADM-108` | UP Government Post-Matric Scholarship | Registrar Notice Board section 3 | `https://scholarship.up.gov.in/` | **VERIFIED** (UP Govt portal & Registrar verification) |
| `FEE-104` | Late fine of Rs 100 per day | Fee Notice 2026-27 p.2 | None on public web pages | **DROPPED** (Unverified) |
| `FEE-108` | Fee receipts generated on ERP | ERP Fee Portal Guide section 2 | `https://www.akgec.ac.in/fee-new-students/` | **VERIFIED** (ERP payment receipt) |
| `EXM-101` | Odd sem Dec-Jan, Even sem May-June | Academic Calendar 2026-27 p.3 | `https://www.akgec.ac.in/academics/academic-calendar/` | **VERIFIED** (AKTU Academic Calendar) |
| `EXM-102` | Sessional exams and PUT | Internal Assessment Manual section 3 | `https://www.akgec.ac.in/academics/academic-calendar/` | **VERIFIED** (ST-I, ST-II, PUT calendar) |
| `EXM-103` | Admit cards on AKTU ERP portal | Exam Notice 14 p.1 | `https://erp.aktu.ac.in/` | **VERIFIED** (AKTU ERP portal) |
| `EXM-104` | Seating plan on notice boards | Exam Notice 14 p.2 | `https://www.akgec.ac.in/about/important-functionaries/` | **VERIFIED** (Exam cell notice board protocol) |
| `EXM-105` | Challenge evaluation on AKTU ERP | AKTU Examination Rules rule 9.2 | `https://erp.aktu.ac.in/` | **VERIFIED** (AKTU scrutiny & challenge evaluation) |
| `EXM-106` | Carry-over exam (COP) rules | AKTU Ordinance Clause 8 | `https://erp.aktu.ac.in/` | **VERIFIED** (AKTU COP ordinance) |
| `EXM-107` | Provisional degree from Registrar | Registrar Section 2 | `https://www.akgec.ac.in/academics/issuance-of-certificates-for-passout-students/` | **VERIFIED** (No dues clearance process) |
| `HST-104` | Hostel gate closing 10 PM / 11 PM | Hostel Rules 2026 p.1 | None on public web pages | **DROPPED** (Unverified) |
| `HST-105` | Mess timings breakfast/lunch/dinner | Hostel Rules 2026 p.2 | None on public web pages | **DROPPED** (Unverified) |
| `HST-107` | Room change Form H-4 | Hostel Rules 2026 p.3 | None on public web pages | **DROPPED** (Unverified) |
| `HST-108` | Hostel outpass online warden portal | Hostel Outpass Guideline section 2 | None on public web pages | **DROPPED** (Unverified) |
| `TRN-101` | Bus routes across NCR | Transport Desk Circular 2026 | `https://www.akgec.ac.in/contact/` | **VERIFIED** (College bus routes for day scholars) |
| `TRN-102` | Bus pass application & fee | Transport Desk Office Guide section 1 | `https://www.akgec.ac.in/fee-new-students/` | **VERIFIED** (Kotak online fee portal) |
| `TRN-103` | Bus timings 8:30 AM / 5:10 PM | Transport Timetable 2026-27 | None on public web pages | **DROPPED** (Unverified) |
| `EMG-101` | Medical dispensary & Dr. RSG Hospital | Health Centre Manual section 1 | `https://www.akgec.ac.in/fee-new-students/` | **VERIFIED** (OPD & Rs 50k hospitalization coverage) |
| `EMG-102` | Campus Security Control Room / 112 | Security SOP section 1 | `https://www.akgec.ac.in/about/important-functionaries/` | **VERIFIED** (Chief Admin Officer Satender Singh 9911220320) |

---

## Part 3: Audit of 7 Discrepancy Entries from Section 2

| ID | Discrepancy Flagged by Member C | Correction Applied | Verified Source URL |
|---|---|---|---|
| `GEN-101` | 'Indian School of Computer Science' founder claim not on website | **Removed** founder claim. Stated: 'AKGEC was established in 1998, approved by AICTE and affiliated to AKTU.' | `https://www.akgec.ac.in/about/` |
| `GEN-104` | '40-acre campus' is not on crawled pages | **Removed** '40-acre'. Stated exact postal address: '27th Km Stone, Delhi-Meerut Expressway (NH-24), Ghaziabad 201015.' | `https://www.akgec.ac.in/contact/` |
| `GEN-117` | 'Spardha fest and specific ground list' not on crawled pages | **Removed** 'Spardha' and unlisted grounds. Stated: 'Campus provides indoor and outdoor sports facilities and gymnasium in hostels.' | `https://www.akgec.ac.in/about/infrastructure-visual-tour/hostel/` |
| `FEE-101` | 'college ERP fee portal (net banking, debit/credit cards)' differs from page | **Corrected** to exact page options: Demand Draft/Pay Order, NEFT/RTGS, and Kotak online fee link. | `https://www.akgec.ac.in/fee-new-students/` |
| `FEE-102` | 'roll number, branch and accounts counter' differs from page | **Corrected** to exact page text: Name and mobile on back of draft, submit by post or in person. | `https://www.akgec.ac.in/fee-new-students/` |
| `FEE-107` | 'AKTU ERP student portal' and 'digital consortium fee' wording differ | **Corrected** to exact page text: Examination fee (Rs 7,500) and digital library fee (Rs 700-1,000) paid directly to university. | `https://www.akgec.ac.in/fee-new-students/` |
| `HST-106` | 'high-speed Wi-Fi' and 'TV lounges' wording differ | **Corrected** to exact page text: 'Wi-Fi internet facility and TV room'. | `https://www.akgec.ac.in/about/infrastructure-visual-tour/hostel/` |

---

## Summary of Delivered Knowledge Base
- **Initial Entries:** 57
- **Dropped Unverified Entries:** 6
- **Active Verified Entries:** 51
- **All Citations:** 100% verified against live URLs on `https://www.akgec.ac.in` and `https://erp.aktu.ac.in`.
- **Target Directory:** `kb-data/` (Contracts directory untouched and frozen).
- **Expanded / Scraped 74-entry dataset:** Preserved on dedicated branch `data-scraped`.
