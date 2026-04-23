"""
Semantic Distance Service (Version 2 - Multilingual)

Uses OpenAI embeddings to calculate semantic similarity between patient's 
unmapped pain expressions and our multilingual medical pain dictionary.

**Improved Architecture (User-Suggested):**
1. Patient expression (any language) → Compare with native language dictionary embeddings
2. Find best matching term in native language dictionary (e.g., Korean "따끔거리다")
3. Use dictionary's standard English translation (e.g., "Pricking")
4. NO GPT translation needed - uses pre-defined medical translations

**Supported Languages:**
- Chinese (中文): 373+ terms from CHINESE_PAIN_DESCRIPTORS
- Korean (한국어): 131+ terms from KOREAN_PAIN_DESCRIPTORS  
- Spanish (Español): 74+ terms from SPANISH_PAIN_DESCRIPTORS
- Hmong: Terms from HMONG_PAIN_DESCRIPTORS
- English: Pass-through (no mapping needed)

Advantages:
- Native language → Native language semantic space (more accurate)
- Medical-grade English translations (standardized)
- Faster (no GPT translation API calls)
- Cost-effective (~$0.02 per 1M tokens for embeddings only)

Cost: ~$0.02 per 1M tokens (text-embedding-3-small)
"""

import numpy as np
from openai import OpenAI
from typing import List, Dict
import os
from ontology.pain_mapping_multilingual import (
    CHINESE_PAIN_DESCRIPTORS,
    KOREAN_PAIN_DESCRIPTORS,
    SPANISH_PAIN_DESCRIPTORS,
    HMONG_PAIN_DESCRIPTORS
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Cache for dictionary embeddings (precomputed at startup)
# Structure: {language_code: {terms: [...], embeddings: [...], metadata: [...]}}
DICTIONARY_EMBEDDINGS_CACHE = {}


def precompute_dictionary_embeddings():
    """
    Precompute embeddings for ALL multilingual pain terms at app startup.
    
    Processes dictionaries for:
    - Chinese (中文): ~373 terms + aliases
    - Korean (한국어): ~131 terms + aliases
    - Spanish (Español): ~74 terms + aliases
    - Hmong: All defined terms
    
    Each language gets its own embedding cache for accurate native-language matching.
    """
    global DICTIONARY_EMBEDDINGS_CACHE
    
    # Language configurations
    language_configs = {
        'zh': {'name': 'Chinese', 'descriptors': CHINESE_PAIN_DESCRIPTORS},
        'ko': {'name': 'Korean', 'descriptors': KOREAN_PAIN_DESCRIPTORS},
        'es': {'name': 'Spanish', 'descriptors': SPANISH_PAIN_DESCRIPTORS},
        'hmong': {'name': 'Hmong', 'descriptors': HMONG_PAIN_DESCRIPTORS}
    }
    
    print(f"[Semantic Distance V2] Precomputing embeddings for {len(language_configs)} languages...")
    
    for lang_code, config in language_configs.items():
        descriptors = config['descriptors']
        lang_name = config['name']
        
        if not descriptors:
            print(f"[Semantic Distance V2]   ⚠️ {lang_name}: No descriptors found, skipping")
            continue
        
        # Extract all terms + aliases from dictionary
        all_terms = []
        term_metadata = []  # Store: term → English translation + metadata
        
        for term_key, metadata in descriptors.items():
            # Add main term
            all_terms.append(term_key)
            term_metadata.append({
                "native_term": term_key,
                "english": metadata.get("english", metadata.get("mapped_english", "Unknown")),
                "pain_type": metadata.get("pain_type", "unknown"),
                "dimension": metadata.get("dimension", "sensory"),
                "is_alias": False
            })
            
            # Add aliases if available
            for alias in metadata.get("aliases", []):
                all_terms.append(alias)
                term_metadata.append({
                    "native_term": alias,
                    "english": metadata.get("english", metadata.get("mapped_english", "Unknown")),
                    "pain_type": metadata.get("pain_type", "unknown"),
                    "dimension": metadata.get("dimension", "sensory"),
                    "is_alias": True,
                    "parent_term": term_key
                })
        
        if not all_terms:
            print(f"[Semantic Distance V2]   ⚠️ {lang_name}: No terms extracted, skipping")
            continue
        
        print(f"[Semantic Distance V2]   {lang_name}: Processing {len(all_terms)} terms...")
        
        # Batch API call to get embeddings for all terms in this language
        try:
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=all_terms
            )
            
            embeddings = [item.embedding for item in response.data]
            
            DICTIONARY_EMBEDDINGS_CACHE[lang_code] = {
                "terms": all_terms,
                "embeddings": embeddings,
                "metadata": term_metadata
            }
            
            print(f"[Semantic Distance V2]   ✓ {lang_name}: Cached {len(all_terms)} term embeddings")
            
        except Exception as e:
            print(f"[Semantic Distance V2]   ❌ {lang_name}: Embedding failed - {e}")
    
    total_terms = sum(len(cache["terms"]) for cache in DICTIONARY_EMBEDDINGS_CACHE.values())
    print(f"[Semantic Distance V2] ✓ Total: Cached {total_terms} terms across {len(DICTIONARY_EMBEDDINGS_CACHE)} languages")


