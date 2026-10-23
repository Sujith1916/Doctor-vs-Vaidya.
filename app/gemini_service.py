"""
Gemini API Service for Doctor vs Vaidya
Interacts directly with the Google Gemini API to analyze prescriptions,
extract constituents, evaluate differences, and check herb-drug safety in real time.
"""

import os
import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, Dict, Any

from app.models import ComparisonResponse, ComparisonDetailRow, MedicineDetail, DrugInteraction


def get_api_key(passed_key: Optional[str] = None) -> Optional[str]:
    """Resolves the Gemini API key from explicit arg, env vars, or .env file."""
    if passed_key and passed_key.strip():
        return passed_key.strip()

    # Check environment variables
    env_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if env_key and env_key.strip():
        return env_key.strip()

    # Check .env file in project root
    env_file = Path(__file__).resolve().parent.parent / ".env"
    if env_file.exists():
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip("'\"")
                    if k in ("GEMINI_API_KEY", "GOOGLE_API_KEY") and v:
                        return v
        except Exception:
            pass

    return None


SYSTEM_PROMPT = """You are a world-class senior Integrative Clinical Pharmacologist and Classical Ayurvedic Vaidya expert.
Your task is to thoroughly analyze two medical prescriptions:
1. An Allopathic Prescription (Modern Medicine / Doctor)
2. An Ayurvedic Prescription (Classical Ayurveda / Vaidya)

You must objectively evaluate both prescriptions, extract active constituents, explain pharmacological mechanisms and Tridosha energetics, generate a comprehensive 9-point difference comparison table, detect any potential herb-drug interactions, and provide balanced clinical guidance.

You MUST respond strictly in valid JSON format matching the schema provided. Do not enclose in markdown code blocks like ```json. Return only pure JSON."""

