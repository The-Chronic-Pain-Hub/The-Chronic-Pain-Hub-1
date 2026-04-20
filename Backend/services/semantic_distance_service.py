from openai import OpenAI
import numpy as np
from typing import List, Dict
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Embed the dictionary terms once and cache them for future use
DICTIONARY_EMBEDDINGS_CACHE = None

def get_standard_pain_terms():
    """Return a list of standard pain terms for semantic distance calculation."""
    return [
        "burning", "tingling", "shooting", "stabbing", "aching", 
        "throbbing", "sharp", "dull", "cramping", "electric-shock-like",
        "pricking", "numb", "crawling", "tight", "heavy"
    ]

def precompute_dictionary_embeddings():
    """Precompute and cache dictionary embeddings at system startup."""
    global DICTIONARY_EMBEDDINGS_CACHE
    
    terms = get_standard_pain_terms()
    response = client.embeddings.create(
        model="text-embedding-3-small",  # inexpensive
        input=terms
    )
    
    DICTIONARY_EMBEDDINGS_CACHE = {
        "terms": terms,
        "embeddings": [item.embedding for item in response.data]
    }
    print(f"[Init] Cached {len(terms)} dictionary embeddings")

def calculate_semantic_distances(
    unmapped_terms: List[str],
    patient_text: str,
    language: str,
    translated_terms: List[str] = None  # Pre-translated terms (optional)
) -> Dict:
    """
    Calculate semantic distances only for unmapped terms.
    
    Args:
        unmapped_terms: Original pain expressions (any language)
        patient_text: Full patient text (for context)
        language: Detected language name
        translated_terms: Optional pre-translated English versions of unmapped_terms
                         If provided, will use these directly instead of translating again
    
    Returns:
        Dictionary with unmapped_analysis containing similarity scores
    """
    if not unmapped_terms:
        return None
    
    # Ensure dictionary embeddings are loaded
    if DICTIONARY_EMBEDDINGS_CACHE is None:
        precompute_dictionary_embeddings()
    
    # Use pre-translated terms if provided, otherwise translate now
    if translated_terms and len(translated_terms) == len(unmapped_terms):
        print(f"[Semantic Distance] Using pre-translated terms")
        terms_to_embed = translated_terms
    elif language != "English":
        print(f"[Semantic Distance] Translating {len(unmapped_terms)} non-English terms to English...")
        translated_terms = []
        for term in unmapped_terms:
            try:
                # Quick translation to English for semantic matching
                response = client.chat.completions.create(
                    model="gpt-4o-mini",  # Use faster model for translation
                    messages=[
                        {"role": "system", "content": "Translate pain descriptions to concise medical English. Output ONLY the translation, no explanations."},
                        {"role": "user", "content": f"Translate to medical English: {term}"}
                    ],
                    temperature=0.1,
                    max_tokens=50
                )
                translated = response.choices[0].message.content.strip().strip('"\'')
                translated_terms.append(translated)
                print(f"[Semantic Distance]   '{term[:40]}...' → '{translated}'")
            except Exception as e:
                print(f"[Semantic Distance] Translation failed for '{term[:40]}...', using original")
                translated_terms.append(term)
        
        terms_to_embed = translated_terms
    else:
        terms_to_embed = unmapped_terms
    
    # Get embeddings for (translated) unmapped terms
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=terms_to_embed
    )
    unmapped_embeddings = [item.embedding for item in response.data]
    
    # Calculate similarities
    results = []
    for i, original_term in enumerate(unmapped_terms):
        similarities = []
        for j, dict_term in enumerate(DICTIONARY_EMBEDDINGS_CACHE["terms"]):
            score = cosine_similarity(
                unmapped_embeddings[i],
                DICTIONARY_EMBEDDINGS_CACHE["embeddings"][j]
            )
            similarities.append({"term": dict_term, "score": round(score, 3)})
        
        # Top 3
        top_matches = sorted(similarities, key=lambda x: x['score'], reverse=True)[:3]
        confidence = "high" if top_matches[0]['score'] > 0.75 else \
                     "medium" if top_matches[0]['score'] > 0.60 else "low"
        
        results.append({
            "original_term": original_term,
            "translated_term": terms_to_embed[i] if language != "English" else None,
            "closest_matches": top_matches,
            "confidence": confidence
        })
    
    return {"unmapped_analysis": results}

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))