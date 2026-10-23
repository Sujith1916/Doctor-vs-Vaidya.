from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class PrescriptionInput(BaseModel):
    condition: Optional[str] = Field(None, description="Diagnostic condition or primary symptom")
    text: str = Field(..., description="Raw text of the prescription or medicine names")
    notes: Optional[str] = Field(None, description="Additional patient notes, instructions or doctor advice")


class CompareRequest(BaseModel):
    allopathic: PrescriptionInput = Field(..., description="Allopathic / Modern Medicine prescription")
    ayurvedic: PrescriptionInput = Field(..., description="Ayurvedic / Classical Medicine prescription")
    condition: Optional[str] = Field(None, description="Optional overarching condition override")
    api_key: Optional[str] = Field(None, description="Optional user-provided Gemini API key")



class ComparisonDetailRow(BaseModel):
    key_id: str = Field(..., description="Unique key identifier for the comparison metric")
    title: str = Field(..., description="User-friendly title of the metric")
    icon: str = Field("activity", description="Icon identifier for frontend rendering")
    allopathic_value: str = Field(..., description="Allopathic perspective / data")
    ayurvedic_value: str = Field(..., description="Ayurvedic perspective / data")
    key_difference: str = Field(..., description="Summary takeaway highlighting the contrast")
    significance: str = Field("medium", description="Significance level: high, medium, neutral")


class DrugInteraction(BaseModel):
    severity: str = Field("warning", description="Severity level: danger, warning, caution, info")
    allopathic_agent: str = Field(..., description="Allopathic drug involved")
    ayurvedic_herb: str = Field(..., description="Ayurvedic formulation or botanical involved")
    interaction_type: str = Field(..., description="Pharmacokinetic or Pharmacodynamic nature")
    description: str = Field(..., description="Clinical risk description")
    clinical_advice: str = Field(..., description="Actionable safety guidance")


class MedicineDetail(BaseModel):
    name: str = Field(..., description="Name of the medicine or formulation")
    type: str = Field("allopathic", description="'allopathic' or 'ayurvedic'")
    active_constituents: List[str] = Field(default_factory=list, description="Chemical salts or Botanical herbs")
    primary_action: str = Field(..., description="Primary pharmacological or dosha balancing action")
    typical_dosage: Optional[str] = Field(None, description="Standard dosage or administration")
    anupana_or_carrier: Optional[str] = Field(None, description="Carrier medium (Water, Honey, Ghee, etc.)")


class ComparisonResponse(BaseModel):
    condition_detected: str = Field(..., description="Identified clinical indication or condition")
    paradigm_summary: Dict[str, str] = Field(
        ...,
        description="High-level contrast between Allopathic and Ayurvedic paradigms"
    )
    comparison_table: List[ComparisonDetailRow] = Field(
        ...,
        description="Predefined key comparison criteria matrix"
    )
    allopathic_medications: List[MedicineDetail] = Field(
        default_factory=list,
        description="Parsed allopathic drugs"
    )
    ayurvedic_formulations: List[MedicineDetail] = Field(
        default_factory=list,
        description="Parsed ayurvedic formulations"
    )
    interactions: List[DrugInteraction] = Field(
        default_factory=list,
        description="Potential herb-drug interactions if taken together"
    )
    clinical_verdict: Dict[str, Any] = Field(
        ...,
        description="Comprehensive summary and recommendations for integrated care"
    )


class PresetItem(BaseModel):
    id: str
    title: str
    icon: str
    category: str
    condition: str
    allopathic_text: str
    allopathic_notes: str
    ayurvedic_text: str
    ayurvedic_notes: str
    brief: str
