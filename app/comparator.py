"""
Comparator Engine for Doctor vs Vaidya
Delegates directly to the Gemini API for dynamic clinical AI extraction,
pharmacological comparison, and herb-drug safety evaluation.
"""

from typing import Optional
from app.models import CompareRequest, ComparisonResponse
from app.gemini_service import analyze_with_gemini


def compare_prescriptions(payload: CompareRequest, api_key: Optional[str] = None) -> ComparisonResponse:
    """Compares allopathic and ayurvedic prescriptions dynamically using Google Gemini API."""
    key = api_key or payload.api_key

    return analyze_with_gemini(
        allopath_text=payload.allopathic.text,
        allopath_notes=payload.allopathic.notes,
        ayurved_text=payload.ayurvedic.text,
        ayurved_notes=payload.ayurvedic.notes,
        condition_hint=payload.condition or payload.allopathic.condition or payload.ayurvedic.condition,
        api_key=key
    )
