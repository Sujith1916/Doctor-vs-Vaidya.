"""
Doctor vs Vaidya - FastAPI Application
Provides RESTful API powered by Google Gemini API and serves the frontend comparison dashboard.
"""

import os
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.models import CompareRequest, ComparisonResponse, PresetItem
from app.comparator import compare_prescriptions
from app.knowledge_base import CLINICAL_PRESETS
from app.gemini_service import get_api_key

# Base directory for static files
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="Doctor vs Vaidya - Gemini AI Prescription Comparator API",
    description="Dynamic AI comparison engine powered by Google Gemini API contrasting Allopathic and Ayurvedic prescriptions.",
    version="1.1.0"
)

# CORS middleware for open integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static directory exists
os.makedirs(STATIC_DIR, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    has_key = bool(get_api_key())
    return {
        "status": "healthy",
        "service": "Doctor vs Vaidya Prescription Comparator",
        "gemini_api_configured": has_key,
        "model": os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
        "version": "1.1.0"
    }


@app.get("/api/presets", response_model=List[PresetItem])
def get_presets():
    """Returns curated clinical presets for one-click testing."""
    return CLINICAL_PRESETS


@app.post("/api/compare", response_model=ComparisonResponse)
def compare_endpoint(
    payload: CompareRequest,
    x_gemini_api_key: Optional[str] = Header(None, alias="x-gemini-api-key")
):
    """Compares an Allopathic prescription and an Ayurvedic prescription via Google Gemini API."""
    if not payload.allopathic.text.strip():
        raise HTTPException(status_code=400, detail="Allopathic prescription text cannot be empty.")
    if not payload.ayurvedic.text.strip():
        raise HTTPException(status_code=400, detail="Ayurvedic prescription text cannot be empty.")

    api_key_candidate = x_gemini_api_key or payload.api_key

    try:
        response = compare_prescriptions(payload, api_key=api_key_candidate)
        return response
    except ValueError as ve:
        # e.g., missing API key or parse error
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        # e.g., Gemini API communication error
        raise HTTPException(status_code=502, detail=str(re))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")


@app.get("/")
async def serve_frontend():
    """Serves the frontend single-page application."""
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "Doctor vs Vaidya API is running. UI file is being initialized."}
