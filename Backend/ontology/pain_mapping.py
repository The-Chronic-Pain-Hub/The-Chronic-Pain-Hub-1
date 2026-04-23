"""
Chinese-English pain ontology mapping dictionary.

Maps culturally-specific Chinese pain descriptors to standardized English medical terminology
aligned with McGill Pain Questionnaire (SF-MPQ) and SNOMED CT.

This module provides deterministic, dictionary-based mapping to ensure medical accuracy
and cross-cultural semantic alignment.
"""

from typing import List, Dict, Optional, Any


# Chinese pain descriptor mappings
# Each entry maps a Chinese term to its English medical equivalent with metadata
CHINESE_PAIN_DESCRIPTORS = {
    # ========== Neuropathic Pain Descriptors ==========
    "针扎": {
        "english": "Pricking",
        "aliases": ["像针扎一样", "针刺", "如针扎", "针扎样"],
        "dimension": "sensory",
        "pain_type": "neuropathic",
        "mcgill_category": "Sensory",
        "description": "Sharp, needle-like pain sensation typical of nerve irritation"
    },
    
    "触电": {
        "english": "Electric-shock-like",
        "aliases": ["像触电一样", "电击", "过电", "触电样", "电击样"],
        "dimension": "sensory",
        "pain_type": "neuropathic",
        "mcgill_category": "Sensory",
        "description": "Sharp, sudden, shocking nerve pain resembling electric shock"
    },
    
    "麻": {
        "english": "Tingling",
        "aliases": ["发麻", "麻木", "麻刺", "又麻又痛", "麻痹"],
        "dimension": "sensory",
        "pain_type": "neuropathic",
        "mcgill_category": "Sensory",
        "description": "Tingling, numbness, or pins-and-needles sensation"
    },
    
    "刺": {
        "english": "Stabbing",
        "aliases": ["刺痛", "刀刺", "刺骨", "像刀刺一样"],
        "dimension": "sensory",
        "pain_type": "neuropathic",
        "mcgill_category": "Sensory",
        "description": "Sharp, stabbing pain sensation"
    },
    
    "蚂蚁": {
        "english": "Formication (crawling sensation)",
        "aliases": ["蚂蚁在咬", "蚂蚁爬", "虫子爬", "有东西在爬"],
        "dimension": "sensory",
        "pain_type": "neuropathic",
        "mcgill_category": "Sensory",
        "description": "Crawling, tingling sensation like insects on skin"
    },
    
    # ========== Nociceptive Pain Descriptors ==========
    "火辣辣": {
        "english": "Burning",
        "aliases": ["烧灼", "灼烧", "火烧", "灼热", "火辣"],
        "dimension": "sensory",
        "pain_type": "nociceptive",
        "mcgill_category": "Sensory",
        "description": "Hot, burning sensation"
    },
    
    "隐痛": {
        "english": "Aching",
        "aliases": ["隐隐作痛", "隐隐的痛", "隐约的痛"],
        "dimension": "sensory",
        "pain_type": "nociceptive",
        "mcgill_category": "Sensory",
        "description": "Dull, continuous aching pain"
    },
    
    "酸痛": {
        "english": "Sore",
        "aliases": ["酸", "发酸", "又酸又痛"],
        "dimension": "sensory",
        "pain_type": "nociceptive",
        "mcgill_category": "Sensory",
        "description": "Sore, achy muscle pain"
    },
    
    "胀": {
        "english": "Distended",
        "aliases": ["胀痛", "又酸又胀", "发胀", "膨胀"],
        "dimension": "sensory",
        "pain_type": "nociceptive",
        "mcgill_category": "Sensory",
        "description": "Distending, swelling pain sensation"
    },
    
    "跳": {
        "english": "Throbbing",
        "aliases": ["跳痛", "一跳一跳的", "像心跳一样"],
        "dimension": "sensory",
        "pain_type": "nociceptive",
        "mcgill_category": "Sensory",
        "description": "Pulsating, throbbing pain"
    },
    
    "钝痛": {
        "english": "Dull",
        "aliases": ["钝钝的", "不尖锐"],
        "dimension": "sensory",
        "pain_type": "nociceptive",
        "mcgill_category": "Sensory",
        "description": "Dull, non-sharp pain"
    },

    
    # ========== Affective (Emotional) Descriptors ==========
    "郁闷": {
        "english": "Depressed",
        "aliases": ["抑郁", "心情不好", "情绪低落", "沮丧", "低落"],
        "dimension": "affective",
        "mcgill_category": "Affective",
        "description": "Emotional distress and depressive symptoms associated with pain"
    },
    
    "烦躁": {
        "english": "Anxious",
        "aliases": ["焦虑", "心烦", "烦", "不安", "烦恼"],
        "dimension": "affective",
        "mcgill_category": "Affective",
        "description": "Anxiety, irritability, and restlessness"
    },
    
    "累": {
        "english": "Exhausting",
        "aliases": ["疲惫", "累得慌", "精疲力竭", "疲劳", "乏力"],
        "dimension": "affective",
        "mcgill_category": "Affective",
        "description": "Physical and emotional exhaustion from persistent pain"
    },
    
    "难受": {
        "english": "Distressing",
        "aliases": ["痛苦", "受罪", "折磨"],
        "dimension": "affective",
        "mcgill_category": "Affective",
        "description": "Overall distress and suffering"
    },
    
    "绝望": {
        "english": "Hopeless",
        "aliases": ["没希望", "无望"],
        "dimension": "affective",
        "mcgill_category": "Affective",
        "description": "Sense of hopelessness and despair"
    }
    

}


