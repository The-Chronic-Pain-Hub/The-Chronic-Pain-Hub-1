"""
Pydantic data models for structured pain assessment.

This module defines the core data structures for the neuro-symbolic pain assessment system:
- PainOntology: Structured representation of pain characteristics
- ClinicalRecommendation: Rule-based clinical recommendations with evidence
- ExplainableReport: Complete assessment output with reasoning chain
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class PainOntology(BaseModel):
    """
    Core pain ontology representing structured clinical pain data.
    
    Maps unstructured patient descriptions to standardized medical terminology
    aligned with McGill Pain Questionnaire (SF-MPQ) and SNOMED CT.
    
    This is the minimal semantic structure that all pain descriptions must converge to.
    """
    
    pain_type: str = Field(
        description="Physical sensation description and neuropathic/nociceptive classification. "
                   "E.g., 'Neuropathic (Electric-shock-like, Tingling)' or 'Nociceptive (Aching, Burning)'"
    )
    
    intensity: Optional[str] = Field(
        default="Not explicitly stated",
        description="Pain intensity: numeric (0-10) or qualitative (Mild/Moderate/Severe). "
                   "Only capture if explicitly stated by patient."
    )
    
    location: str = Field(
        description="Anatomical location of pain. E.g., 'Lower back', 'Both knees', 'Upper extremities'"
    )
    
    emotion: Optional[str] = Field(
        default=None,
        description="Affective dimension: emotional distress associated with pain. "
                   "E.g., 'Depressed', 'Anxious', 'Exhausting', 'Frustrated'. "
                   "Maps to McGill Pain Questionnaire Affective dimension."
    )
    
    temporal_pattern: str = Field(
        description="Onset, frequency, and duration of pain. "
                   "E.g., 'Chronic (>3 months)', 'Acute (<3 months)', 'Intermittent', 'Constant'"
    )
    
    functional_impact: Optional[str] = Field(
        default=None,
        description="Impact on daily activities and quality of life. "
                   "E.g., 'Severe sleep interference', 'Unable to work', 'Limited mobility'"
    )
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "pain_type": "Neuropathic (Electric-shock-like, Tingling)",
                "intensity": "Not explicitly stated",
                "location": "Lower back to lower extremities",
                "emotion": "Depressed",
                "temporal_pattern": "Chronic (4 months)",
                "functional_impact": "Severe sleep interference"
            }
        }


class ClinicalRecommendation(BaseModel):
    """
    Represents a single clinical recommendation triggered by the rule engine.
    
    Each recommendation is linked to a specific clinical decision rule and includes
    the evidence (structured data fields) that triggered the rule.
    """
    
    recommendation: str = Field(
        description="Clinical action or pathway recommendation"
    )
    
    triggered_by_rule: str = Field(
        description="Name/ID of the rule that triggered this recommendation"
    )
    
    evidence: Dict[str, Any] = Field(
        description="Specific field values from PainOntology that triggered the rule"
    )
    
    confidence: str = Field(
        default="high",
        description="Confidence level of the recommendation: high/medium/low"
    )
    
    guideline_reference: Optional[str] = Field(
        default=None,
        description="Reference to clinical guideline or evidence base. "
                   "E.g., 'Wisconsin Medical Examining Board Guidelines for Chronic Pain Management'"
    )
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "recommendation": "Recommend behavioral therapy (CBT) per Wisconsin chronic pain guidelines",
                "triggered_by_rule": "RULE_A: Chronic Pain + Depression",
                "evidence": {
                    "temporal_pattern": "Chronic (4 months)",
                    "emotion": "Depressed"
                },
                "confidence": "high",
                "guideline_reference": "Wisconsin Medical Examining Board Guidelines"
            }
        }


class ExplainableReport(BaseModel):
    """
    Final output containing structured data, reasoning chain, and readable report.
    
    This is the complete output of the neuro-symbolic pain assessment pipeline,
    providing full transparency from input to clinical recommendations.
    
    Key components:
    - structured_data: Normalized pain ontology
    - ontology_mapping_trace: How Chinese terms were mapped to English medical terms
    - clinical_recommendations: Rule-triggered recommendations with evidence
    - reasoning_chain: Step-by-step reasoning from input to output
    - physician_summary: Human-readable clinical summary
    """
    
    structured_data: PainOntology = Field(
        description="Structured pain data following the PainOntology schema"
    )
    
    ontology_mapping_trace: List[Dict[str, Any]] = Field(
        description="Trace of Chinese input → English medical term mapping. "
                   "Each entry shows: chinese_input, mapped_english, dimension, pain_type, SNOMED CT code, confidence"
    )
    
    clinical_recommendations: List[ClinicalRecommendation] = Field(
        description="List of clinical recommendations triggered by rule engine"
    )
    
    reasoning_chain: List[str] = Field(
        description="Human-readable step-by-step reasoning process showing complete decision pathway"
    )
    
    physician_summary: str = Field(
        description="Natural language summary for clinical review"
    )
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "structured_data": {
                    "pain_type": "Neuropathic (Electric-shock-like, Tingling)",
                    "intensity": "Not explicitly stated",
                    "location": "Lower back to lower extremities",
                    "emotion": "Depressed",
                    "temporal_pattern": "Chronic (4 months)",
                    "functional_impact": "Severe sleep interference"
                },
                "ontology_mapping_trace": [
                    {
                        "multilingual_input": "electric-shock-like",
                        "mapped_english": "Electric-shock-like",
                        "dimension": "sensory",
                        "pain_type": "neuropathic",
                        "snomed_ct": "60924000",
                        "confidence": "high"
                    }
                ],
                "clinical_recommendations": [
                    {
                        "recommendation": "Recommend behavioral therapy (CBT)",
                        "triggered_by_rule": "RULE_A: Chronic Pain + Depression",
                        "evidence": {"temporal_pattern": "Chronic", "emotion": "Depressed"},
                        "confidence": "high"
                    }
                ],
                "reasoning_chain": [
                    "=== Ontology Mapping ===",
                    "Input 'electric-shock-like' → Mapped to 'Electric-shock-like (Neuropathic)'",
                    "=== Rule Engine Evaluation ===",
                    "✓ Triggered: RULE_A"
                ],
                "physician_summary": "Patient presents with chronic pain (4 months duration)..."
            }
        }
