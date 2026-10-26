# Doctor vs Vaidya 🩺🌿 (Gemini AI Edition)
### Allopathic vs Ayurvedic Prescription Comparator

An intelligent clinical pharmacology & Ayurveda comparison tool powered by **Google Gemini API**, **FastAPI**, **Uvicorn**, and managed with **uv**.

---

## 🌟 Overview

**Doctor vs Vaidya** takes an **Allopathic prescription** (Modern Medicine) and an **Ayurvedic prescription** (Classical Medicine) and uses **Google Gemini AI** to generate a real-time, dynamic **Difference Table** comparing them across 9 clinical and pharmacological dimensions.

---

## 🔑 Gemini API Key Configuration

The application supports setting the Gemini API key through any of the following methods:

1. **In the Web UI Dashboard (Easiest)**: Click the **"Gemini API Key"** button in the top navigation bar and enter your key. It is saved in your browser's `localStorage` and sent with requests.
2. **Environment Variable**:
   ```bash
   export GEMINI_API_KEY="your-gemini-api-key"
   ```
3. **`.env` File**: Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your-gemini-api-key
   GEMINI_MODEL=gemini-2.5-flash
   ```

*(Get a free API key at [Google AI Studio](https://aistudio.google.com/app/apikey)).*

---

## 🔬 9-Point Predefined Comparison Matrix

1. **Active Ingredients & Composition**: Synthetic single-molecule chemical salts (APIs) vs. botanical & herbo-mineral phytocomplexes.
2. **Description & Pharmacological Mechanism**: Targeted receptor/enzyme inhibition (e.g. AMPK, AT1 blockers, PPIs, COX inhibitors) vs. Tridosha balancing (Vata/Pitta/Kapha), Agni enhancement, and Ama detoxification.
3. **Therapeutic Philosophy**: Acute symptom suppression & biomarker normalization vs. Root-cause elimination (Nidan Parivarjan) and systemic tissue rejuvenation (Rasayana).
4. **Onset of Action & Timeline**: Rapid/immediate biochemical control vs. Progressive, gradual, and sustainable metabolic resetting.
5. **Side Effects & Organ Safety Profile**: Hepatic/renal load, tolerance, and GI risks vs. Shodhana-purified, organ-protective classical formulations.
6. **Administration & Carrier Medium (Anupana)**: Plain water oral intake vs. Synergistic bio-enhancing vehicles (Anupanas: honey, warm milk, ghee, herbal decoctions).
7. **Dietary & Lifestyle Regimen (Pathya / Apathya)**: Advisory nutritional guidelines vs. Rigorous personalized Ayurvedic dietary and circadian protocols (Dinacharya).
8. **Evidence Base & Regulatory Standards**: FDA/CDSCO multi-center randomized controlled trials (RCTs) vs. Classical Ayurvedic Samhitas (Charaka, Sushruta, Vagbhata) & Ayurvedic Pharmacopoeia of India (API).
9. **Optimal Clinical Suitability & Role**: Critical for acute emergencies and severe exacerbations vs. Chronic lifestyle management, prevention, and long-term vitality.

---

## ⚡ Key Features

- **Dynamic Gemini AI Generation**: Prescriptions are dynamically evaluated using Gemini with structured JSON output, eliminating hardcoded limitations.
- **Dual Prescription Inputs**: Dedicated input cards for Allopathy (Doctor) and Ayurveda (Vaidya) with real-time item counters.
- **1-Click Test Presets**: Ready-to-use clinical presets for Diabetes, Hypertension, GERD, Osteoarthritis, Insomnia, Bronchitis, and Cholesterol.
- **Herb-Drug Interaction Safety Engine**: Automatically detects and flags critical clashes (e.g. Hypoglycemia risk with Metformin + Bitter Melon, hypotensive collapse with Telmisartan + Sarpagandha, additive sedation with Zolpidem + Tagara).
- **Parsed Medication Breakdown Cards**: Visual cards displaying active constituents, mechanisms, and carrier media for each parsed medicine.
- **Integrated Clinical Verdict**: Pragmatic synthesis guiding safe multi-therapy, timing separations (1–2 hour rule), and physician coordination.
- **Export & Share**: One-click Print/PDF export and clipboard copy.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/) (or standard Python)

### 2. Running with `uv`

```bash
# Run using uv
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Or run via Python directly:
```bash
python main.py
```

### 3. Accessing the Application
- **Web UI Dashboard**: [http://localhost:8000](http://localhost:8000)
- **FastAPI Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📡 API Endpoints

### `POST /api/compare`
Compares an Allopathic prescription and an Ayurvedic prescription using Gemini AI.

**Headers:**
- `x-gemini-api-key` *(optional if set in env/backend)*: Your Google Gemini API Key

**Request Payload:**
```json
{
  "allopathic": {
    "text": "Tab. Metformin HCl 500 mg BD\nTab. Glimepiride 1 mg OD",
    "notes": "Advised HbA1c monitoring every 3 months"
  },
  "ayurvedic": {
    "text": "Madhumehantak Churna 3g BD with warm water\nNisha Amalaki 2 tabs BD",
    "notes": "Pathya: Barley (Yava), Bitter Gourd"
  },
  "api_key": "optional-api-key-here"
}
```

### `GET /api/presets`
Returns all curated clinical test case presets.

### `GET /api/health`
Returns health check status and whether Gemini API key is configured on server.
