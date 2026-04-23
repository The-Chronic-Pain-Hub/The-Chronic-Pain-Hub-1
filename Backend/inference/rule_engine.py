"""
Deterministic rule-based clinical inference engine.

Applies expert-validated If-Then rules to structured pain ontology data.
NO probabilistic reasoning or LLM-based inference - all clinical logic is 
deterministic and traceable.

This module implements the symbolic reasoning component of the neuro-symbolic
hybrid architecture, ensuring medical decisions are explainable and evidence-based.
"""

from typing import List, Dict, Callable
from dataclasses import dataclass
import sys
import os

# Add Backend to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.pain_schema import PainOntology, ClinicalRecommendation


@dataclass
class ClinicalRule:
    """
    Represents a single clinical decision rule.
    
    Each rule consists of:
    - Condition: A function that evaluates PainOntology and returns True/False
    - Action: The recommendation to make if condition is met
    - Evidence fields: Which PainOntology fields to include as evidence
    - Guideline reference: Citation to clinical guideline supporting the rule
    """
    rule_id: str
    name: str
    condition: Callable[[PainOntology], bool]
    recommendation: str
    evidence_fields: List[str]
    guideline_reference: str = None
    confidence: str = "high"


class RuleEngine:
    """
    Expert system rule engine for pain assessment.
    
    Applies deterministic clinical rules to structured pain data and generates
    explainable recommendations with complete evidence chains.
    
    All rules are:
    1. Based on established clinical guidelines
    2. Deterministic (no probabilistic inference)
    3. Fully explainable (evidence is explicitly tracked)
    4. Independently verifiable by medical experts
    """
    
    def __init__(self):
        """Initialize rule engine and load clinical decision rules."""
        self.rules: List[ClinicalRule] = []
        self._initialize_rules()
    
    def _initialize_rules(self):
        """
        Initialize clinical decision rules.
        
        Each rule is based on established clinical guidelines and pain management
        best practices. Rules are evaluated in order of priority.
        """
        
        # ========== RULE A: Chronic Pain + Depressive Symptoms → Behavioral Therapy ==========
        def rule_a_condition(pain_data: PainOntology) -> bool:
            """
            Chronic pain with significant affective distress requires multimodal approach.
            
            Based on: Wisconsin Medical Examining Board Guidelines for Chronic Pain Management
            Rationale: Chronic pain with depression benefits from CBT and non-pharmacologic
                      interventions before considering pharmacological escalation.
            """
            temporal_chronic = (
                pain_data.temporal_pattern and 
                ("chronic" in pain_data.temporal_pattern.lower() or "months" in pain_data.temporal_pattern.lower())
            )
            
            emotion_depressed = pain_data.emotion and any(
                term in pain_data.emotion.lower() 
                for term in ["depressed", "depression", "despair", "hopeless"]
            )
            
            return temporal_chronic and emotion_depressed
        
        self.rules.append(ClinicalRule(
            rule_id="RULE_A",
            name="Chronic Pain + Depression → Behavioral Therapy",
            condition=rule_a_condition,
            recommendation=(
                "Recommend behavioral therapy (CBT) per Wisconsin chronic pain guidelines. "
                "Chronic pain with significant depressive symptoms benefits from "
                "culturally concordant behavioral interventions. Prioritize non-pharmacologic "
                "multidisciplinary care before considering pharmacological escalation."
            ),
            evidence_fields=["temporal_pattern", "emotion"],
            guideline_reference="Wisconsin Medical Examining Board Guidelines for Chronic Pain Management",
            confidence="high"
        ))
        
        # ========== RULE B: Neuropathic Pain in Distal Extremities → Peripheral Neuropathy Screening ==========
        def rule_b_condition(pain_data: PainOntology) -> bool:
            """
            Neuropathic pain in hands/feet suggests peripheral neuropathy.
            
            Rationale: Classic presentation of peripheral neuropathy includes neuropathic
                      pain descriptors (electric-shock, tingling, burning) in distal extremities.
                      Requires screening for underlying causes (diabetes, vitamin B12 deficiency, etc.)
            """
            neuropathic = pain_data.pain_type and "neuropathic" in pain_data.pain_type.lower()
            
            distal_location = pain_data.location and any(
                loc in pain_data.location.lower() 
                for loc in ["lower extremities", "feet", "hands", "legs", "arms", "extremities"]
            )
            
            return neuropathic and distal_location
        
        self.rules.append(ClinicalRule(
            rule_id="RULE_B",
            name="Neuropathic Pain in Distal Extremities → Peripheral Neuropathy Screening",
            condition=rule_b_condition,
            recommendation=(
                "Recommend peripheral neuropathy screening. "
                "Neuropathic pain in distal extremities suggests possible peripheral nerve pathology. "
                "Consider neurological examination and investigation of potential underlying causes "
                "(diabetes mellitus, vitamin B12 deficiency, autoimmune conditions, medication toxicity)."
            ),
            evidence_fields=["pain_type", "location"],
            confidence="high"
        ))
        
        # ========== RULE C: Severe Functional Impact → Multidisciplinary Pain Clinic Referral ==========
        def rule_c_condition(pain_data: PainOntology) -> bool:
            """
            Severe functional impairment requires comprehensive pain management.
            
            Rationale: Pain causing significant functional disability (sleep, work, mobility)
                      often requires multidisciplinary approach beyond primary care.
            """
            has_functional_impact = pain_data.functional_impact is not None
            
            severe_impact = has_functional_impact and any(
                term in pain_data.functional_impact.lower()
                for term in ["severe", "unable", "cannot", "impossible", "interfere", "disability"]
            )
            
            return severe_impact
        
        self.rules.append(ClinicalRule(
            rule_id="RULE_C",
            name="Severe Functional Impact → Multidisciplinary Pain Clinic",
            condition=rule_c_condition,
            recommendation=(
                "Consider referral to multidisciplinary pain clinic. "
                "Severe functional impairment indicates need for comprehensive pain management "
                "involving physical therapy, occupational therapy, psychological support, and "
                "coordinated medical management."
            ),
            evidence_fields=["functional_impact", "temporal_pattern"],
            confidence="high"
        ))
        
        # ========== RULE D: Burning Pain → Consider Inflammatory or Neuropathic Etiology ==========
        def rule_d_condition(pain_data: PainOntology) -> bool:
            """
            Burning pain quality suggests specific etiologies.
            
            Rationale: Burning pain can indicate inflammatory processes or small fiber neuropathy.
            """
            burning_pain = pain_data.pain_type and "burning" in pain_data.pain_type.lower()
            return burning_pain
        
        self.rules.append(ClinicalRule(
            rule_id="RULE_D",
            name="Burning Pain → Inflammatory/Neuropathic Workup",
            condition=rule_d_condition,
            recommendation=(
                "Burning pain quality suggests possible inflammatory or small fiber neuropathic etiology. "
                "Consider evaluation for inflammatory conditions, nerve injury, or small fiber neuropathy. "
                "May benefit from topical treatments or neuropathic pain medications."
            ),
            evidence_fields=["pain_type", "location"],
            confidence="medium"
        ))
    
    def evaluate(self, pain_data: PainOntology) -> List[ClinicalRecommendation]:
        """
        Apply all rules to the pain data and return triggered recommendations.
        
        Each recommendation includes:
        - The clinical recommendation text
        - Which rule triggered it
        - The specific evidence (field values) that triggered the rule
        - Confidence level
        - Guideline reference
        
        Args:
            pain_data: Structured pain ontology data
            
        Returns:
            List of clinical recommendations with complete evidence chains
            
        Example:
            >>> pain = PainOntology(
            ...     pain_type="Neuropathic (Electric-shock-like)",
            ...     location="Lower extremities",
            ...     temporal_pattern="Chronic (4 months)",
            ...     emotion="Depressed"
            ... )
            >>> engine = RuleEngine()
            >>> recommendations = engine.evaluate(pain)
            >>> # Returns recommendations for RULE_A and RULE_B
        """
        recommendations = []
        
        for rule in self.rules:
            try:
                if rule.condition(pain_data):
                    # Extract evidence from specified fields
                    evidence = {}
                    for field in rule.evidence_fields:
                        if hasattr(pain_data, field):
                            value = getattr(pain_data, field)
                            if value is not None:  # Only include non-None values
                                evidence[field] = value
                    
                    recommendations.append(ClinicalRecommendation(
                        recommendation=rule.recommendation,
                        triggered_by_rule=f"{rule.rule_id}: {rule.name}",
                        evidence=evidence,
                        confidence=rule.confidence,
                        guideline_reference=rule.guideline_reference
                    ))
            except Exception as e:
                # Log error but continue evaluating other rules
                print(f"Warning: Error evaluating {rule.rule_id}: {str(e)}")
                continue
        
        return recommendations
    
    def generate_reasoning_chain(
        self, 
        pain_data: PainOntology, 
        recommendations: List[ClinicalRecommendation],
        ontology_mappings: List[Dict]
    ) -> List[str]:
        """
        Generate human-readable reasoning chain showing complete decision pathway.
        
        This provides full transparency from patient input to clinical recommendations,
        enabling clinical validation and building trust in the system.
        
        The reasoning chain includes:
        1. Ontology mapping (Chinese → English medical terms)
        2. Structured pain data extraction
        3. Rule evaluation and triggers
        4. Final recommendations with evidence
        
        Args:
            pain_data: Structured pain ontology data
            recommendations: List of triggered recommendations
            ontology_mappings: List of multilingual→English mappings
            
        Returns:
            List of reasoning step strings
            
        Example output:
            [
                "=== Ontology Mapping ===",
                "Input '电击一样' → Mapped to 'Electric-shock-like (Neuropathic)'",
                "=== Structured Pain Data ===",
                "Pain Type: Neuropathic (Electric-shock-like)",
                "=== Rule Engine Evaluation ===",
                "✓ Triggered: RULE_B",
                "  Evidence: {'pain_type': 'Neuropathic', 'location': 'Lower extremities'}"
            ]
        """
        chain = []
        
        # ===== Step 1: Show ontology mappings =====
        chain.append("=== Ontology Mapping ===")
        if ontology_mappings:
            for mapping in ontology_mappings:
                # Show: matched text in user input → dictionary term → English translation
                matched = mapping.get('matched_text', mapping.get('original_term', 'N/A'))
                original = mapping.get('original_term', 'N/A')
                english = mapping.get('mapped_english', 'N/A')
                
                # Display: what user said → what it matches → English term
                if matched != original:
                    display_input = f"{matched} (matches '{original}')"
                else:
                    display_input = matched
                
                chain.append(
                    f"Input '{display_input}' → "
                    f"Mapped to '{english}' "
                    f"({mapping.get('dimension', 'N/A')}, confidence: {mapping.get('confidence', 'N/A')})"
                )
        else:
            chain.append("No specific pain descriptors were mapped from ontology dictionary.")
        
        # ===== Step 2: Show structured data extraction =====
        chain.append("\n=== Structured Pain Data ===")
        chain.append(f"Pain Type: {pain_data.pain_type}")
        chain.append(f"Location: {pain_data.location}")
        chain.append(f"Temporal Pattern: {pain_data.temporal_pattern}")
        if pain_data.intensity and pain_data.intensity != "Not explicitly stated":
            chain.append(f"Intensity: {pain_data.intensity}")
        if pain_data.emotion:
            chain.append(f"Emotional Dimension: {pain_data.emotion}")
        if pain_data.functional_impact:
            chain.append(f"Functional Impact: {pain_data.functional_impact}")
        
        # ===== Step 3: Show rule triggers and recommendations =====
        chain.append("\n=== Rule Engine Evaluation ===")
        if recommendations:
            for rec in recommendations:
                chain.append(f"✓ Triggered: {rec.triggered_by_rule}")
                chain.append(f"  Evidence: {rec.evidence}")
                chain.append(f"  → Recommendation: {rec.recommendation}")
                if rec.guideline_reference:
                    chain.append(f"  → Guideline: {rec.guideline_reference}")
                chain.append("")  # Blank line for readability
        else:
            chain.append("No specific clinical rules triggered.")
            chain.append("Standard pain assessment and management pathway recommended.")
        
        return chain
    
    def add_rule(self, rule: ClinicalRule):
        """
        Add a custom clinical rule to the engine.
        
        This allows for dynamic rule expansion and customization based on
        specific clinical contexts or institutional guidelines.
        
        Args:
            rule: ClinicalRule instance to add
        """
        self.rules.append(rule)
    
    def get_rule_count(self) -> int:
        """Return the number of active rules in the engine."""
        return len(self.rules)
    
    def get_rule_ids(self) -> List[str]:
        """Return list of all rule IDs for reference."""
        return [rule.rule_id for rule in self.rules]
