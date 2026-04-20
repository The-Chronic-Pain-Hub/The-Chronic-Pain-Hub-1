"""
Neuro-symbolic pain assessment service.

Integrates LLM extraction with ontology mapping and rule-based reasoning.
This is the main entry point for the upgraded pain assessment system.

Architecture:
- Neural: LLM for narrow-scope entity extraction
- Symbolic: Dictionary-based ontology mapping + rule-based clinical reasoning
- Output: Fully explainable clinical recommendations with evidence chains
"""

import sys
import os

# Add Backend to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.pain_assessment_pipeline import PainAssessmentPipeline
from models.pain_schema import ExplainableReport
from services.llm_service import (
    extract_pain_entities_constrained, 
    normalize_transcription,
    match_pain_terms_from_vocabulary,
    translate_pain_description
)
from utils.language_detector import detect_language, get_language_name


# Initialize pipeline (singleton pattern for performance)
_pipeline = None


def get_pipeline() -> PainAssessmentPipeline:
    """
    Get or create pipeline instance.
    
    Uses singleton pattern to avoid reinitializing the rule engine
    on every request (improves performance).
    
    Returns:
        PainAssessmentPipeline instance
    """
    global _pipeline
    if _pipeline is None:
        _pipeline = PainAssessmentPipeline(verbose=True)
    return _pipeline


def analyze_pain_neuro_symbolic(patient_text: str) -> dict:
    """
    Main entry point for neuro-symbolic pain assessment.
    
    This function replaces the pure LLM analysis from the old system.
    It implements a complete neuro-symbolic hybrid architecture:
    
    1. LLM extracts entities (narrow-scope NER only)
    2. Ontology mapping converts Chinese to English medical terms
    3. Data is structured into validated Pydantic model
    4. Rule engine applies deterministic clinical logic
    5. Complete reasoning chain is generated for explainability
    
    Args:
        patient_text: Raw patient pain description (Chinese or multilingual)
        
    Returns:
        Dictionary representation of ExplainableReport containing:
        - structured_data: Normalized pain ontology (PainOntology)
        - ontology_mapping_trace: Chinese→English mapping details
        - clinical_recommendations: Rule-triggered recommendations with evidence
        - reasoning_chain: Step-by-step explanation of decision process
        - physician_summary: Human-readable clinical summary
        
    Example:
        >>> result = analyze_pain_neuro_symbolic("Lower back electric-shock pain for 4 months, feeling depressed")
        >>> print(result['structured_data']['pain_type'])
        'Neuropathic (Electric-shock-like)'
        >>> print(result['clinical_recommendations'][0]['triggered_by_rule'])
        'RULE_A: Chronic Pain + Depression'
    """
    try:
        # Step 0: Detect language for normalization
        detected_lang = detect_language(patient_text)
        language_name = get_language_name(detected_lang)
        
        # Step 1: Normalize transcription (fix Whisper errors & standardize expressions)
        print(f"[Neuro-Symbolic Service] Normalizing {language_name} transcription...")
        normalization_result = normalize_transcription(patient_text, language_name)
        
        original_text = normalization_result.get("original", patient_text)
        normalized_text = normalization_result.get("normalized", patient_text)
        corrections = normalization_result.get("corrections", [])
        normalization_confidence = normalization_result.get("confidence", "unknown")
        
        print(f"[Neuro-Symbolic Service] Applied {len(corrections)} corrections (confidence: {normalization_confidence})")
        
        # Step 2: Load vocabulary for detected language
        print(f"[Neuro-Symbolic Service] Loading {language_name} pain vocabulary...")
        from ontology.pain_mapping_multilingual import LANGUAGE_DESCRIPTORS
        
        vocabulary_dict = LANGUAGE_DESCRIPTORS.get(detected_lang, {})
        vocabulary_list = list(vocabulary_dict.keys())
        
        if not vocabulary_list:
            print(f"[Neuro-Symbolic Service] WARNING: No vocabulary for {language_name}, using English fallback")
            vocabulary_list = []
        else:
            print(f"[Neuro-Symbolic Service] Loaded {len(vocabulary_list)} terms for {language_name}")
        
        # Step 3: LLM term matching (with vocabulary)
        print("[Neuro-Symbolic Service] Matching pain terms from vocabulary...")
        
        llm_match_result = match_pain_terms_from_vocabulary(
            normalized_text, 
            vocabulary_list, 
            language_name
        )
        
        matched_terms = llm_match_result.get('matched_terms', [])
        print(f"[Neuro-Symbolic Service] LLM matched {len(matched_terms)} terms: {matched_terms}")
        
        # Step 4: Translate matched terms using dictionary
        print("[Neuro-Symbolic Service] Translating matched terms...")
        ontology_mappings = []
        
        for term in matched_terms:
            if term in vocabulary_dict:
                term_data = vocabulary_dict[term]
                ontology_mappings.append({
                    "original_term": term,
                    "matched_text": term,
                    "mapped_english": term_data["english"],
                    "dimension": term_data.get("dimension", "sensory"),
                    "pain_type": term_data.get("pain_type"),
                    "confidence": "high",  # High confidence because it's from dictionary
                    "mcgill_dimension": term_data.get("mcgill_dimension", "sensory"),
                    "detected_language": detected_lang
                })
        
        print(f"[Neuro-Symbolic Service] Translated {len(ontology_mappings)} terms to English")
        
        # Step 4.5: Extract unique/unmapped pain descriptors (creative expressions not in dictionary)
        print("[Neuro-Symbolic Service] Extracting unique pain descriptors...")
        from services.llm_service import extract_pain_entities_constrained
        unique_entities = extract_pain_entities_constrained(normalized_text)
        unique_descriptors = unique_entities.get("pain_descriptors", [])
        
        # These are creative/metaphorical descriptions not in our dictionary
        # Examples: "好像蚂蚁在爬", "说不出来的难受", "像被火烧一样"
        # V2: Will use multilingual dictionary (Chinese/Korean/Spanish/Hmong) for semantic matching
        if unique_descriptors:
            print(f"[Neuro-Symbolic Service] Found {len(unique_descriptors)} unique descriptors: {unique_descriptors}")
            print(f"[Neuro-Symbolic Service] → Will match against multilingual pain dictionary ({language_name})")
        
        # Prepare LLM entities for pipeline
        llm_entities = {
            "pain_descriptors": unique_descriptors,  # Original native language text (for multilingual semantic analysis V2)
            "location": llm_match_result.get("location", "Not stated"),
            "duration_phrase": llm_match_result.get("duration_phrase", "Not stated"),
            "intensity": llm_match_result.get("intensity", "Not stated"),
            "emotion_keywords": llm_match_result.get("emotion_keywords", []),
            "functional_impact": llm_match_result.get("functional_impact")
        }
        
        # Step 5: Execute complete pipeline (ontology mapping + rule engine)
        print("[Neuro-Symbolic Service] Executing pipeline...")
        pipeline = get_pipeline()
        report: ExplainableReport = pipeline.execute_with_mappings(
            normalized_text, 
            llm_entities,
            ontology_mappings  # Pass pre-computed mappings
        )
        
        # Step 6: Translate full sentence to English (if not English)
        english_translation = None
        if detected_lang != 'en':
            print(f"[Neuro-Symbolic Service] Translating from {language_name} to English...")
            english_translation = translate_pain_description(
                normalized_text,
                language_name,
                matched_terms,
                ontology_mappings
            )
            print(f"[Neuro-Symbolic Service] Translation: {english_translation}")
        
        # Step 7: Convert Pydantic models to dictionary for API response
        return {
            "status": "success",
            "transcription": {
                "original": original_text,
                "normalized": normalized_text,
                "english_translation": english_translation,  # NEW: Full sentence translation
                "corrections_applied": corrections,
                "normalization_confidence": normalization_confidence,
                "language_detected": language_name,
                "vocabulary_size": len(vocabulary_list),
                "matched_terms_count": len(matched_terms)
            },
            "structured_data": report.structured_data.model_dump(),
            "ontology_mapping_trace": report.ontology_mapping_trace,
            "clinical_recommendations": [
                rec.model_dump() for rec in report.clinical_recommendations
            ],
            "reasoning_chain": report.reasoning_chain,
            "physician_summary": report.physician_summary
        }
    
    except Exception as e:
        # Return error with detailed information for debugging
        import traceback
        return {
            "status": "error",
            "message": f"Pipeline execution failed: {str(e)}",
            "error_type": type(e).__name__,
            "traceback": traceback.format_exc()
        }


