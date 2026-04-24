# PreAuth.ai — PA Denial Risk Scorer

> **Getting care should not depend on paperwork.**  
> **PreAuth.ai helps doctors and care teams move through prior authorization faster, so patients can get treated sooner.**

Upload an insurance policy PDF + patient medical record → get an AI-powered denial risk score before you submit.

**The problem:** Doctors spend 13 hours/week on prior authorization paperwork. 94% say it harms patient care. Every existing AI tool requires EHR integration and enterprise contracts — leaving solo and rural clinics with nothing.

**What this does:** Upload two PDFs. Get back a 0–100 denial risk score, plain-English explanation, and exact list of what to fix. No EHR. No contract. Just a browser.

## How to run

```bash
cd prior_auth

# Install dependencies
pip install -r requirements.txt

# Copy and fill in your Anthropic API key
cp .env.example .env
# edit .env and set ANTHROPIC_API_KEY=sk-ant-...

# Generate demo PDFs (only needed once)
python generate_demo_pdfs.py

# Start the server
uvicorn main:app --reload
```

Open http://localhost:8000 and click **Load Demo Case** to see it in action.

## Demo scenario

The included demo shows a rheumatoid arthritis patient being prescribed Humira. The record has 4 critical gaps vs. the BlueCrest policy — wrong diagnosis code, incomplete step therapy documentation, missing DAS28 score, and no rheumatologist note. Claude catches all of them.

## Why this matters

Doctors and care teams spend too much time going back and forth with insurance companies before they can move ahead with treatment. That means delays, stress, and in some cases, patients giving up before they get the care they need.

## Features

- Clean browser-based interface — no EHR or enterprise contract required
- Upload any policy PDF + medical record PDF
- 0–100 denial risk score with plain-English explanation
- Exact list of gaps and what to fix before submitting
- One-click demo case with a pre-loaded scenario

## How it works

1. Upload the insurer's policy PDF and the patient's medical record
2. Claude extracts and compares the two documents
3. Missing or weak criteria are flagged with a risk score
4. The provider sees exactly what to fix before submitting
5. Fewer denials, less back-and-forth, faster treatment

## Built by

- Akhil Khambatla
- Rohith Kumar Tappa
- Venkat Gollangi

---

> **No patient should be left waiting because paperwork moved slower than their illness.**