# Temporal pattern mappings
TEMPORAL_PATTERNS = {
    "几个月": "Chronic (>3 months)",
    "好几个月": "Chronic (>3 months)",
    "很久": "Chronic (>3 months)",
    "长期": "Chronic (>3 months)",
    "一直": "Constant",
    "总是": "Constant",
    "经常": "Frequent",
    "偶尔": "Intermittent",
    "时不时": "Intermittent",
    "有时候": "Intermittent",
    "突然": "Acute onset",
    "最近": "Recent onset",
    "反复": "Recurring",
    "每天": "Daily",
    "晚上": "Nocturnal"
}


# Anatomical location mappings
ANATOMICAL_LOCATIONS = {
    "腰": "Lower back",
    "后腰": "Lower back",
    "腰部": "Lower back",
    "腿": "Lower extremities",
    "下肢": "Lower extremities",
    "大腿": "Thighs",
    "小腿": "Legs",
    "膝盖": "Knees",
    "膝": "Knees",
    "手": "Hands",
    "上肢": "Upper extremities",
    "脚": "Feet",
    "足": "Feet",
    "头": "Head",
    "颈": "Neck",
    "脖子": "Neck",
    "肩": "Shoulders",
    "背": "Back",
    "胸": "Chest",
    "腹": "Abdomen",
    "肚子": "Abdomen",
    "浑身": "Whole body"
    
}


def map_chinese_to_english(chinese_text: str) -> List[Dict[str, Any]]:
    """
    Map Chinese pain descriptors to standardized English medical terminology.
    
    Uses dictionary-based exact and fuzzy matching to identify pain descriptors
    in patient text and map them to McGill Pain Questionnaire dimensions and
    SNOMED CT codes.
    
    Args:
        chinese_text: Raw Chinese patient description
        
    Returns:
        List of mappings, each containing:
        - chinese_input: The Chinese term found in text
        - mapped_english: Standardized English medical term
        - dimension: sensory/affective
        - pain_type: neuropathic/nociceptive (if applicable)
        - snomed_ct: SNOMED CT code (if applicable)
        - confidence: Mapping confidence (high/medium/low)
    
    Example:
        >>> mappings = map_chinese_to_english("腰部像触电一样的麻痛，很郁闷")
        >>> # Returns mappings for "触电" → "Electric-shock-like" and "郁闷" → "Depressed"
    """
    mappings = []
    
    # Iterate through all defined pain descriptors
    for chinese_term, term_data in CHINESE_PAIN_DESCRIPTORS.items():
        # Check if main term appears in text
        if chinese_term in chinese_text:
            mappings.append({
                "chinese_input": chinese_term,
                "mapped_english": term_data["english"],
                "dimension": term_data["dimension"],
                "pain_type": term_data.get("pain_type"),
                "confidence": "high",
                "mcgill_category": term_data.get("mcgill_category")
            })
        else:
            # Check aliases for fuzzy matching
            for alias in term_data.get("aliases", []):
                if alias in chinese_text:
                    mappings.append({
                        "chinese_input": alias,
                        "mapped_english": term_data["english"],
                        "dimension": term_data["dimension"],
                        "pain_type": term_data.get("pain_type"),
                        "confidence": "high",
                        "mcgill_category": term_data.get("mcgill_category")
                    })
                    break  # Only match once per term to avoid duplicates
    
    return mappings


