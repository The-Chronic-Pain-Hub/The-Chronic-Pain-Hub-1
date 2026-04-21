"""
End-to-end neuro-symbolic pain assessment pipeline with multilingual support.

Orchestrates: LLM extraction -> Ontology mapping -> JSON structuring -> Rule engine -> Report generation

Supported Languages: Chinese (中文), Korean (한국어), Spanish (Español), Hmong

This module implements the complete data flow from unstructured patient input to
structured, explainable clinical recommendations. LLM is used ONLY for narrow-scope
entity extraction and optional report formatting. All clinical logic is deterministic
and rule-based.
"""

from typing import Dict, Any, List
import sys
import os

# Add Backend to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.pain_schema import PainOntology, ExplainableReport
from ontology.pain_mapping_multilingual import (
    map_multilingual_to_english,
    extract_temporal_pattern,
    extract_anatomical_location,
    get_supported_languages
)
from ontology.pain_mapping import get_unmapped_descriptors, suggest_similar_terms, verify_all_terms_with_semantic_model
from utils.language_detector import detect_language, get_language_name, LanguageCode
from inference.rule_engine import RuleEngine
from services.llm_service import generate_comprehensive_report
from utils.report_generator import translate_to_english_simple

# Smart semantic distance service selection
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "biolord")

if EMBEDDING_MODEL == "biolord":
    from services.semantic_distance_service_biolord import calculate_semantic_distances
else:
    from services.semantic_distance_service_v2 import calculate_semantic_distances


