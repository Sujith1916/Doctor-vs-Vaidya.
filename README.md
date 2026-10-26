# Doctor vs Vaidya 🩺🌿
### Cross-System Medical Record Comparison Platform

## Overview

Doctor vs Vaidya is a web-based prototype designed to help users understand and compare medical records from Allopathy, Ayurveda, and Homeopathy. The platform accepts structured medical information through text input and provides functionality to store, retrieve, summarize, and compare records.

Using Python, FastAPI, SQLite, terminology mapping, and Google Gemini AI, the system generates informational comparisons that highlight similarities, differences, and missing information across selected medical records.

The project is intended for educational and informational purposes only. It does not provide diagnoses, prescribe treatments, or establish clinical equivalence between different healthcare systems.

## Key Features

- **Medical Record Management:** Save and retrieve medical records containing patient references, medical systems, conditions, medicines, and notes.
- **Multiple Healthcare Systems:** Supports records associated with Allopathy, Ayurveda, and Homeopathy.
- **Terminology Search:** Find possible related terms across healthcare systems using demonstration terminology mappings.
- **AI-Assisted Comparison:** Use Google Gemini AI to compare two medical records and generate a structured explanation.
- **Record Retrieval:** Retrieve individual records, view all saved records, and retrieve records associated with a patient reference.
- **Patient Record Separation:** Prevent comparisons between records belonging to different patient references.
- **REST API:** Provide endpoints for communication between the frontend and backend.
- **Interactive API Documentation:** Test available endpoints using FastAPI Swagger UI.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| ASGI Server | Uvicorn |
| Database | SQLite |
| Data Validation | Pydantic |
| AI Integration | Google Gemini API |
| Python SDK | `google-genai` |
| Environment Configuration | `python-dotenv` |
| API Testing | FastAPI Swagger UI |
| Version Control | Git and GitHub |

## Project Structure

```text
doctor-vs-vaidya/
├── main.py
├── database.py
├── models.py
├── terminology.py
├── requirements.txt
├── README.md
├── .gitignore
├── frontend/
│   └── index.html
├── .env                 # Local only; never commit
├── medical_records.db   # Local database
└── .venv/               # Python virtual environment
```

The structure above represents the original backend version. Keep any additional files required by your actual working setup.

## Prerequisites

- Python 3.10 or later
- pip
- A Google Gemini API key for AI-assisted comparison
- A modern web browser
- Visual Studio Code (recommended)

## Installation and Setup

### 1. Open the project directory

```powershell
cd C:\Users\SUJITH\Documents\doctor-vs-vaidya
```

### 2. Activate the virtual environment

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create a `.env` file in the project root if it does not already exist:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder with your own API key. Never publish the key or commit the `.env` file to GitHub.

### 5. Start the backend

```bash
python -m uvicorn main:app --reload
```

Keep the terminal open while using the application.

## Accessing the Application

- **Web application:** http://127.0.0.1:8000/
- **Interactive API documentation:** http://127.0.0.1:8000/docs
- **Backend health check:** http://127.0.0.1:8000/api/health

These local addresses work while the backend server is running on your computer.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Check the backend homepage |
| GET | `/api/health` | Check backend health |
| GET | `/api/terminology/search` | Search terminology mappings |
| POST | `/api/records` | Create a medical record |
| GET | `/api/records` | Retrieve all saved records |
| GET | `/api/records/{record_id}` | Retrieve one record |
| GET | `/api/patients/{patient_id}/records` | Retrieve records associated with a patient reference |
| GET | `/api/compare/{record_id_1}/{record_id_2}` | Compare two records using AI |

### Example: Create a Medical Record

Send a `POST` request to `/api/records` with JSON similar to:

```json
{
  "patient_reference": "PAT001",
  "medical_system": "allopathy",
  "record_type": "prescription",
  "condition_terms": ["Example condition"],
  "medicines": ["Example medicine"],
  "notes": "Example notes"
}
```

This is an illustrative request. Use the field names and allowed values defined in the current `models.py` file.

### Example: Search Terminology

Send a `GET` request to:

```text
/api/terminology/search?system=allopathy&term=diabetes
```

The response contains the source term, source medical system, and any available demonstration mappings.

### Example: Compare Records

Send a `GET` request using the IDs of two saved records:

```text
/api/compare/1/2
```

Both records must exist and belong to the same patient reference. The response includes an AI-generated informational comparison, subject to successful Gemini API access.

## Database

The project uses SQLite to store medical records locally. The database contains structured information such as patient references, medical systems, record types, condition terms, medicines, and notes.

The database connection and initialization are handled by `database.py`. The data model and validation rules are defined in `models.py`.

## AI-Assisted Comparison

The Gemini integration generates a readable comparison of two selected records. It is designed to highlight:

1. A summary of each record.
2. Similarities in recorded condition terms.
3. Differences in recorded condition terms.
4. Similarities and differences in medicine names.
5. Missing information and uncertainties.

The AI output depends on the supplied records and successful API access. It must not be treated as a verified clinical assessment.

## Limitations and Safety

- Terminology mappings are demonstration mappings and require independent verification.
- Similar terminology does not prove that two conditions, medicines, or treatments are clinically equivalent.
- AI-generated comparisons may contain errors or omissions.
- The prototype does not diagnose diseases or recommend, initiate, stop, or change treatment.
- Uploaded-photo text extraction (OCR) and automatic EHR import are not documented as implemented features in this version.
- Medical information should be reviewed by a qualified healthcare professional before being used for clinical decisions.
- Use appropriate privacy safeguards when handling patient information.

## Future Enhancements

- Add reliable prescription-photo upload and OCR.
- Support importing records from different EHR formats.
- Integrate verified terminology resources.
- Improve patient-specific record filtering and access controls.
- Add structured comparison reports and PDF export.
- Expand automated testing and deployment support.

## Running Tests

Start the backend and open:

http://127.0.0.1:8000/docs

Use the interactive documentation to test the available endpoints with sample data. Confirm that record creation, retrieval, terminology search, and AI comparison work correctly in the current environment.

## License

No license has been specified yet. Add an appropriate license before permitting reuse or redistribution.

---

**Doctor vs Vaidya** — An educational prototype for understanding and comparing medical documentation across healthcare systems.
