"""
Multilingual pain ontology mapping dictionary.

Extends the Chinese-English mapping to support Korean, Spanish, and Hmong languages.
Maps culturally-specific pain descriptors to standardized English medical terminology
aligned with McGill Pain Questionnaire (SF-MPQ) and SNOMED CT.

Supported Languages:
- Chinese (Simplified)
- Korean (Hangul)
- Spanish (Castilian)
- Hmong

This module provides deterministic, dictionary-based mapping to ensure medical accuracy
and cross-cultural semantic alignment.
"""

import json
import os
import sys
from typing import List, Dict, Optional, Any

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.language_detector import detect_language, LanguageCode

# Load multilingual pain descriptors from JSON
def _load_pain_descriptors():
    """Load pain descriptors from JSON file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, '..', 'scripts', 'multilingual_pain_data.json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def _extract_core_terms(term: str, language: str) -> List[str]:
    """
    Extract core pain descriptor terms to enable fuzzy matching across all languages.
    
    Handles linguistic variations:
    - Chinese: Removes suffixes like 'de-tong', 'de-teng', 'de-ganjue'
    - Korean: Removes verb endings like 'hada', 'apeuda'
    - Spanish: Extracts root words, handles verb forms
    - Hmong: Splits compound words
    
    Args:
        term: Original term from ontology dictionary
        language: Language code ('zh', 'ko', 'es', 'hmong', 'en')
        
    Returns:
        List of core term variants (including original)
        
    Example:
        >>> _extract_core_terms("yi-chou-yi-chou-de-tong", "zh")
        ['yi-chou-yi-chou', 'yi-chou-yi-chou-de-tong']
        >>> _extract_core_terms("punzante", "es")
        ['punzante', 'punz']  # root form
    """
    cores = []
    
    if language == 'zh':  # Chinese
        # Remove common pain-related suffixes to extract core descriptor
        suffixes = ['的痛', '的疼', '的感觉', '痛', '疼', '的']
        core = term
        
        for suffix in suffixes:
            if core.endswith(suffix) and len(core) > len(suffix):
                core = core[:-len(suffix)]
                cores.append(core)
                break
        
        cores.append(term)  # Also keep original term for exact matching
        
    elif language == 'ko':  # Korean
        # Handle Korean verb conjugations and descriptive forms
        if term.endswith('하다') and len(term) > 2:
            cores.append(term[:-2])
        elif term.endswith('아프다') and len(term) > 3:
            cores.append(term[:-3])
        elif term.endswith('듯') and len(term) > 2:
            cores.append(term[:-2])
        cores.append(term)
        
    elif language == 'es':  # Spanish
        # Handle common Spanish suffixes and verb forms
        # Examples: "punzante" → "punz", "ardiente" → "ardi"
        spanish_suffixes = ['ante', 'ente', 'ción', 'miento', 'oso', 'osa']
        core = term.lower()
        
        for suffix in spanish_suffixes:
            if core.endswith(suffix) and len(core) > len(suffix) + 3:
                cores.append(core[:-len(suffix)])
                break
        
        # Also try matching first 4+ characters for root
        if len(term) >= 4:
            cores.append(term[:4])
        
        cores.append(term)
        
    elif language == 'hmong':  # Hmong
        # Hmong often uses compound words separated by spaces
        # Split and try individual words too
        if ' ' in term:
            words = term.split()
            cores.extend(words)  # Add individual words
        cores.append(term)  # Keep full phrase
        
    else:  # English - keep as is
        cores.append(term)
    
    return list(set(cores))  # Remove duplicates

# Load data at module level
_MULTILINGUAL_DATA = _load_pain_descriptors()

# Flatten the multilingual data for easier access
# Structure: {language: {term: {english, dimension, pain_type, ...}}}
KOREAN_PAIN_DESCRIPTORS = {}
for category in ['neuropathic', 'nociceptive', 'affective']:
    for term, data in _MULTILINGUAL_DATA['korean'].get(category, {}).items():
        KOREAN_PAIN_DESCRIPTORS[term] = {
            **data,
            'pain_type': category if category != 'affective' else None,
            'dimension': 'affective' if category == 'affective' else 'sensory'
        }

SPANISH_PAIN_DESCRIPTORS = {}
for category in ['neuropathic', 'nociceptive', 'affective']:
    for term, data in _MULTILINGUAL_DATA['spanish'].get(category, {}).items():
        SPANISH_PAIN_DESCRIPTORS[term] = {
            **data,
            'pain_type': category if category != 'affective' else None,
            'dimension': 'affective' if category == 'affective' else 'sensory'
        }

HMONG_PAIN_DESCRIPTORS = {}
for category in ['neuropathic', 'nociceptive', 'affective']:
    for term, data in _MULTILINGUAL_DATA['hmong'].get(category, {}).items():
        HMONG_PAIN_DESCRIPTORS[term] = {
            **data,
            'pain_type': category if category != 'affective' else None,
            'dimension': 'affective' if category == 'affective' else 'sensory'
        }

CHINESE_PAIN_DESCRIPTORS = {}
for category in ['neuropathic', 'nociceptive', 'affective']:
    for term, data in _MULTILINGUAL_DATA['chinese'].get(category, {}).items():
        CHINESE_PAIN_DESCRIPTORS[term] = {
            **data,
            'pain_type': category if category != 'affective' else None,
            'dimension': 'affective' if category == 'affective' else 'sensory'
        }

# Map language codes to descriptor dictionaries
LANGUAGE_DESCRIPTORS = {
    'zh': CHINESE_PAIN_DESCRIPTORS,
    'ko': KOREAN_PAIN_DESCRIPTORS,
    'es': SPANISH_PAIN_DESCRIPTORS,
    'hmong': HMONG_PAIN_DESCRIPTORS,
    'en': {}  # English input doesn't need translation
}


def map_multilingual_to_english(
    text: str, 
    language: Optional[LanguageCode] = None
) -> List[Dict[str, Any]]:
    """
    Map multilingual pain descriptors to standardized English medical terminology.
    
    Supports Chinese, Korean, Spanish, Hmong, and English input.
    Uses dictionary-based exact matching to identify pain descriptors
    and map them to McGill Pain Questionnaire dimensions.
    
    Args:
        text: Raw patient description in any supported language
        language: Language code ('zh', 'ko', 'es', 'hmong', 'en'). 
                 If None, will auto-detect from text.
        
    Returns:
        List of mappings, each containing:
        - original_term: The term found in text
        - mapped_english: Standardized English medical term
        - dimension: sensory/affective
        - pain_type: neuropathic/nociceptive (if applicable)
        - confidence: Mapping confidence (high/medium/low)
        - detected_language: The detected or specified language
    
    Example:
        >>> # Chinese input
        >>> mappings = map_multilingual_to_english("I have burning pain")
        >>> # Returns mapping for "burning pain" → "burning"
        
        >>> # Korean input
        >>> mappings = map_multilingual_to_english("허리가 따끔거리듯이 아프다")
        >>> # Returns mapping for "따끔거리다" → "sting"
    """
    # Auto-detect language if not specified
    if language is None:
        language = detect_language(text)
    
    # Get appropriate descriptor dictionary
    descriptors = LANGUAGE_DESCRIPTORS.get(language, {})
    
    if not descriptors:
        # If language not supported or English input
        return [{
            "original_term": text,
            "mapped_english": text,  # Pass through for English
            "dimension": "unknown",
            "pain_type": None,
            "confidence": "low",
            "detected_language": language
        }]
    
    mappings = []
    
    # Iterate through all defined pain descriptors for this language
    for term, term_data in descriptors.items():
        # Extract core terms for fuzzy matching
        core_terms = _extract_core_terms(term, language)
        
        # Try to match any core term variant
        matched_core = None
        for core in core_terms:
            # For Chinese, allow single character matches (麻, 疼, 痛, 酸, etc.)
            # For other languages, require at least 2 characters to avoid false positives
            min_length = 1 if language == 'zh' else 2
            if core in text and len(core) >= min_length:
                matched_core = core
                break
        
        if matched_core:
            # Determine confidence based on match type
            confidence = "high" if matched_core == term else "medium"
            
            mappings.append({
                "original_term": term,  # Original ontology term
                "matched_text": matched_core,  # What actually matched in user input
                "mapped_english": term_data["english"],
                "dimension": term_data["dimension"],
                "pain_type": term_data.get("pain_type"),
                "confidence": confidence,
                "mcgill_dimension": term_data.get("mcgill_dimension", "sensory"),
                "detected_language": language
            })
    
    return mappings


def get_supported_languages() -> List[str]:
    """
    Get list of all supported languages.
    
    Returns:
        List of language codes
    """
    return ['zh', 'ko', 'es', 'hmong', 'en']


def get_descriptor_count(language: LanguageCode) -> int:
    """
    Get the number of pain descriptors available for a language.
    
    Args:
        language: Language code
        
    Returns:
        Number of descriptors
    """
    return len(LANGUAGE_DESCRIPTORS.get(language, {}))


# Re-export temporal and anatomical mappings from original module
# These are language-agnostic or can be expanded in the future
try:
    from ontology.pain_mapping import (
        TEMPORAL_PATTERNS,
        ANATOMICAL_LOCATIONS,
        extract_temporal_pattern,
        extract_anatomical_location
    )
except ImportError:
    # Fallback if running as standalone
    from pain_mapping import (
        TEMPORAL_PATTERNS,
        ANATOMICAL_LOCATIONS,
        extract_temporal_pattern,
        extract_anatomical_location
    )


if __name__ == '__main__':
    # Test multilingual mapping
    test_cases = [
        ("我有火辣辣的疼痛", "zh"),
        ("허리가 따끔거리듯이 아프다", "ko"),
        ("Tengo un dolor agudo", "es"),
        ("Kuv mob mob heev", "hmong"),
    ]
    
    print("Multilingual Pain Mapping Tests:")
    print("=" * 70)
    
    for text, expected_lang in test_cases:
        print(f"\nText: {text}")
        print(f"Expected language: {expected_lang}")
        
        mappings = map_multilingual_to_english(text)
        
        if mappings:
            print(f"Mappings found: {len(mappings)}")
            for m in mappings:
                print(f"  - {m['original_term']} → {m['mapped_english']} ({m['pain_type']})")
                print(f"    Language: {m['detected_language']}, Confidence: {m['confidence']}")
        else:
            print("  No mappings found")
