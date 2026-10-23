from typing import Literal, Optional
from pydantic import BaseModel, Field


class MedicalRecord(BaseModel):
    patient_reference: str = Field(
        ..., min_length=1,
        description="A fictional or anonymized patient reference"
    )

    medical_system: Literal[
        "allopathy",
        "ayurveda",
        "homeopathy"
    ]

    record_type: Literal[
        "prescription",
        "ehr"
    ]

    condition_terms: list[str] = Field(default_factory=list)

    medicines: list[str] = Field(default_factory=list)

    notes: Optional[str] = None