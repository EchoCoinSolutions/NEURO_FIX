# NEURO-FIX: Real-Time Behavioral Drift Engine

> Detect emotional and cognitive state shifts from text — before the user even realizes it.

**Neuro-Fix** is a deterministic, audit-ready system that detects psychological drift in real-time using:

- Typing latency (pause-to-submit timing)
- Entropy (linguistic unpredictability)
- Phrase classification (e.g. "freeze", "grief", "masking")
- Drift scoring (compared to session baselines)

It runs entirely **offline**, requires **no biometric input**, uses **no AI black-box logic**, and generates **time-stamped, forensic logs** suitable for clinical review, field deployment, or academic submission.

---

##  What This System Does

- Accepts live input (via terminal or interface)
- Logs every phrase with:
  - Latency
  - Entropy
  - Phrase category (e.g., “self-abandoning”, “grief”)
  - Drift score (relative to prior entries)
- Flags phrases that cross escalation thresholds
- Calibrates thresholds over time (adaptive sensitivity)
- Outputs .jsonl logs, .csv exports, and drift trendline charts

---

##  Use Cases

| Sector | Use |
|--------|-----|
| **Clinical Psychology** | Detect early spiraling in trauma recovery or grief sessions |
| **Cognitive Ops / Task Forces** | Monitor typed comms for drift in undercover operatives or CI handlers |
| **Mental Health Tech** | Add drift logging and entropy scoring to journaling apps or AI co-pilots |
| **Forensic Linguistics** | Behavioral state tracing across session logs |

---

##  Repo Contents

- `run_live_classify.py` → Entry point
- `/config/` → Approved phrase mappings, thresholds
- `/logs/` → .jsonl session logs
- `/exports/` → Charts, .csvs, reports
- `NeuroFix_Spec_Sheet.txt` → Formal description
- `INTEGRITY.txt` → Timestamped SHA-256 hash of this repo
- `LICENSE` → Author-controlled usage terms

---

## Integrity + Attribution

This system was developed and released by **Nicoleta C.**  
First published: `2025-07-19 UTC`  
SHA-256 hash of this codebase: `[pending]`  
All sessions are loggable, auditable, and cryptographically verifiable.

---

##  Paper, Abstract, & Submission Materials

Formal abstract, SHA-verified research export, and PDF submission kits included in `/exports/`. Suitable for:

- arXiv
- SSRN
- NIH exploratory grants
- DARPA behavioral research submissions

---

##  License Summary (Full Terms in LICENSE)

 Permitted:
- Academic use
- Clinical pilot studies
- Mental health tool integration

 Prohibited:
- Classified forks without author approval
- Use in commercial surveillance systems
- Removal of authorship or SHA-linked origin

---

##  Status

 Operational  
 Research-Ready  
 Pilot-Deployable  
 Integrity-Locked

---

*This is not a model. It’s a map of the moment a person begins to lose themselves.*  