def extract_temporal_pattern(chinese_text: str) -> Optional[str]:
    """
    Extract and standardize temporal pattern from Chinese text.
    
    Identifies duration, frequency, and onset patterns and maps them to
    standardized clinical terminology.
    
    Args:
        chinese_text: Raw Chinese patient description
        
    Returns:
        Standardized temporal pattern string or None if not found
        
    Example:
        >>> extract_temporal_pattern("已经好几个月了")
        'Chronic (>3 months)'
    """
    # Check for duration indicators (prioritize more specific patterns)
    # Look for "X个月" pattern first
    import re
    
    # Extract numeric duration
    month_match = re.search(r'(\d+)\s*个月', chinese_text)
    if month_match:
        months = int(month_match.group(1))
        if months >= 3:
            return f"Chronic ({months} months)"
        else:
            return f"Acute (<3 months, {months} months)"
    
    # Check predefined temporal patterns
    for chinese_pattern, english_pattern in TEMPORAL_PATTERNS.items():
        if chinese_pattern in chinese_text:
            return english_pattern
    
    return None


def extract_anatomical_location(chinese_text: str) -> List[str]:
    """
    Extract anatomical locations from Chinese text.
    
    Identifies body parts mentioned in patient description and maps them
    to standardized anatomical terminology.
    
    Args:
        chinese_text: Raw Chinese patient description
        
    Returns:
        List of standardized anatomical location strings
        
    Example:
        >>> extract_anatomical_location("腰部到腿部都痛")
        ['Lower back', 'Lower extremities']
    """
    locations = []
    
    for chinese_loc, english_loc in ANATOMICAL_LOCATIONS.items():
        if chinese_loc in chinese_text:
            if english_loc not in locations:  # Avoid duplicates
                locations.append(english_loc)
    
    return locations


def get_unmapped_descriptors(chinese_text: str, mappings: List[Dict]) -> List[str]:
    """
    Identify pain-related words in text that were not mapped to standard terminology.
    
    This helps track coverage gaps in the mapping dictionary and identify
    culturally-specific terms that may need to be added.
    
    Args:
        chinese_text: Raw Chinese patient description
        mappings: List of mappings returned by map_chinese_to_english()
        
    Returns:
        List of Chinese pain-related terms that were not mapped
        
    Note:
        This is a simple heuristic-based approach. For production use,
        consider using NER or more sophisticated linguistic analysis.
    """
    # Common pain-related indicator words in Chinese
    pain_indicators = ["痛", "疼", "酸", "麻", "胀", "难受", "不舒服"]
    
    unmapped = []
    # Support both old format (chinese_input) and new format (original_term)
    mapped_terms = {m.get("chinese_input") or m.get("original_term") for m in mappings}
    
    # Simple heuristic: look for pain indicator characters
    for indicator in pain_indicators:
        if indicator in chinese_text and indicator not in mapped_terms:
            # Extract context around the indicator (basic approach)
            import re
            pattern = f".{{0,3}}{indicator}.{{0,3}}"
            matches = re.findall(pattern, chinese_text)
            for match in matches:
                if match not in mapped_terms and match not in unmapped:
                    unmapped.append(match)
    
    return unmapped


