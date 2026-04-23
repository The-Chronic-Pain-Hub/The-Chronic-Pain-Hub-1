"""
Pain Mapping Report Generator
Generates clinical reports from pain mapping data
"""

from models.pain_mapping import PainMapData, PainReport, PainRegion
from typing import Dict, List
import uuid
from datetime import datetime


class PainMappingService:
    """Processes pain mapping data and generates reports"""
    
    # Clinical significance of pain types
    PAIN_TYPE_CLINICAL = {
        "burning": {
            "name": "Burning/燃烧感",
            "indicator": "High Neuropathic Pain Indicator",
            "color": "#005EB8",
            "neuropathic": True
        },
        "aching": {
            "name": "Aching/酸痛",
            "indicator": "Musculoskeletal / Non-neuropathic Pain",
            "color": "#F1C40F",
            "neuropathic": False
        },
        "stabbing": {
            "name": "Stabbing/刺痛",
            "indicator": "Sharp Neuropathic Pain",
            "color": "#E74C3C",
            "neuropathic": True
        },
        "numbness": {
            "name": "Numbness/麻木",
            "indicator": "Nerve Damage Indicator",
            "color": "#191C1E",
            "neuropathic": True
        },
        "tingling": {
            "name": "Tingling/刺痛感",
            "indicator": "Paresthesia (Neuropathic)",
            "color": "#27AE60",
            "neuropathic": True
        },
        "allodynia": {
            "name": "Touch Pain/触摸痛",
            "indicator": "Allodynia (Neuropathic)",
            "color": "#E67E22",
            "neuropathic": True
        },
        "other": {
            "name": "Other/其他",
            "indicator": "Non-standard sensation",
            "color": "#9B59B6",
            "neuropathic": False
        }
    }
    
    def calculate_statistics(self, pain_data: PainMapData) -> Dict:
        """Calculate pain statistics"""
        total_strokes = 0
        sensation_counts = {}
        neuropathic_count = 0
        
        # Count strokes for each region
        for region in pain_data.pain_regions:
            total_strokes += len(region.strokes)
            for stroke in region.strokes:
                pain_type = stroke.type
                sensation_counts[pain_type] = sensation_counts.get(pain_type, 0) + 1
                
                # Check if neuropathic pain
                if self.PAIN_TYPE_CLINICAL.get(pain_type, {}).get("neuropathic", False):
                    neuropathic_count += 1
        
        # Calculate percentages
        sensation_breakdown = {}
        if total_strokes > 0:
            for pain_type, count in sensation_counts.items():
                sensation_breakdown[pain_type] = round((count / total_strokes) * 100, 1)
        
        # Calculate average intensity
        if pain_data.pain_regions:
            avg_intensity = sum(r.intensity for r in pain_data.pain_regions) / len(pain_data.pain_regions)
        else:
            avg_intensity = 0.0
        
        return {
            "total_strokes": total_strokes,
            "sensation_breakdown": sensation_breakdown,
            "neuropathic_indicators": neuropathic_count,
            "overall_intensity": round(avg_intensity, 1)
        }
    
    def generate_summary(self, pain_data: PainMapData, stats: Dict) -> str:
        """Generate natural language summary"""
        summary_parts = []
        
        # Basic statistics
        num_regions = len(pain_data.pain_regions)
        if num_regions == 0:
            return "No pain regions mapped yet."
        
        summary_parts.append(f"Patient has mapped {num_regions} pain region(s).")
        
        # Intensity description
        intensity = stats["overall_intensity"]
        if intensity >= 7:
            intensity_desc = "severe pain"
        elif intensity >= 4:
            intensity_desc = "moderate pain"
        else:
            intensity_desc = "mild pain"
        
        summary_parts.append(f"Overall pain intensity: {intensity}/10 ({intensity_desc}).")
        
        # Primary sensation type
        breakdown = stats["sensation_breakdown"]
        if breakdown:
            sorted_sensations = sorted(breakdown.items(), key=lambda x: x[1], reverse=True)
            top_sensation = sorted_sensations[0]
            sensation_name = self.PAIN_TYPE_CLINICAL.get(top_sensation[0], {}).get("name", top_sensation[0])
            summary_parts.append(f"Dominant sensation: {sensation_name} ({top_sensation[1]}%).")
        
        # Neuropathic assessment
        neuro_percentage = (stats["neuropathic_indicators"] / stats["total_strokes"] * 100) if stats["total_strokes"] > 0 else 0
        if neuro_percentage >= 60:
            summary_parts.append("High probability of neuropathic pain component - recommend neurological evaluation.")
        elif neuro_percentage >= 30:
            summary_parts.append("Mixed pain presentation with neuropathic features.")
        else:
            summary_parts.append("Primarily non-neuropathic pain pattern.")
        
        return " ".join(summary_parts)
    
    def determine_neuropathic_probability(self, stats: Dict) -> str:
        """Determine neuropathic pain probability"""
        if stats["total_strokes"] == 0:
            return "unknown"
        
        neuro_percentage = (stats["neuropathic_indicators"] / stats["total_strokes"]) * 100
        
        if neuro_percentage >= 60:
            return "high"
        elif neuro_percentage >= 30:
            return "medium"
        else:
            return "low"
    
    def recommend_specialists(self, stats: Dict, pain_data: PainMapData) -> List[str]:
        """Recommend specialist physicians"""
        specialists = []
        
        neuro_prob = self.determine_neuropathic_probability(stats)
        
        if neuro_prob in ["high", "medium"]:
            specialists.append("Neurologist - for neuropathic pain evaluation")
        
        if stats["overall_intensity"] >= 7:
            specialists.append("Pain Management Specialist - for severe pain")
        
        # Check specific regions
        regions_mentioned = [r.name.lower() for r in pain_data.pain_regions]
        if any("back" in r or "spine" in r or "lumbar" in r for r in regions_mentioned):
            specialists.append("Orthopedic Specialist / Spine Surgeon")
        
        if any("joint" in r or "knee" in r or "shoulder" in r for r in regions_mentioned):
            specialists.append("Rheumatologist or Orthopedic Specialist")
        
        if not specialists:
            specialists.append("Primary Care Physician - for initial evaluation")
        
        return specialists
    
    def generate_report(self, pain_data: PainMapData) -> PainReport:
        """Generate complete pain report"""
        # Calculate statistics
        stats = self.calculate_statistics(pain_data)
        
        # Update statistics in pain_data
        pain_data.total_strokes = stats["total_strokes"]
        pain_data.sensation_breakdown = stats["sensation_breakdown"]
        pain_data.neuropathic_indicators = stats["neuropathic_indicators"]
        pain_data.overall_intensity = stats["overall_intensity"]
        
        # Generate summary
        summary = self.generate_summary(pain_data, stats)
        
        # Determine dominant sensations
        dominant_sensations = []
        if stats["sensation_breakdown"]:
            sorted_sensations = sorted(
                stats["sensation_breakdown"].items(),
                key=lambda x: x[1],
                reverse=True
            )
            # Take top 3
            for pain_type, percentage in sorted_sensations[:3]:
                if percentage > 0:
                    dominant_sensations.append(
                        f"{self.PAIN_TYPE_CLINICAL.get(pain_type, {}).get('name', pain_type)} ({percentage}%)"
                    )
        
        # Neuropathic probability
        neuro_prob = self.determine_neuropathic_probability(stats)
        
        # Recommend specialists
        specialists = self.recommend_specialists(stats, pain_data)
        
        # Region summary
        regions_summary = []
        for region in pain_data.pain_regions:
            regions_summary.append({
                "name": region.name,
                "view": region.view,
                "sensation": self.PAIN_TYPE_CLINICAL.get(region.sensation, {}).get("name", region.sensation),
                "intensity": region.intensity,
                "depth_layer": self._get_depth_label(region.depth)
            })
        
        # Create report
        report = PainReport(
            report_id=str(uuid.uuid4()),
            patient_id=pain_data.patient_id,
            summary=summary,
            pain_regions_summary=regions_summary,
            dominant_sensations=dominant_sensations,
            neuropathic_probability=neuro_prob,
            recommended_specialists=specialists,
            mapping_data=pain_data
        )
        
        return report
    
    def _get_depth_label(self, depth: int) -> str:
        """Get depth layer label"""
        if depth < 25:
            return "Dermal (skin level)"
        elif depth < 50:
            return "Subcutaneous Fascia"
        elif depth < 75:
            return "Muscular layer"
        else:
            return "Skeletal (deep tissue)"


# Singleton instance
pain_mapping_service = PainMappingService()