COMPARISON_SCHEMA_PROMPT = """
Return a JSON object with this exact structure:
{
  "condition_detected": "Diagnosed clinical condition or primary indication (e.g. Type 2 Diabetes Mellitus / Madhumeha)",
  "paradigm_summary": {
    "allopathic": "1-2 sentences summarizing the modern pharmacological treatment strategy and molecular target",
    "ayurvedic": "1-2 sentences summarizing the classical Ayurvedic Tridosha, Agni, and Dhatu rejuvenation strategy"
  },
  "comparison_table": [
    {
      "key_id": "ingredients",
      "title": "1. Active Ingredients & Composition",
      "icon": "flask-conical",
      "allopathic_value": "Specific synthetic APIs, active salts, chemical classes present in the allopathic prescription",
      "ayurvedic_value": "Specific botanical Latin names, classical herbs, Bhasmas, and rasayanas present in the ayurvedic prescription",
      "key_difference": "Crisp synthesis highlighting the core contrast between chemical isolates vs whole-plant phytocomplex",
      "significance": "high"
    },
    {
      "key_id": "mechanism",
      "title": "2. Description & Pharmacological Mechanism",
      "icon": "cpu",
      "allopathic_value": "Detailed biochemical pathways, receptor antagonism/agonism, enzyme inhibition",
      "ayurvedic_value": "Dosha balancing (Vata/Pitta/Kapha), Agni enhancement, Ama detoxification, Srotas clearance",
      "key_difference": "Targeted pathway inhibition vs systemic metabolic/energetic homeostasis",
      "significance": "high"
    },
    {
      "key_id": "philosophy",
      "title": "3. Therapeutic Philosophy & Target",
      "icon": "sparkles",
      "allopathic_value": "Targeted acute symptom control and biomarker/parameter normalization",
      "ayurvedic_value": "Nidan Parivarjan (eliminating root causes) and Dhatu rejuvenation (Rasayana)",
      "key_difference": "Acute symptom suppression vs root-cause elimination & holistic equilibrium",
      "significance": "high"
    },
    {
      "key_id": "onset",
      "title": "4. Onset of Action & Timeline",
      "icon": "timer",
      "allopathic_value": "Expected onset time and duration of effect for the modern medications",
      "ayurvedic_value": "Expected onset time, cellular assimilation, and duration of effect for the classical herbs",
      "key_difference": "Immediate/rapid acute response vs progressive cumulative metabolic resetting",
      "significance": "medium"
    },
    {
      "key_id": "side_effects",
      "title": "5. Side Effects & Organ Safety Profile",
      "icon": "shield-alert",
      "allopathic_value": "Common adverse effects, GI distress, hepatic/renal clearance load, tolerance risks",
      "ayurvedic_value": "Safety profile, Shodhana purification status, digestive tolerance, organ-protective benefits",
      "key_difference": "High risk of organ strain and rebound vs organ-nourishing profile when properly purified",
      "significance": "high"
    },
    {
      "key_id": "administration",
      "title": "6. Administration & Carrier Medium (Anupana)",
      "icon": "coffee",
      "allopathic_value": "Standard oral ingestion timing with plain water (pre/post meal, OD/BD/TDS)",
      "ayurvedic_value": "Classical Anupana carrier vehicles (Honey, Warm Milk, Ghee, Lukewarm water) and Aushadha Sevana Kala",
      "key_difference": "Inert water swallow vs catalytic bio-enhancing vehicle (Anupana) boosting bioavailability",
      "significance": "medium"
    },
    {
      "key_id": "diet_lifestyle",
      "title": "7. Dietary & Lifestyle Protocols (Pathya / Apathya)",
      "icon": "utensils",
      "allopathic_value": "Standard general nutritional advice, exercise, hydration",
      "ayurvedic_value": "Strict Pathya (beneficial foods/routines) and Apathya (contraindicated triggers, Dinacharya)",
      "key_difference": "Advisory tips vs diet considered integral 50% of the active therapeutic cure",
      "significance": "medium"
    },
    {
      "key_id": "evidence_base",
      "title": "8. Evidence Base & Regulatory Standards",
      "icon": "book-open",
      "allopathic_value": "FDA/CDSCO clinical trials, double-blind RCTs, Cochrane reviews",
      "ayurvedic_value": "Classical Samhita references (Charaka, Sushruta, Vagbhata) + Ayurvedic Pharmacopoeia of India (API)",
      "key_difference": "Modern biochemical trial standards vs thousands of years of documented empirical wisdom and AYUSH monographs",
      "significance": "medium"
    },
    {
      "key_id": "suitability",
      "title": "9. Optimal Clinical Suitability & Role",
      "icon": "check-circle",
      "allopathic_value": "When Allopathy is strictly preferred (emergencies, acute severe crisis, quantifiable control)",
      "ayurvedic_value": "When Ayurveda is strictly preferred (chronic lifestyle disorders, long-term rehabilitation, preventive vitality)",
      "key_difference": "Emergency crisis control vs chronic lifestyle reversal and sustainable wellness",
      "significance": "high"
    }
  ],
  "allopathic_medications": [
    {
      "name": "Medicine name extracted from prescription",
      "type": "allopathic",
      "active_constituents": ["Chemical salt 1", "API 2"],
      "primary_action": "Pharmacological action summary",
      "typical_dosage": "Dosage/frequency extracted or standard",
      "anupana_or_carrier": "Plain drinking water"
    }
  ],
  "ayurvedic_formulations": [
    {
      "name": "Formulation name extracted from prescription",
      "type": "ayurvedic",
      "active_constituents": ["Latin botanical name 1", "Herb 2"],
      "primary_action": "Ayurvedic action & Dosha target",
      "typical_dosage": "Dosage/frequency extracted or classical",
      "anupana_or_carrier": "Recommended carrier (e.g. Honey / Warm water / Milk)"
    }
  ],
  "interactions": [
    {
      "severity": "danger | warning | caution | info",
      "allopathic_agent": "Allopathic drug involved",
      "ayurvedic_herb": "Ayurvedic herb/formulation involved",
      "interaction_type": "Pharmacokinetic / Pharmacodynamic mechanism",
      "description": "Clear explanation of the clinical risk or additive effect if taken concurrently",
      "clinical_advice": "Actionable guidance on timing separation or dosage precautions"
    }
  ],
  "clinical_verdict": {
    "allopathic_strength": "Summary of where the allopathic prescription provides the greatest clinical value",
    "ayurvedic_strength": "Summary of where the ayurvedic prescription provides the greatest clinical value",
    "integrated_recommendation": "Pragmatic medical advice on how a patient can safely navigate both therapies (including maintaining a 1-2 hour time separation and consulting their doctors)"
  }
}
"""