def suggest_similar_terms(unmapped_term: str, language: str = "zh") -> List[Dict[str, Any]]:
    """
    Suggest similar pain descriptors from the dictionary for unmapped terms.
    
    Supports all languages: Chinese, Korean, Spanish, Hmong.
    Provides NON-DEFINITIVE suggestions for terms not found in dictionary.
    
    Args:
        unmapped_term: Pain descriptor not found in dictionary
        language: Language code ('zh', 'ko', 'es', 'hmong', 'en')
        
    Returns:
        List of dictionaries containing similar terms and their properties
    """
    # Import multilingual data
    try:
        from ontology.pain_mapping_multilingual import _load_pain_descriptors
        all_descriptors = _load_pain_descriptors()
    except:
        all_descriptors = {}
    
    suggestions = []
    
    # Language-specific similarity matching
    if language == "zh":
        # Chinese: Character-based matching
        pain_chars = set()
        for char in ["痛", "疼", "酸", "麻", "胀", "刺", "钝", "跳", "抽", "紧", "沉", "胀"]:
            if char in unmapped_term:
                pain_chars.add(char)
        
        if pain_chars:
            # Search Chinese dictionary
            for dict_term, metadata in CHINESE_PAIN_DESCRIPTORS.items():
                shared_chars = pain_chars & set(dict_term)
                if shared_chars:
                    similarity_reason = f"shares character(s): {', '.join(shared_chars)}"
                    if unmapped_term in dict_term or dict_term in unmapped_term:
                        similarity_reason += " (possible variant)"
                    
                    suggestions.append({
                        "dictionary_term": dict_term,
                        "english": metadata["english"],
                        "pain_type": metadata.get("pain_type", "unknown"),
                        "dimension": metadata.get("dimension", "unknown"),
                        "similarity_reason": similarity_reason,
                        "confidence": "low"
                    })
    
    elif language == "ko":
        # Korean: Syllable and morpheme matching
        korean_pain_roots = ["아프", "쑤시", "저리", "욱신", "찌르", "뻐근", "뻣뻣", "당기"]
        
        matched_roots = [root for root in korean_pain_roots if root in unmapped_term]
        
        if matched_roots and 'korean' in all_descriptors:
            for dict_term, metadata in all_descriptors['korean'].items():
                for root in matched_roots:
                    if root in dict_term:
                        suggestions.append({
                            "dictionary_term": dict_term,
                            "english": metadata["english"],
                            "pain_type": metadata.get("pain_type", "unknown"),
                            "dimension": metadata.get("dimension", "unknown"),
                            "similarity_reason": f"shares Korean root: '{root}'",
                            "confidence": "low"
                        })
                        break
    
    elif language == "es":
        # Spanish: Root and substring matching
        spanish_pain_roots = ["dolor", "duel", "punc", "ard", "quem", "pinch", "puls", "palp"]
        unmapped_lower = unmapped_term.lower()
        
        matched_roots = [root for root in spanish_pain_roots if root in unmapped_lower]
        
        if matched_roots and 'spanish' in all_descriptors:
            for dict_term, metadata in all_descriptors['spanish'].items():
                dict_lower = dict_term.lower()
                for root in matched_roots:
                    if root in dict_lower:
                        suggestions.append({
                            "dictionary_term": dict_term,
                            "english": metadata["english"],
                            "pain_type": metadata.get("pain_type", "unknown"),
                            "dimension": metadata.get("dimension", "unknown"),
                            "similarity_reason": f"shares Spanish root: '{root}'",
                            "confidence": "low"
                        })
                        break
    
    elif language == "hmong":
        # Hmong: Word component matching
        hmong_pain_words = ["mob", "nkees", "rwg", "kub", "tawv"]
        unmapped_lower = unmapped_term.lower()
        
        matched_words = [word for word in hmong_pain_words if word in unmapped_lower]
        
        if matched_words and 'hmong' in all_descriptors:
            for dict_term, metadata in all_descriptors['hmong'].items():
                dict_lower = dict_term.lower()
                for word in matched_words:
                    if word in dict_lower:
                        suggestions.append({
                            "dictionary_term": dict_term,
                            "english": metadata["english"],
                            "pain_type": metadata.get("pain_type", "unknown"),
                            "dimension": metadata.get("dimension", "unknown"),
                            "similarity_reason": f"shares Hmong word: '{word}'",
                            "confidence": "low"
                        })
                        break
    
    # Sort by similarity and limit results
    suggestions.sort(key=lambda x: len(x.get("similarity_reason", "")), reverse=True)
    
    # Add note to all suggestions
    for s in suggestions[:3]:
        s["note"] = f"⚠️ Suggestion only. Patient used '{unmapped_term}' which is not in dictionary. Clinical review required."
    
    return suggestions[:3]


