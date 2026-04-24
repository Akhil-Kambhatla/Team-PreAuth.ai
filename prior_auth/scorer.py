import json
from pathlib import Path
import anthropic
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")


SYSTEM_PROMPT = """
You are a clinical prior authorization specialist with deep knowledge
of insurance payer policies and medical documentation requirements.

You will receive two documents: an insurance payer policy and a
patient medical record. Cross-reference them carefully and identify
every gap or mismatch that would cause a prior authorization request
to be denied.

Look specifically for:
- Missing required clinical documentation
- Step therapy or fail-first requirements not met
- Diagnosis codes mismatched with the requested treatment
- Medical necessity language absent or insufficient
- Quantity, frequency, or duration outside policy limits
- Age, gender, or comorbidity exclusions in the policy
- Out-of-network or non-covered provider issues

Return ONLY a valid JSON object. No markdown. No explanation outside
the JSON. Exact structure required:
{
  "score": <integer 0-100>,
  "confidence_low": <integer, score minus 5-15 based on doc quality>,
  "confidence_high": <integer, score plus 5-15 based on doc quality>,
  "label": <"Low" | "Moderate" | "High" | "Very High">,
  "rationale": "<2-3 sentences in plain English>",
  "risk_factors": ["<specific issue>", "<specific issue>"],
  "suggested_actions": ["<specific fix>", "<specific fix>"]
}

Score guide:
0-24   → Low (likely approved)
25-49  → Moderate (minor gaps)
50-74  → High (significant gaps)
75-100 → Very High (likely denied as-is)

Confidence interval: narrow (±5-8) when docs are thorough and policy
is explicit. Wide (±12-18) when docs are sparse or policy is vague.
"""


def _truncate(text: str) -> str:
    words = text.split()
    if len(words) <= 4000:
        return text
    return " ".join(words[:3500]) + "\n...[truncated]...\n" + " ".join(words[-500:])


def score_risk(policy_text: str, record_text: str) -> dict:
    fallback = {
        "score": 0,
        "confidence_low": 0,
        "confidence_high": 0,
        "label": "Error",
        "rationale": "Could not parse AI response.",
        "risk_factors": [],
        "suggested_actions": [],
    }

    try:
        client = anthropic.Anthropic()
        policy_trunc = _truncate(policy_text)
        record_trunc = _truncate(record_text)

        user_message = (
            f"PAYER POLICY DOCUMENT:\n{policy_trunc}\n\n"
            f"---\n\n"
            f"PATIENT MEDICAL RECORD:\n{record_trunc}\n\n"
            f"Analyze and return the JSON risk assessment."
        )

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )

        raw = response.content[0].text.strip()
        raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(raw)
    except Exception:
        return fallback