def get_system_info() -> dict:
    """
    Get information about the neuro-symbolic system configuration.
    
    Useful for debugging, monitoring, and documentation.
    
    Returns:
        Dictionary with system metadata
    """
    pipeline = get_pipeline()
    
    return {
        "system_name": "Neuro-Symbolic Pain Assessment System",
        "version": "1.0.0",
        "architecture": "Hybrid (Neural + Symbolic)",
        "components": {
            "neural": {
                "llm_model": "GPT-5.2",
                "purpose": "Named Entity Recognition only",
                "temperature": 0.1
            },
            "symbolic": {
                "ontology_mappings": "Chinese↔English pain descriptors",
                "rule_engine": "Deterministic If-Then clinical rules",
                "knowledge_bases": [
                    "McGill Pain Questionnaire (SF-MPQ)",
                    "SNOMED CT",
                    "Wisconsin Medical Examining Board Guidelines"
                ]
            }
        },
        "pipeline_info": pipeline.get_pipeline_info(),
        "capabilities": [
            "Cross-cultural pain assessment (Chinese→English)",
            "Deterministic clinical reasoning",
            "Complete explainability with evidence chains",
            "Neuropathic vs Nociceptive pain classification",
            "Guideline-based clinical recommendations"
        ],
        "limitations": [
            "Ontology coverage limited to defined descriptors",
            "Rule engine contains 4 clinical rules (expandable)",
            "Requires manual review for unmapped terms",
            "Not a diagnostic tool - for triage and assessment only"
        ]
    }


def validate_input(patient_text: str) -> tuple[bool, str]:
    """
    Validate patient input before processing.
    
    Args:
        patient_text: Raw patient input
        
    Returns:
        Tuple of (is_valid, error_message)
        If valid, error_message is empty string
    """
    if not patient_text or not patient_text.strip():
        return False, "Input text is empty"
    
    if len(patient_text) < 5:
        return False, "Input text too short (minimum 5 characters)"
    
    if len(patient_text) > 10000:
        return False, "Input text too long (maximum 10000 characters)"
    
    return True, ""


# Batch processing support (for future use)
def analyze_pain_batch(patient_texts: list[str]) -> list[dict]:
    """
    Process multiple patient descriptions in batch.
    
    Args:
        patient_texts: List of patient pain descriptions
        
    Returns:
        List of analysis results (one per input)
    """
    results = []
    for text in patient_texts:
        results.append(analyze_pain_neuro_symbolic(text))
    return results