def calculate_semantic_distances(
    unmapped_terms: List[str],
    patient_text: str,
    language: str,
    translated_terms: List[str] = None  # Deprecated parameter (backward compatibility)
) -> Dict:
    """
    Calculate semantic distances for unmapped pain expressions in ANY supported language.
    
    **Multilingual Flow:**
    1. Chinese patient: "像有成千上万只蚂蚁在皮肤下面爬来爬去"
       → Compare with Chinese dictionary → Match "蚂蚁爬" → Return "Formication (crawling)"
    
    2. Korean patient: "허리가 따끔거리듯이 아프다"
       → Compare with Korean dictionary → Match "따끔거리다" → Return "Pricking"
    
    3. Spanish patient: "dolor punzante en la espalda"
       → Compare with Spanish dictionary → Match "punzante" → Return "Stabbing"
    
    Args:
        unmapped_terms: Original pain expressions in patient's native language
        patient_text: Full patient text (for logging)
        language: Detected language name (e.g., "Chinese", "Korean", "Spanish", "Hmong")
        translated_terms: [DEPRECATED] Pre-translated terms (no longer used)
    
    Returns:
        Dictionary with unmapped_analysis containing:
        - original_term: Patient's native language expression
        - matched_native_term: Best matching dictionary term (native language)
        - standard_english: Dictionary's medical English translation
        - closest_matches: Top 3 similar dictionary terms
        - confidence: high/medium/low based on similarity score
        - language: Detected language code
    """
    if not unmapped_terms:
        return None
    
    # Map language names to codes
    language_map = {
        "Chinese": "zh",
        "Korean": "ko",
        "Spanish": "es",
        "Hmong": "hmong",
        "English": "en"
    }
    
    lang_code = language_map.get(language, "en")
    
    # Skip semantic analysis for English (already standardized) or unsupported languages
    if lang_code == "en":
        print(f"[Semantic Distance V2] Skipping - English terms already standardized")
        return None
    
    # Ensure dictionary embeddings are loaded
    if not DICTIONARY_EMBEDDINGS_CACHE:
        precompute_dictionary_embeddings()
    
    # Check if this language is supported
    if lang_code not in DICTIONARY_EMBEDDINGS_CACHE:
        print(f"[Semantic Distance V2] ⚠️ Language '{language}' ({lang_code}) not supported - no dictionary available")
        return None
    
    lang_cache = DICTIONARY_EMBEDDINGS_CACHE[lang_code]
    
    print(f"[Semantic Distance V2] Analyzing {len(unmapped_terms)} {language} unmapped terms...")
    print(f"[Semantic Distance V2]   Using {language} dictionary: {len(lang_cache['terms'])} terms")
    
    # Get embeddings for patient's unmapped terms (in their native language)
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=unmapped_terms
    )
    unmapped_embeddings = [item.embedding for item in response.data]
    
    # Calculate similarities between patient terms and dictionary
    results = []
    for i, patient_term in enumerate(unmapped_terms):
        similarities = []
        
        # Compare with all dictionary terms in this language
        for j, dict_data in enumerate(lang_cache["metadata"]):
            score = cosine_similarity(
                unmapped_embeddings[i],
                lang_cache["embeddings"][j]
            )
            similarities.append({
                "native_term": dict_data["native_term"],
                "english": dict_data["english"],
                "pain_type": dict_data["pain_type"],
                "dimension": dict_data["dimension"],
                "score": round(score, 3)
            })
        
        # Get Top 3 matches
        top_matches = sorted(similarities, key=lambda x: x['score'], reverse=True)[:3]
        
        # Determine confidence level
        best_score = top_matches[0]['score']
        if best_score > 0.75:
            confidence = "high"
        elif best_score > 0.60:
            confidence = "medium"
        else:
            confidence = "low"
        
        # Log best match
        print(f"[Semantic Distance V2]   '{patient_term[:50]}' → '{top_matches[0]['native_term']}' "
              f"({top_matches[0]['english']}) [score: {best_score:.3f}]")
        
        results.append({
            "original_term": patient_term,  # Patient's native language expression
            "matched_native_term": top_matches[0]['native_term'],  # Best dictionary term (native)
            "standard_english": top_matches[0]['english'],  # Medical English translation
            "closest_matches": top_matches,  # Top 3 for display
            "confidence": confidence,
            "language": lang_code
        })
    
    return {"unmapped_analysis": results}


def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