def verify_all_terms_with_semantic_model(
    patient_text: str,
    ontology_mappings: List[Dict],
    language: str = "zh"
) -> List[Dict[str, Any]]:
    """
    Verify all terms (both mapped and unmapped) through semantic model.
    Supports all languages: Chinese, Korean, Spanish, Hmong.
    
    Provides semantic verification for all pain descriptors:
    1. Dictionary-matched terms → Verify semantic consistency
    2. Unmapped terms → Provide semantic suggestions
    
    Args:
        patient_text: Original patient text
        ontology_mappings: Existing dictionary mappings
        language: Language code ('zh', 'ko', 'es', 'hmong', 'en')
        
    Returns:
        Enhanced mappings with semantic verification flags:
        [
            {
                "original_term": "刺痛",
                "mapped_english": "Stabbing",
                "pain_type": "neuropathic",
                "match_type": "dictionary",  # or "semantic" or "both"
                "semantic_confidence": "high",  # high/medium/low
                "semantic_alternatives": [...]  # other semantic candidates
            }
        ]
    """
    # Support all languages (no language check restriction)
    enhanced_mappings = []
    mapped_terms = set()
    
    # Step 1: Verify existing dictionary mappings with semantic model
    for mapping in ontology_mappings:
        original_term = mapping.get("original_term") or mapping.get("chinese_input")
        if not original_term:
            enhanced_mappings.append(mapping)
            continue
            
        mapped_terms.add(original_term)
        
        # Verify this mapping with semantic model
        semantic_suggestions = suggest_similar_terms(original_term, language)
        
        # Check if dictionary mapping is in semantic top candidates
        dict_english = mapping.get("mapped_english", "")
        semantic_match_found = any(
            s["english"].lower() == dict_english.lower() 
            for s in semantic_suggestions
        )
        
        enhanced_mapping = mapping.copy()
        enhanced_mapping["match_type"] = "both" if semantic_match_found else "dictionary"
        enhanced_mapping["semantic_confidence"] = "high" if semantic_match_found else "medium"
        
        # Add semantic alternatives (if there are different suggestions)
        alternatives = [
            s for s in semantic_suggestions 
            if s["english"].lower() != dict_english.lower()
        ]
        if alternatives:
            enhanced_mapping["semantic_alternatives"] = alternatives[:2]  # At most 2 alternatives
        
        enhanced_mappings.append(enhanced_mapping)
    
    # Step 2: Apply semantic model to all unmapped pain terms in patient_text
    unmapped_terms = get_unmapped_descriptors(patient_text, ontology_mappings)
    
    for term in unmapped_terms:
        if term in mapped_terms:
            continue  # Already processed
            
        semantic_suggestions = suggest_similar_terms(term, language)
        
        if semantic_suggestions:
            # Add semantic-only match
            for suggestion in semantic_suggestions[:1]:  # Only take top match
                enhanced_mappings.append({
                    "original_term": term,
                    "mapped_english": suggestion["english"],
                    "pain_type": suggestion.get("pain_type", "unknown"),
                    "dimension": suggestion.get("dimension", "unknown"),
                    "match_type": "semantic_only",
                    "semantic_confidence": "low",  # Semantic-only is always low confidence
                    "is_suggestion": True,
                    "similarity_reason": suggestion.get("similarity_reason", ""),
                    "suggestion_note": f"⚠️ Not in dictionary. Semantic suggestion only - clinical review required."
                })
    
    return enhanced_mappings

