"""
Pain Mapping Data Models
For storing and processing body pain mapping data
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class PainStroke(BaseModel):
    """Single pain marking point"""
    x: float = Field(..., description="X coordinate on canvas")
    y: float = Field(..., description="Y coordinate on canvas")
    type: str = Field(..., description="Pain type: burning, aching, stabbing, numbness, tingling, allodynia, other")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


class PainRegion(BaseModel):
    """Pain region (a named pain point)"""
    id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Region name (e.g., 'Left Shoulder')")
    view: str = Field(..., description="Body view: 'front' or 'back'")
    sensation: str = Field(..., description="Primary sensation type")
    intensity: float = Field(..., ge=0, le=10, description="Pain intensity 0-10")
    strokes: List[PainStroke] = Field(default_factory=list, description="Drawing strokes")
    depth: int = Field(default=50, ge=0, le=100, description="Tissue depth: 0=dermal, 33=fascia, 66=muscular, 100=skeletal")


class PainMapData(BaseModel):
    """Complete pain mapping data"""
    patient_id: Optional[str] = Field(None, description="Patient identifier (if available)")
    session_id: str = Field(..., description="Unique session identifier")
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    # Canvas data
    front_canvas_data: Optional[str] = Field(None, description="Base64 encoded front view canvas")
    back_canvas_data: Optional[str] = Field(None, description="Base64 encoded back view canvas")
    
    # Structured pain regions
    pain_regions: List[PainRegion] = Field(default_factory=list)
    
    # Aggregate statistics
    overall_intensity: float = Field(default=0.0, ge=0, le=10)
    sensation_breakdown: Dict[str, float] = Field(
        default_factory=dict,
        description="Percentage breakdown of each sensation type"
    )
    
    # Clinical flags
    neuropathic_indicators: int = Field(default=0, description="Count of neuropathic pain indicators")
    total_strokes: int = Field(default=0, description="Total number of paint strokes")


class PainReport(BaseModel):
    """Generated pain report"""
    report_id: str = Field(..., description="Unique report identifier")
    patient_id: Optional[str] = Field(None)
    generated_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    # Summary
    summary: str = Field(..., description="Natural language summary of pain mapping")
    
    # Pain distribution
    pain_regions_summary: List[Dict] = Field(default_factory=list)
    
    # Clinical insights
    dominant_sensations: List[str] = Field(default_factory=list)
    neuropathic_probability: str = Field(..., description="low/medium/high")
    recommended_specialists: List[str] = Field(default_factory=list)
    
    # Visualizations
    front_view_url: Optional[str] = None
    back_view_url: Optional[str] = None
    
    # Raw data reference
    mapping_data: PainMapData