class PainAssessmentPipeline:
    """
    Orchestrates the complete neuro-symbolic pain assessment workflow.
    
    Pipeline stages:
    1. Input Reception - Receive raw patient text
    2. LLM Entity Extraction - Extract entities using constrained LLM (NER only)
    3. Ontology Mapping - Map Chinese terms to English medical terminology
    4. JSON Structuring - Populate PainOntology Pydantic model
    5. Rule Engine - Apply deterministic clinical decision rules
    6. Report Generation - Create final explainable report
    
    LLM is used ONLY for narrow-scope NER and final report formatting.
    All clinical logic is deterministic and rule-based.
    """
    
    def __init__(self, verbose: bool = True):
        """
        Initialize the pain assessment pipeline.
        
        Args:
            verbose: If True, print progress messages for each pipeline stage
        """
        self.rule_engine = RuleEngine()
        self.verbose = verbose
    
    def _log(self, message: str):
        """Print log message if verbose mode is enabled."""
        if self.verbose:
            print(message)
    
    def execute(
        self, 
        patient_text: str, 
        llm_entities: Dict[str, Any] = None,
        language: LanguageCode = None
    ) -> ExplainableReport:
        """
        Execute the complete pain assessment pipeline with multilingual support.
        
        Args:
            patient_text: Raw patient pain description in any supported language
                         (Chinese, Korean, Spanish, Hmong, English)
            llm_entities: Optional pre-extracted LLM entities (for testing or caching)
                         If None, will need to call LLM service externally
            language: Optional language code ('zh', 'ko', 'es', 'hmong', 'en')
                     If None, will auto-detect from text
            
        Returns:
            ExplainableReport with structured data, reasoning chain, and recommendations
            
        Example:
            >>> pipeline = PainAssessmentPipeline()
            >>> # Chinese input
            >>> text = "最近四个月腰部到腿部总是像触电一样的麻痛，晚上痛得睡不着，心情很郁闷"
            >>> llm_entities = {
            ...     "pain_descriptors": ["触电一样", "麻痛"],
            ...     "location": "腰部到腿部",
            ...     "duration_phrase": "四个月",
            ...     "emotion_keywords": ["郁闷"],
            ...     "functional_impact": "睡不着"
            ... }
            >>> report = pipeline.execute(text, llm_entities)
            >>> 
            >>> # Korean input
            >>> text_ko = "허리가 따끔거리듯이 아프다"
            >>> report = pipeline.execute(text_ko, language='ko')
        """
        
        # ===== Save context for GPT report generation =====
        self.original_patient_text = patient_text
        self.detected_language = None
        self.current_ontology_mappings = []
        
        # ===== Node 1: Input Reception with Language Detection =====
        self._log(f"[Node 1] Received input: {patient_text[:100]}...")
        
        # Auto-detect language if not specified
        if language is None:
            language = detect_language(patient_text)
        
        language_name = get_language_name(language)
        self.detected_language = language_name  # Save language name
        self._log(f"[Node 1] Detected language: {language_name} ({language})")
        
        # ===== Node 2: LLM Entity Extraction (Narrow-Scope NER) =====
        # Note: LLM extraction is handled externally by llm_service.py
        # This pipeline receives the extracted entities as input
        self._log("[Node 2] Using provided LLM entity extraction...")
        if llm_entities is None:
            llm_entities = {}  # Fallback to empty dict if not provided
        
        # ===== Node 3: Ontology Mapping (Deterministic) =====
        self._log(f"[Node 3] Performing {language_name} → English ontology mapping...")
        ontology_mappings = map_multilingual_to_english(patient_text, language)
        
        # ===== SEMANTIC MODEL VERIFICATION (All Terms) =====
        self._log(f"[Node 3] 🔬 Verifying ALL terms with semantic model...")
        ontology_mappings = verify_all_terms_with_semantic_model(
            patient_text, 
            ontology_mappings, 
            language
        )
        
        # Count different types of matches
        dict_matches = sum(1 for m in ontology_mappings if m.get("match_type") == "dictionary")
        both_matches = sum(1 for m in ontology_mappings if m.get("match_type") == "both")
        semantic_only = sum(1 for m in ontology_mappings if m.get("match_type") == "semantic_only")
        
        self._log(f"[Node 3] ✓ Dictionary matches: {dict_matches}")
        self._log(f"[Node 3] ✓ Dictionary + Semantic verified: {both_matches}")
        self._log(f"[Node 3] ⚠️ Semantic-only suggestions: {semantic_only}")
        
        self.current_ontology_mappings = ontology_mappings  # Save for GPT use
        temporal_pattern = extract_temporal_pattern(patient_text)
        locations = extract_anatomical_location(patient_text)
        
        # Check for unmapped descriptors (for logging only - already handled by semantic verification)
        unmapped = get_unmapped_descriptors(patient_text, ontology_mappings)
        
        self._log(f"[Node 3] Found {len(ontology_mappings)} term mapping(s) from {language_name}")
        
        # ===== Node 3.5: Semantic Analysis V2 (Multilingual Dictionary Matching) =====
        if unmapped:
            self._log(f"[Node 3.5] Analyzing {len(unmapped)} unmapped terms (V2: Multilingual dictionary)...")
            semantic_analysis = calculate_semantic_distances(
                unmapped_terms=unmapped,  # Original native language expressions
                patient_text=patient_text,
                language=language_name
            )
        else:
            semantic_analysis = None

        self.semantic_analysis = semantic_analysis
        
        # ===== Node 4: Forced JSON Structuring =====
        self._log("[Node 4] Constructing PainOntology JSON...")
        pain_data = self._construct_pain_ontology(
            llm_entities, 
            ontology_mappings, 
            temporal_pattern,
            locations,
            unmapped
        )
        
        # ===== Node 5: Rule Engine (Symbolic Reasoning) =====
        self._log("[Node 5] Applying clinical decision rules...")
        recommendations = self.rule_engine.evaluate(pain_data)
        self._log(f"[Node 5] Triggered {len(recommendations)} recommendation(s)")
        
        reasoning_chain = self.rule_engine.generate_reasoning_chain(
            pain_data, 
            recommendations, 
            ontology_mappings
        )
        
        # ===== Node 6: Report Generation =====
        self._log("[Node 6] Generating final clinical report...")
        physician_summary = self._generate_summary(
            pain_data, 
            recommendations,
            unmapped
        )
        
        # Assemble final explainable report
        report = ExplainableReport(
            structured_data=pain_data,
            ontology_mapping_trace=ontology_mappings,
            clinical_recommendations=recommendations,
            reasoning_chain=reasoning_chain,
            physician_summary=physician_summary
        )
        
        self._log("[Pipeline] Execution complete!")
        return report
    
    def execute_with_mappings(
        self, 
        patient_text: str, 
        llm_entities: Dict[str, Any],
        ontology_mappings: List[Dict],
        language: LanguageCode = None
    ) -> ExplainableReport:
        """
        Execute pipeline with pre-computed ontology mappings.
        
        Used when LLM has already matched terms from provided vocabulary.
        Skips the ontology mapping step and uses pre-translated mappings.
        
        Args:
            patient_text: Patient description
            llm_entities: LLM extracted structured fields (pain_descriptors = unique/unmapped terms)
            ontology_mappings: Pre-computed term translations from vocabulary
            language: Language code
            
        Returns:
            ExplainableReport with full analysis
        """
        if language is None:
            language = detect_language(patient_text)
        
        # ===== Save context for GPT report generation =====
        self.original_patient_text = patient_text
        language_name = get_language_name(language)
        self.detected_language = language_name
        self.current_ontology_mappings = ontology_mappings
        
        self._log(f"[Pipeline-Fast] Using {len(ontology_mappings)} pre-computed mappings")
        
        # Extract patterns
        temporal_pattern = extract_temporal_pattern(patient_text)
        locations = extract_anatomical_location(patient_text)
        
        # Unmapped descriptors = unique expressions in llm_entities.pain_descriptors
        # These are creative/metaphorical terms not in dictionary (e.g., "蚂蚁在爬", "따끔거리다")
        unmapped = llm_entities.get("pain_descriptors", [])
        
        # ===== Semantic Analysis V2: Multilingual Dictionary Matching =====
        if unmapped:
            self._log(f"[Pipeline-Fast] Analyzing {len(unmapped)} unmapped terms (V2: Multilingual dictionary)...")
            self.semantic_analysis = calculate_semantic_distances(
                unmapped_terms=unmapped,  # Original native language expressions
                patient_text=patient_text,
                language=language_name
            )
            # Debug: Print semantic analysis results
            if self.semantic_analysis:
                self._log(f"[Pipeline-Fast] Semantic analysis completed: {self.semantic_analysis}")
        else:
            self.semantic_analysis = None

        # Construct pain data
        pain_data = self._construct_pain_ontology(
            llm_entities, 
            ontology_mappings, 
            temporal_pattern,
            locations,
            unmapped
        )
        
        # Apply rules
        recommendations = self.rule_engine.evaluate(pain_data)
        reasoning_chain = self.rule_engine.generate_reasoning_chain(
            pain_data, recommendations, ontology_mappings
        )
        
        # Generate report
        physician_summary = self._generate_summary(pain_data, recommendations, unmapped)
        
        report = ExplainableReport(
            structured_data=pain_data,
            ontology_mapping_trace=ontology_mappings,
            clinical_recommendations=recommendations,
            reasoning_chain=reasoning_chain,
            physician_summary=physician_summary
        )
        
        self._log("[Pipeline-Fast] Execution complete!")
        return report
    
    def _construct_pain_ontology(
        self,
        llm_entities: Dict[str, Any],
        ontology_mappings: List[Dict],
        temporal_pattern: str,
        locations: List[str],
        unmapped_descriptors: List[str]
    ) -> PainOntology:
        """
        Construct PainOntology from mapped data.
        
        Combines LLM extraction with deterministic ontology mapping to populate
        the structured pain model. Prioritizes ontology mapping over LLM extraction
        for medical terms to ensure accuracy.
        
        Args:
            llm_entities: Dictionary of entities extracted by LLM
            ontology_mappings: List of Chinese→English mappings from ontology
            temporal_pattern: Standardized temporal pattern
            locations: List of anatomical locations
            unmapped_descriptors: Pain descriptors that couldn't be mapped
            
        Returns:
            PainOntology instance with all fields populated
        """
        
        # ===== Extract pain type from ontology mappings =====
        pain_types = []
        pain_classification = None
        
        for mapping in ontology_mappings:
            if mapping['dimension'] == 'sensory':
                pain_types.append(mapping['mapped_english'])
                if not pain_classification and mapping.get('pain_type'):
                    pain_classification = mapping['pain_type'].capitalize()
        
        # Construct pain type string
        if pain_types:
            pain_type_str = f"{pain_classification or 'Mixed'} ({', '.join(pain_types)})"
        else:
            # Fallback to LLM extraction if no ontology mapping
            llm_descriptors = llm_entities.get('pain_descriptors', [])
            if llm_descriptors:
                pain_type_str = f"Unclassified ({', '.join(llm_descriptors)})"
            else:
                pain_type_str = "Not clearly specified"
        
        # Add note if unmapped descriptors exist
        if unmapped_descriptors:
            pain_type_str += f" [Unmapped terms: {', '.join(unmapped_descriptors[:3])}]"
        
        # ===== Extract emotion from affective mappings =====
        emotions = [
            mapping['mapped_english'] 
            for mapping in ontology_mappings 
            if mapping['dimension'] == 'affective'
        ]
        
        # Fallback to LLM if no ontology mapping
        if not emotions and llm_entities.get('emotion_keywords'):
            emotions = llm_entities['emotion_keywords']
        
        emotion_str = ', '.join(emotions) if emotions else None
        
        # ===== Construct location string =====
        if locations:
            location_str = ', '.join(locations)
        else:
            location_str = llm_entities.get('location') or 'Not specified'
        
        # ===== Temporal pattern =====
        if not temporal_pattern:
            temporal_pattern = llm_entities.get('temporal_pattern') or "Not specified"
        
        # ===== Intensity (from LLM only, as it's factual extraction) =====
        # Format: "Original text [English translation]" for bilingual display
        intensity_raw = llm_entities.get('intensity', 'Not explicitly stated')
        if intensity_raw and intensity_raw != 'Not explicitly stated' and intensity_raw != 'Not stated':
            # Try to translate if non-English
            intensity_en = translate_to_english_simple(intensity_raw)
            # If translation differs from original, use bilingual format
            if intensity_en != intensity_raw:
                intensity = f"{intensity_raw} [{intensity_en}]"
            else:
                intensity = intensity_raw
        else:
            intensity = intensity_raw
        
        # ===== Functional impact =====
        # Format: "Original text [English translation]" for bilingual display
        functional_impact_raw = llm_entities.get('functional_impact')
        if functional_impact_raw:
            # Try to translate if non-English
            functional_impact_en = translate_to_english_simple(functional_impact_raw)
            # If translation differs from original, use bilingual format
            if functional_impact_en != functional_impact_raw:
                functional_impact = f"{functional_impact_raw} [{functional_impact_en}]"
            else:
                functional_impact = functional_impact_raw
        else:
            functional_impact = None
        
        return PainOntology(
            pain_type=pain_type_str,
            intensity=intensity,
            location=location_str,
            emotion=emotion_str,
            temporal_pattern=temporal_pattern,
            functional_impact=functional_impact
        )
    
    def _generate_summary(
        self,
        pain_data: PainOntology,
        recommendations: List,
        unmapped_descriptors: List[str]
    ) -> str:
        """
        Generate clinical summary using GPT comprehensive report.
        
        Calls GPT to generate bilingual/multilingual clinical report after
        rule-based analysis completes.
        """
        try:
            # Call GPT to generate comprehensive report with BioLORD analysis of ALL terms
            report = generate_comprehensive_report(
                original_text=self.original_patient_text,
                structured_data=pain_data.model_dump(),
                ontology_mappings=self.current_ontology_mappings,
                clinical_recommendations=[rec.model_dump() for rec in recommendations],
                detected_language=self.detected_language or "Chinese",  # Default to Chinese
                semantic_analysis=self.semantic_analysis,  # Legacy: unmapped terms only
                biolord_comprehensive_analysis=getattr(self, 'biolord_comprehensive_analysis', None)  # NEW: All terms BioLORD analysis
            )
            
            # Add MAPPED terms section (direct dictionary matches)
            mapped_count = 0
            if self.current_ontology_mappings:
                # Filter out suggestions, only show exact mappings
                exact_mappings = [m for m in self.current_ontology_mappings 
                                 if not m.get('is_suggestion') and m.get('confidence') != 'suggestion_only']
                
                if exact_mappings:
                    mapped_count = len(exact_mappings)
                    report += "\n\n---\n\n## ✅ Successfully Mapped Pain Descriptors\n\n"
                    report += "*These terms were found directly in the standard medical pain dictionary:*\n\n"
                    
                    for mapping in exact_mappings[:10]:  # Limit display
                        original = mapping.get('original_term', '')
                        english = mapping.get('mapped_english', '')
                        pain_type = mapping.get('pain_type', 'unknown')
                        if original and english:
                            report += f"- **{original}** → {english} (Category: {pain_type})\n"
                    
                    if len(exact_mappings) > 10:
                        report += f"\n*...and {len(exact_mappings) - 10} more mapped terms*\n"
            
            # Add UNMAPPED terms semantic analysis section
            if self.semantic_analysis and self.semantic_analysis.get('unmapped_analysis'):
                report += "\n\n---\n\n## 🔬 Unmapped Terms - Semantic Distance Analysis (AI-Assisted Interpretation)\n\n"
                report += "*The following expressions were NOT found in the standard dictionary. Our AI system performed semantic analysis to suggest possible medical term matches:*\n\n"
                report += f"**Total unmapped terms analyzed:** {len(self.semantic_analysis['unmapped_analysis'])}\n\n"
                
                for item in self.semantic_analysis['unmapped_analysis']:
                    original = item['original_term']  # Patient's native language expression
                    matched_native = item.get('matched_mcgill_native')  # Best matching dictionary term (native lang)
                    standard_english = item.get('matched_standard_english')  # Dictionary's medical English translation
                    matches = item['closest_matches']
                    confidence = item['confidence']
                    lang_code = item.get('language', 'unknown')
                    
                    report += f"### Original Expression: \"{original}\"\n\n"
                    
                    # Show dictionary match (works for all languages: Chinese, Korean, Spanish, Hmong)
                    if matched_native and standard_english:
                        report += f"**Best Dictionary Match:** {matched_native} → **{standard_english}**\n\n"
                    
                    report += f"**Confidence Level:** {confidence.upper()}\n\n"
                    report += "**Top 3 Similar Medical Terms (from dictionary):**\n\n"
                    
                    for i, match in enumerate(matches[:3], 1):
                        similarity_pct = match['score'] * 100
                        native_term = match.get('native_term', match.get('chinese_term', match.get('term', '')))
                        english_term = match.get('english', '')
                        report += f"{i}. **{native_term}** ({english_term}) - Similarity: {match['score']:.3f} ({similarity_pct:.1f}%)\n"
                    
                    # Improved interpretation
                    top_score = matches[0]['score']
                    if top_score > 0.75:
                        strength = "strong"
                    elif top_score > 0.60:
                        strength = "moderate"
                    else:
                        strength = "weak"
                    
                    report += f"\n**Clinical Interpretation:** The semantic analysis shows {strength} similarity "
                    if matched_native and standard_english:
                        report += f"(score: {top_score:.3f}) to the dictionary term '{matched_native}' ({standard_english}). "
                        report += f"This suggests the patient may be experiencing {standard_english.lower()}-type pain sensations.\n\n"
                    else:
                        report += f"(score: {top_score:.3f}) to medical terms in the dictionary.\n\n"
                    report += "---\n\n"
                
                report += "---\n\n**Summary:**\n"
                report += f"- ✅ Mapped (direct dictionary match): {mapped_count} terms\n"
                report += f"- 🔬 Unmapped (AI-assisted analysis): {len(self.semantic_analysis['unmapped_analysis'])} terms\n\n"
                report += "*Note: These are AI-generated suggestions based on semantic embedding similarity. Scores closer to 1.0 indicate stronger semantic relationships. Always verify with clinical assessment.*\n\n"
            
            # Add unmapped term warning
            if unmapped_descriptors:
                report += f"\n\n**⚠️ Note | 注意**: Some pain descriptors could not be automatically mapped: {', '.join(unmapped_descriptors[:3])}. Manual clinical review recommended."
            
            # Ensure Clinical Action Plan is included (add if missing)
            if "⚕️ Clinical Action Plan" not in report and "Clinical Action Plan" not in report:
                report += "\n\n---\n\n## ⚕️ Clinical Action Plan\n\n"
                if recommendations:
                    for i, rec in enumerate(recommendations, 1):
                        report += f"**{i}. {rec.triggered_by_rule}**\n\n"
                        report += f"{rec.recommendation}\n\n"
                        if rec.guideline_reference:
                            report += f"*Reference: {rec.guideline_reference}*\n\n"
                else:
                    report += "Based on the pain assessment:\n\n"
                    report += "1. **Comprehensive Clinical Evaluation**: Conduct detailed pain assessment with standardized scales and physical examination.\n\n"
                    report += "2. **Documentation**: Document all pain characteristics, triggers, and functional impacts for ongoing monitoring.\n\n"
                    report += "3. **Individualized Management**: Develop treatment plan based on complete clinical picture and patient preferences.\n\n"
            
            return report
            
        except Exception as e:
            # If GPT fails, fallback to template generation
            import traceback
            error_details = traceback.format_exc()
            self._log(f"[Warning] GPT report generation failed: {e}")
            self._log(f"[Error Details] {error_details}")
            print(f"\n{'='*80}")
            print(f"[ERROR] Report generation failed!")
            print(f"Exception: {e}")
            print(f"Traceback:\n{error_details}")
            print(f"{'='*80}\n")
            return self._generate_summary_template(pain_data, recommendations, unmapped_descriptors)

    def _generate_summary_template(
        self,
        pain_data: PainOntology,
        recommendations: List,
        unmapped_descriptors: List[str]
    ) -> str:
        """Template-based summary as fallback if GPT fails."""
        
        summary_parts = []
        
        # ===== Patient Presentation =====
        summary_parts.append("**Patient Presentation:**\n")
        
        # Temporal pattern and location
        if pain_data.temporal_pattern != "Not specified":
            summary_parts.append(
                f"Patient presents with {pain_data.temporal_pattern.lower()} "
                f"pain localized to {pain_data.location.lower()}. "
            )
        else:
            summary_parts.append(f"Patient presents with pain in {pain_data.location.lower()}. ")
        
        # Pain characteristics
        if pain_data.pain_type != "Not clearly specified":
            summary_parts.append(
                f"Pain is characterized as {pain_data.pain_type.lower()}. "
            )
        
        # Intensity
        if pain_data.intensity and pain_data.intensity != "Not explicitly stated":
            summary_parts.append(f"Pain intensity: {pain_data.intensity}. ")
        
        # Emotional/functional impact
        if pain_data.emotion:
            summary_parts.append(
                f"Patient reports significant affective distress ({pain_data.emotion.lower()}). "
            )
        
        if pain_data.functional_impact:
            summary_parts.append(
                f"Functional impact noted: {pain_data.functional_impact.lower()}. "
            )
        
        # Unmapped terms warning
        if unmapped_descriptors:
            summary_parts.append(
                f"\n**Note:** Some pain descriptors could not be automatically mapped to "
                f"standard medical terminology ({', '.join(unmapped_descriptors[:3])}). "
                f"Manual clinical review recommended.\n"
            )
        
        # ===== Clinical Recommendations =====
        if recommendations:
            summary_parts.append("\n**Clinical Recommendations:**\n")
            for i, rec in enumerate(recommendations, 1):
                summary_parts.append(f"\n{i}. {rec.recommendation}\n")
                if rec.guideline_reference:
                    summary_parts.append(f"   *Reference: {rec.guideline_reference}*\n")
                summary_parts.append(f"   *Evidence: {rec.evidence}*\n")
        else:
            summary_parts.append(
                "\n**Clinical Recommendations:**\n"
                "Standard pain assessment and management pathway recommended. "
                "Consider detailed clinical interview for further characterization.\n"
            )
        
        return ''.join(summary_parts)
    
    def get_pipeline_info(self) -> Dict[str, Any]:
        """
        Get information about the current pipeline configuration.
        
        Returns:
            Dictionary with pipeline metadata
        """
        return {
            "pipeline_version": "2.0.0",
            "architecture": "Neuro-Symbolic Hybrid (Multilingual)",
            "supported_languages": get_supported_languages(),
            "rule_count": self.rule_engine.get_rule_count(),
            "active_rules": self.rule_engine.get_rule_ids(),
            "ontology_coverage": {
                "total_descriptors": 373,
                "chinese_terms": 88,
                "korean_terms": 116,
                "spanish_terms": 105,
                "hmong_terms": 64,
                "temporal_patterns": 14,
                "anatomical_locations": 21
            }
        }