def analyze_with_gemini(
    allopath_text: str,
    allopath_notes: Optional[str],
    ayurved_text: str,
    ayurved_notes: Optional[str],
    condition_hint: Optional[str] = None,
    api_key: Optional[str] = None
) -> ComparisonResponse:
    """Calls Google Gemini API to analyze prescriptions dynamically."""

    resolved_key = get_api_key(api_key)
    if not resolved_key:
        raise ValueError(
            "Gemini API key not found. Please provide a GEMINI_API_KEY in your environment, "
            "in a .env file, or enter it in the web interface settings."
        )

    model_name = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={resolved_key}"

    user_content = f"""Please analyze and compare these two prescriptions:

=== ALLOPATHIC PRESCRIPTION (Modern Medicine / Doctor) ===
Prescription Text:
{allopath_text}

Additional Notes / Instructions:
{allopath_notes or 'None provided'}

=== AYURVEDIC PRESCRIPTION (Classical Ayurveda / Vaidya) ===
Prescription Text:
{ayurved_text}

Additional Notes / Anupana / Pathya:
{ayurved_notes or 'None provided'}

Condition Hint / Diagnosis:
{condition_hint or 'Detect automatically from prescriptions'}

{COMPARISON_SCHEMA_PROMPT}
"""

    payload_dict = {
        "systemInstruction": {
            "parts": [{"text": SYSTEM_PROMPT}]
        },
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_content}]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "application/json"
        }
    }

    req_bytes = json.dumps(payload_dict).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=req_bytes,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=40) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8") if e.fp else str(e)
        # Try falling back to gemini-1.5-flash if 2.5 is not accessible
        if model_name != "gemini-1.5-flash":
            try:
                fallback_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={resolved_key}"
                fallback_req = urllib.request.Request(
                    fallback_url,
                    data=req_bytes,
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                with urllib.request.urlopen(fallback_req, timeout=40) as fb_response:
                    res_body = fb_response.read().decode("utf-8")
                    res_json = json.loads(res_body)
            except Exception as fb_err:
                raise RuntimeError(f"Gemini API Error ({e.code}): {err_msg}")
        else:
            raise RuntimeError(f"Gemini API Error ({e.code}): {err_msg}")
    except Exception as e:
        raise RuntimeError(f"Failed to connect to Gemini API: {str(e)}")

    try:
        candidates = res_json.get("candidates", [])
        if not candidates:
            raise ValueError("No output candidate returned by Gemini API.")

        raw_text = candidates[0]["content"]["parts"][0]["text"]
        # Clean potential markdown wrapping if present
        cleaned_text = raw_text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.startswith("```"):
            cleaned_text = cleaned_text[3:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
        cleaned_text = cleaned_text.strip()

        parsed_data = json.loads(cleaned_text)

        # Parse into Pydantic models
        comp_rows = [ComparisonDetailRow(**row) for row in parsed_data.get("comparison_table", [])]
        allo_meds = [MedicineDetail(**m) for m in parsed_data.get("allopathic_medications", [])]
        ayur_meds = [MedicineDetail(**m) for m in parsed_data.get("ayurvedic_formulations", [])]
        interactions = [DrugInteraction(**i) for i in parsed_data.get("interactions", [])]

        return ComparisonResponse(
            condition_detected=parsed_data.get("condition_detected", "General Medical Condition"),
            paradigm_summary=parsed_data.get("paradigm_summary", {
                "allopathic": "Modern pharmacological therapy targeting specific physiological pathways.",
                "ayurvedic": "Classical Ayurvedic treatment balancing Tridoshas, Agni, and tissue health."
            }),
            comparison_table=comp_rows,
            allopathic_medications=allo_meds,
            ayurvedic_formulations=ayur_meds,
            interactions=interactions,
            clinical_verdict=parsed_data.get("clinical_verdict", {
                "allopathic_strength": "Acute symptom suppression and targeted parameter control.",
                "ayurvedic_strength": "Root-cause balance and holistic systemic nourishment.",
                "integrated_recommendation": "Consult healthcare professionals and maintain a 1-2 hour interval between doses."
            })
        )

    except Exception as e:
        raise ValueError(f"Failed to parse Gemini response into comparison model: {str(e)}")
