import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyzePainDescription(text: str) ->dict:
    
    system_prompt = """You are an expert Medical Anthropologist specializing in cross-cultural pain expression.

    Your task is to analyze a patient's transcript by decomposing it into FOUR analytical layers, and then output a structured JSON representation.

    ⚠️ Constraints:
    - Do NOT act as a medical doctor or provide diagnosis.
    - Do NOT infer beyond the given transcript.
    - If uncertain, explicitly state "unknown" or explain uncertainty.
    - Output MUST be valid JSON only. No extra text.

    ---

    ### Analytical Framework (MANDATORY)

    You MUST analyze the transcript in the following four layers:

    1. Linguistic Layer  
    - Provide a literal translation preserving the patient's original wording and meaning.  
    - Do NOT interpret or simplify.

    2. Cultural-Semantic Layer  
    - Identify culturally specific metaphors or expressions.  
    - Explain what they mean in plain English.  
    - Preserve original language for reference.

    3. Clinical Abstraction Layer  
    - Map the narrative into structured pain descriptors:
    - sensory qualities (e.g., sharp, dull)
    - affective qualities (e.g., tiring, distressing)
    - temporal pattern (e.g., intermittent, constant)
    - possible body location (if mentioned)
    - If unclear, mark as "unknown"

    4. Psychosocial Layer  
    - Identify:
    - emotional distress
    - under-reporting (stoicism)
    - communication risks
    - Base ONLY on text evidence (no guessing)

    ---

    ### Output JSON Schema (STRICT)

    {
    "literal_translation": "...",
    "metaphor_mapping": [
        {
        "original_phrase": "...",
        "language": "...",
        "literal_meaning": "...",
        "interpreted_meaning": "..."
        }
    ],
    "clinical_abstraction": {
        "sensory": [],
        "affective": [],
        "temporal_pattern": "",
        "body_location": "",
        "intensity_estimate": ""
    },
    "psychological_and_stoicism_flags": {
        "underreporting_risk": true,
        "emotional_distress": true,
        "communication_risk": "low",
        "notes": ""
    },
    "physician_action_note": ""
    }"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-5.2",  # Use gpt-5.2 for the latest features
            messages=[
                {"role": "system", "content": system_prompt + "\n\n**CRITICAL**: Your response must be ONLY valid JSON. No additional text before or after the JSON."},
                {"role": "user", "content": text}
            ],
            temperature=0.1  # Low temperature for consistency
        )
        
        analysis = json.loads(response.choices[0].message.content)
        return analysis
    
    except Exception as e:
        raise Exception(f"Error analyzing pain description: {str(e)}")


def match_pain_terms_from_vocabulary(text: str, vocabulary: list, language: str = "Chinese") -> dict:
    """
    Match pain terms from a provided vocabulary list in the patient's text.
    
    This replaces the old entity extraction approach. Instead of asking LLM to extract terms,
    we provide a curated vocabulary and ask it to identify which terms are present.
    
    Benefits:
    - No hallucination (LLM chooses from given list)
    - No unmapped terms (all terms are in dictionary)
    - Language-specific vocabulary reduces token usage
    - Translation handled by dictionary (100% accurate)
    
    Args:
        text: Patient's pain description
        vocabulary: List of pain terms in patient's language (from our dictionary)
        language: Language name for context
        
    Returns:
        Dictionary with:
        - matched_terms: List of terms from vocabulary found in text
        - location: Body part mentioned
        - duration_phrase: Time expression
        - intensity: Pain intensity if stated
        - emotion_keywords: Emotional words
        - functional_impact: Activity limitations
        
    Example:
        >>> vocab = ["火辣辣的疼", "麻的", "刺痛", "酸痛"]
        >>> result = match_pain_terms_from_vocabulary("腿火辣辣的疼，还有点麻", vocab, "Chinese")
        >>> # Returns: {"matched_terms": ["火辣辣的疼", "麻的"], ...}
    """
    
    # Format vocabulary for prompt (limit to prevent token overflow)
    vocab_str = "\n".join([f"  - {term}" for term in vocabulary[:200]])  # Max 200 terms
    
    system_prompt = f"""You are a medical term matcher for {language} pain descriptions.

**YOUR TASK**: Identify which pain terms from the provided vocabulary appear in the patient's text.

**VOCABULARY** (pain descriptors in {language}):
{vocab_str}

**MATCHING RULES**:
1. **Exact and Fuzzy Matching ONLY**:
   - Exact: If patient says "火辣辣的疼" and it's in vocabulary → MATCH ✅
   - Fuzzy: If patient says "火辣辣的" or "有点麻", match "火辣辣的疼" or "麻的" ✅
   - Core matching: "麻" can match "麻的", "一抽一抽" can match "一抽一抽的痛"

2. **CRITICAL - NO INTERPRETATION**:
   - ❌ DO NOT interpret metaphors (e.g., "蚂蚁在爬" should NOT match "痒的" even if it sounds itchy)
   - ❌ DO NOT infer meaning (e.g., "像被火烧" should NOT match "火辣辣的" unless text contains "火辣")
   - ❌ DO NOT translate descriptions to medical terms
   - ✅ ONLY match if the ACTUAL WORDS appear in text (with fuzzy tolerance for suffixes)

3. **What to Match**:
   - Pain quality words that LITERALLY appear in text
   - DO NOT match: connectors (还有, 而且), fillers (那个, 嗯), modifiers alone (有点, 很)

3. **Additional Extraction** (structured fields):
   - location: Body part (腿, 腰, knee, back, etc.)
   - duration_phrase: Time (四个月, 3 months, 一周)
   - intensity: Numeric (0-10) or qualitative if clearly stated
   - emotion_keywords: Emotional words (郁闷, depressed, 害怕)
   - functional_impact: Activity limitations (睡不着, can't walk, 影响工作)

**OUTPUT FORMAT** (JSON only):
{{
  "matched_terms": ["term1 from vocabulary", "term2 from vocabulary"],
  "location": "body part or 'Not stated'",
  "duration_phrase": "time phrase or 'Not stated'",
  "intensity": "intensity or 'Not stated'",
  "emotion_keywords": ["emotion1", "emotion2"],
  "functional_impact": "impact or null"
}}

**EXAMPLES**:

Example 1:
Input: "我的腿火辣辣的疼，还有点麻"
Vocabulary contains: ["火辣辣的疼", "麻的", "刺痛"]
Output: {{
  "matched_terms": ["火辣辣的疼", "麻的"],
  "location": "腿",
  "duration_phrase": "Not stated",
  "intensity": "Not stated",
  "emotion_keywords": [],
  "functional_impact": null
}}

Example 2:
Input: "腰部到腿部触电一样麻痛，四个月了，睡不着，很郁闷"
Vocabulary contains: ["触电一样", "麻痛", "郁闷"]
Output: {{
  "matched_terms": ["触电一样", "麻痛"],
  "location": "腰部到腿部",
  "duration_phrase": "四个月",
  "intensity": "Not stated",
  "emotion_keywords": ["郁闷"],
  "functional_impact": "睡不着"
}}

Example 3 (IMPORTANT - NO INTERPRETATION):
Input: "腿部火辣辣的疼，好像浑身有蚂蚁在爬"
Vocabulary contains: ["火辣辣的疼", "麻的", "痒的", "刺痛"]
Output: {{
  "matched_terms": ["火辣辣的疼"],
  "location": "腿部",
  "duration_phrase": "Not stated",
  "intensity": "Not stated",
  "emotion_keywords": [],
  "functional_impact": null
}}
NOTE: "蚂蚁在爬" is a metaphor describing sensation, but "蚂蚁" does not appear in vocabulary.
DO NOT match "痒的" even though ants crawling sounds itchy - no literal word match!
The metaphor "蚂蚁在爬" will be handled separately as an unmapped unique description.
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-5.2",
            messages=[
                {"role": "system", "content": system_prompt + "\n\n**CRITICAL**: Return ONLY valid JSON. No extra text."},
                {"role": "user", "content": text}
            ],
            temperature=0.1
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    
    except Exception as e:
        # Fallback: return empty matches
        return {
            "matched_terms": [],
            "location": "Not stated",
            "duration_phrase": "Not stated",
            "intensity": "Not stated",
            "emotion_keywords": [],
            "functional_impact": None
        }


def extract_pain_entities_constrained(text: str) -> dict:
    """
    LLM-based Named Entity Recognition for pain descriptions.
    
    STRICT CONSTRAINTS:
    - ONLY extract entities present in text
    - NO medical reasoning or diagnosis
    - NO speculation beyond explicit patient statements
    - Output must conform to predefined fields
    
    This function is part of the neuro-symbolic architecture where LLM is used
    ONLY for narrow-scope entity extraction, not clinical decision-making.
    
    Args:
        text: Raw patient pain description (Chinese or multilingual)
        
    Returns:
        Dictionary with extracted entities (not clinical conclusions)
        
    Example:
        >>> entities = extract_pain_entities_constrained("Electric shock-like pain in lower back for 4 months")
        >>> # Returns: {"pain_descriptors": ["electric shock-like"], "location": "lower back", ...}
    """
    
    system_prompt = """You are a medical NER (Named Entity Recognition) system.

**YOUR ONLY TASK**: Extract factual entities from patient text.

**STRICT RULES**:
1. ONLY extract information explicitly stated in the text
2. DO NOT make medical diagnoses or clinical interpretations
3. DO NOT infer pain type classifications (e.g., neuropathic vs nociceptive)
4. DO NOT add medical reasoning or recommendations
5. Mark fields as "Not stated" if not explicitly mentioned

**WHAT TO EXTRACT**:
- **location**: Anatomical body parts mentioned (腿, 腰, knee, back, etc.)
- **duration_phrase**: Time expressions (四个月, 3 months, 一周, etc.)
- **intensity**: Numeric scores (0-10) or qualitative terms if clearly stated
- **emotion_keywords**: Emotional words (郁闷, depressed, 害怕, anxious, etc.)
- **functional_impact**: Activity limitations (睡不着, can't walk, 影响工作, etc.)
- **pain_descriptors**: OPTIONAL - only extract if patient uses vivid/unique descriptions not in standard medical terminology

**NOTE ON pain_descriptors**: 
  • Our system has a comprehensive pain term dictionary (152 Chinese terms, 131 Korean, 74 Spanish)
  • Dictionary matching works directly on original text - no extraction needed for standard terms
  • ONLY extract pain_descriptors if patient uses creative/unique expressions like:
    - "像被火烧一样" (creative metaphor)
    - "说不出来的难受" (hard to describe)
    - "怪怪的感觉" (unusual sensation)
  • For standard terms like "火辣辣的疼", "触电一样", "麻" - leave pain_descriptors EMPTY
  • Dictionary will find them automatically

**PROHIBITED**:
- Medical diagnoses
- Pain classification
- Clinical interpretations
- Recommendations
- Inferences beyond stated text

**OUTPUT FORMAT** (JSON only):
{
  "pain_descriptors": [],  // Usually EMPTY - dictionary handles standard terms
  "location": "anatomical location or 'Not stated'",
  "duration_phrase": "exact time phrase or 'Not stated'",
  "intensity": "numeric value or qualitative term if stated, else 'Not stated'",
  "emotion_keywords": ["emotional words patient used"],
  "functional_impact": "impact on activities if mentioned, else null"
}

**EXAMPLE 1** (Chinese - standard terms, pain_descriptors EMPTY):
Input: "我的腿火辣辣的疼，还有点麻"
Output: {
  "pain_descriptors": [],
  "location": "腿",
  "duration_phrase": "Not stated",
  "intensity": "Not stated",
  "emotion_keywords": [],
  "functional_impact": null
}
Note: "火辣辣的疼" and "麻" are in dictionary - no need to extract

**EXAMPLE 2** (Chinese - extract only unique expressions):
Input: "腰部到腿部说不出来的难受感觉，四个月了，晚上睡不着，心情很郁闷"
Output: {
  "pain_descriptors": ["说不出来的难受感觉"],
  "location": "腰部到腿部",
  "duration_phrase": "四个月",
  "intensity": "Not stated",
  "emotion_keywords": ["郁闷"],
  "functional_impact": "晚上睡不着"
}
Note: "说不出来的难受感觉" is unique/creative - extract it

**EXAMPLE 3** (English - focus on structure):
Input: "My lower back has been aching for 3 months, I'm exhausted"
Output: {
  "pain_descriptors": [],
  "location": "lower back",
  "duration_phrase": "3 months",
  "intensity": "Not stated",
  "emotion_keywords": ["exhausted"],
  "functional_impact": null
}
Note: "aching" is standard - dictionary handles it
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-5.2",  # Use gpt-5.2 for the latest features
            messages=[
                {"role": "system", "content": system_prompt + "\n\n**CRITICAL**: Your response must be ONLY valid JSON. No additional text before or after the JSON."},
                {"role": "user", "content": text}
            ],
            temperature=0.1  # Low temperature for consistency
        )
        
        entities = json.loads(response.choices[0].message.content)
        return entities
    
    except Exception as e:
        raise Exception(f"Error in LLM entity extraction: {str(e)}")


def normalize_transcription(text: str, language: str = "Chinese") -> dict:
    """
    Normalize speech-to-text transcription using LLM to correct errors and standardize expressions.
    
    This preprocessing step improves ontology matching accuracy by:
    1. Correcting common Whisper transcription errors
    2. Standardizing colloquial/oral expressions to medical terminology
    3. Fixing incomplete grammar while preserving original meaning
    4. Normalizing pain descriptors to match ontology terms
    
    Args:
        text: Original transcription from Whisper
        language: Patient's language (Chinese, Korean, Spanish, Hmong, English)
        
    Returns:
        Dictionary with:
        - original: Original transcription
        - normalized: Cleaned and standardized text
        - corrections: List of changes made (for transparency)
        
    Example:
        >>> result = normalize_transcription("Leg... uh... burning really badly", "English")
        >>> # Returns: {
        >>>   "original": "Leg... uh... burning really badly",
        >>>   "normalized": "Leg burning pain",
        >>>   "corrections": ["removed filler words", "standardized expression"]
        >>> }
    """
    
    system_prompt = f"""You are a medical transcription normalization expert for {language} pain descriptions.

**YOUR TASK**: Clean and standardize speech-to-text transcription while preserving the patient's original pain descriptors.

**NORMALIZATION RULES**:

1. **Fix Transcription Errors**:
   - Correct common Whisper errors (homophones, misheard words)
   - Examples:
     * Chinese: "一揪一揪" → "一抽一抽" (throbbing)
     * Korean: "따금거리다" → "따끔거리다" (stinging)
     * Spanish: "quemasón" → "quemazón" (burning)
   
   **SPECIAL: Traditional Chinese → Simplified Chinese Conversion**:
   - Whisper may output Traditional Chinese based on speaker accent (Taiwan/Hong Kong)
   - Our pain dictionary uses ONLY Simplified Chinese - conversion is REQUIRED
   - Convert Traditional characters to Simplified:
     * 還 → 还, 點 → 点, 個 → 个, 頭 → 头, 麻 → 麻 (already same)
     * 癢 → 痒, 脹 → 胀, 緊 → 紧, 軟 → 软, 腫 → 肿
     * 鬱悶 → 郁闷, 難受 → 难受, 嚴重 → 严重
   - Examples:
     * "我的腿火辣辣的疼，還有點麻" → "我的腿火辣辣的疼，还有点麻"
     * "頭很痛" → "头很痛"
     * "感覺很難受" → "感觉很难受"

2. **Standardize Pain Descriptors**:
   - Keep vivid pain terms intact (these are medically valuable)
   - Convert colloquial to standard forms:
     * Chinese: "疼得不行" → "剧烈疼痛"
     * Korean: "너무 아파" → "심한 통증"
     * Spanish: "me duele muchísimo" → "dolor intenso"

3. **Clean Up Grammar**:
   - Remove filler words ("那个", "嗯", "uh", "like")
   - Complete incomplete sentences
   - Fix word order errors
   - But DO NOT change pain descriptors
    
4. **Preserve Original Meaning**:
   - DO NOT add medical interpretations
   - DO NOT change the severity described
   - DO NOT invent information not in original text

5. **Standardize Body Part Names**:
   - Chinese: "腿" → "腿部", "肚子" → "腹部"
   - Keep other details as-is

**OUTPUT FORMAT** (JSON only):
{{
  "original": "original transcription text",
  "normalized": "cleaned and standardized text",
  "corrections": [
    "fix: description of change made",
    "standardize: description of change"
  ],
  "confidence": "high/medium/low (based on # of corrections)"
}}

**EXAMPLES**:

Input: "腿那个...怎么说...火辣辣的，疼死了"
Output: {{
  "original": "腿那个...怎么说...火辣辣的，疼死了",
  "normalized": "腿部火辣辣的疼",
  "corrections": ["removed filler words '那个', '怎么说'", "standardized '腿' to '腿部'", "converted '疼死了' to '疼'"],
  "confidence": "high"
}}

Input: "我的腿火辣辣的疼，還有點麻"
Output: {{
  "original": "我的腿火辣辣的疼，還有點麻",
  "normalized": "我的腿火辣辣的疼，还有点麻",
  "corrections": ["converted Traditional Chinese to Simplified: 還→还, 點→点"],
  "confidence": "high"
}}

Input: "頭很痛，感覺很難受"
Output: {{
  "original": "頭很痛，感覺很難受",
  "normalized": "头很痛，感觉很难受",
  "corrections": ["converted Traditional Chinese: 頭→头, 難→难"],
  "confidence": "high"
}}

Input: "허리가 따금거려요, 너무 아파요"
Output: {{
  "original": "허리가 따금거려요, 너무 아파요",
  "normalized": "허리가 따끔거리고 심하게 아프다",
  "corrections": ["corrected '따금거려요' to '따끔거리고'", "standardized '너무 아파요' to '심하게 아프다'"],
  "confidence": "high"
}}

Input: "Me duele la espalda, como quemasón"
Output: {{
  "original": "Me duele la espalda, como quemasón",
  "normalized": "Dolor de espalda con quemazón",
  "corrections": ["standardized sentence structure", "corrected 'quemasón' to 'quemazón'"],
  "confidence": "high"
}}
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-5.2",
            messages=[
                {"role": "system", "content": system_prompt + "\n\n**CRITICAL**: Return ONLY valid JSON. No extra text."},
                {"role": "user", "content": text}
            ],
            temperature=0.2  # Slightly higher for natural corrections
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    
    except Exception as e:
        # Fallback: return original text if normalization fails
        return {
            "original": text,
            "normalized": text,
            "corrections": [f"normalization_failed: {str(e)}"],
            "confidence": "low"
        }


def translate_pain_description(text: str, source_language: str, matched_terms: list, mappings: list) -> str:
    """
    Translate patient's pain description to English using matched term translations as reference.
    
    This creates a natural English translation that incorporates the medical terminology
    already mapped from our dictionary. Ensures consistency between term mappings and full sentence.
    
    Args:
        text: Patient's pain description (in source language)
        source_language: Detected language name ("Chinese", "Korean", etc.)
        matched_terms: List of pain terms matched from vocabulary
        mappings: List of ontology mappings with original_term and mapped_english
        
    Returns:
        English translation string
        
    Example:
        >>> text = "我的腿火辣辣的疼，还有点麻"
        >>> matched_terms = ["火辣辣的疼", "麻的"]
        >>> mappings = [
        ...   {"original_term": "火辣辣的疼", "mapped_english": "burning"},
        ...   {"original_term": "麻的", "mapped_english": "numb"}
        ... ]
        >>> translate_pain_description(text, "Chinese", matched_terms, mappings)
        "My leg has burning pain and feels a bit numb"
    """
    
    # Build reference translation dictionary from mappings
    term_translation_ref = {}
    for mapping in mappings:
        original = mapping.get('original_term', '')
        english = mapping.get('mapped_english', '')
        if original and english:
            term_translation_ref[original] = english
    
    # Format term references for prompt
    term_refs = "\n".join([f"  - '{original}' = '{english}'" for original, english in term_translation_ref.items()])
    
    if not term_refs:
        term_refs = "(No pain-specific terms mapped)"
    
    system_prompt = f"""You are a medical translator specializing in pain assessment.

**YOUR TASK**: Translate the patient's {source_language} pain description into natural medical English.

**CRITICAL REQUIREMENT**: You MUST use the provided term translations from our medical dictionary.
These translations are standardized medical terminology (McGill Pain Questionnaire) and MUST be used exactly.

**PROVIDED TERM TRANSLATIONS** (USE THESE EXACTLY):
{term_refs}

**TRANSLATION RULES**:

1. **Use Dictionary Terms Exactly**:
   - When translating matched pain terms, use ONLY the provided English translation
   - Example: If "火辣辣的疼" → "burning", translate as "burning pain" NOT "fiery pain" or "burning hot"
   
2. **Create Natural English**:
   - Produce fluent, natural medical English
   - Maintain professional but clear tone
   - Use proper medical grammar

3. **Preserve All Information**:
   - Include body location, duration, intensity if mentioned
   - Keep emotional and functional impact details
   - Maintain original meaning and severity

4. **Structure**:
   - Use clear, concise sentences
   - Follow standard medical description format: Location + Pain Quality + Duration + Impact

5. **DO NOT**:
   - Add medical interpretations or diagnoses
   - Change pain severity or characteristics
   - Invent information not in original

**OUTPUT**: Return ONLY the English translation text. No JSON, no additional formatting.

**EXAMPLES**:

Example 1:
Input ({source_language}): "我的腿火辣辣的疼，还有点麻"
Term References: "火辣辣的疼"="burning", "麻的"="numb"
Output: "My leg has burning pain and feels a bit numb"

Example 2:
Input ({source_language}): "腰部到腿部触电一样的痛，四个月了，晚上睡不着，很郁闷"
Term References: "触电一样"="electric-shock-like"
Output: "Electric-shock-like pain from lower back to legs for 4 months, can't sleep at night, feeling very depressed"

Example 3:
Input ({source_language}): "膝盖一抽一抽的痛，走路困难"
Term References: "一抽一抽的痛"="throbbing"
Output: "Throbbing pain in knee, difficulty walking"
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-5.2",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Translate: {text}"}
            ],
            temperature=0.2
        )
        
        translation = response.choices[0].message.content.strip()
        
        # Remove quotes if LLM wrapped the output
        if translation.startswith('"') and translation.endswith('"'):
            translation = translation[1:-1]
        
        return translation
    
    except Exception as e:
        # Fallback: just return the original text
        return text


def generate_comprehensive_report(
    original_text: str,
    structured_data: dict,
    ontology_mappings: list,
    clinical_recommendations: list,
    detected_language: str = "Chinese",  # New parameter: detected language
    semantic_analysis: dict = None  # New parameter: semantic distance analysis
) -> str:
    """
    Generate comprehensive multilingual clinical report using GPT after rule-based analysis.
    
    Called AFTER neuro-symbolic pipeline completes. Supports multiple languages:
    Chinese (中文), Korean (한국어), Spanish (Español), Hmong, English
    
    Args:
        original_text: Patient's original pain description
        structured_data: PainOntology data (dict format)
        ontology_mappings: List of term mappings (original_term → mapped_english)
        clinical_recommendations: List of rule-triggered recommendations
        detected_language: Language detected from input (default: "Chinese")
        semantic_analysis: Optional semantic distance analysis for unmapped terms
        
    Returns:
        Comprehensive bilingual clinical report (original language + English)
    """
    
    # Determine bilingual header format based on language
    language_headers = {
        "Chinese": "中文",
        "Korean": "한국어", 
        "Spanish": "Español",
        "Hmong": "Hmoob",
        "English": "English"
    }
    
    native_lang = language_headers.get(detected_language, "原语言")
    
    # If English input, report is English-only
    is_english_only = (detected_language == "English")
    
    system_prompt = f"""You are a medical report writer for multilingual pain assessment.

**INPUT LANGUAGE**: {detected_language}
**OUTPUT FORMAT**: {"English only (no translation needed)" if is_english_only else f"Bilingual ({native_lang} + English)"}

**YOUR TASK**: Create a well-structured clinical report with THREE sections:

**SECTION 1: Translation & Terminology Mapping {"| 翻译与术语映射" if not is_english_only else ""}**
- Explain how patient's expressions were mapped to standardized medical terminology
- {"List Original " + detected_language + " terms → English translations" if not is_english_only else "Show pain descriptors used"}
- Highlight culturally-specific metaphors if present
- Be clear and structured

**SECTION 2: Clinical Assessment {"| 临床评估" if not is_english_only else ""}**
- Summarize pain characteristics: type, location, duration, intensity
- Explain pain classification (neuropathic/nociceptive) in simple terms
- Describe emotional and functional impacts
- Be empathetic and clear

**SECTION 3: Treatment Recommendations {"| 治疗建议" if not is_english_only else ""}**
- Explain each recommended intervention and WHY
- Reference clinical rules or guidelines that triggered recommendations
- Provide actionable guidance
- Be supportive

**FORMATTING REQUIREMENTS**:
- {"Bilingual headings (" + native_lang + " | English)" if not is_english_only else "English headings"}
- Professional but accessible language
- Concise paragraphs
- Bullet points for clarity
- Total: 300-500 words

**TONE**: Professional, empathetic, culturally sensitive

**IMPORTANT**:
- Base ENTIRELY on provided data - do NOT invent
- If no recommendations, provide supportive general guidance
- Maintain medical accuracy while patient-friendly
- {"Use both " + detected_language + " and English for key medical terms" if not is_english_only else "Use clear medical English"}"""

    # Prepare mappings summary (handle different field names)
    mappings_summary = "\n".join([
        f"- '{m.get('original_term', m.get('chinese_input', 'N/A'))}' → '{m.get('mapped_english', 'N/A')}' ({m.get('pain_type', m.get('dimension', 'N/A'))})"
        for m in ontology_mappings
    ]) if ontology_mappings else "No term mappings available"
    
    recommendations_summary = "\n".join([
        f"- {rec.get('triggered_by_rule', 'N/A')}: {rec.get('recommendation', 'N/A')}\n  Evidence: {rec.get('evidence', {})}"
        for rec in clinical_recommendations
    ]) if clinical_recommendations else "No specific recommendations triggered"
    
    # Prepare semantic analysis summary
    semantic_summary = ""
    if semantic_analysis and semantic_analysis.get('unmapped_analysis'):
        semantic_items = []
        for item in semantic_analysis['unmapped_analysis']:
            original = item['original_term']
            matches = item['closest_matches']
            confidence = item['confidence']
            top_match = matches[0]['term'] if matches else 'N/A'
            score = matches[0]['score'] if matches else 0
            semantic_items.append(
                f"  • '{original}' → closest: '{top_match}' (similarity: {score:.2f}, confidence: {confidence})"
            )
        semantic_summary = f"\n\n**SEMANTIC ANALYSIS** (Unmapped Terms - AI Interpretation):\n" + "\n".join(semantic_items)
        semantic_summary += "\n  Note: These are AI-suggested interpretations based on semantic similarity, not exact matches from the medical dictionary."
    
    user_prompt = f"""**PATIENT'S ORIGINAL DESCRIPTION** ({detected_language}):
{original_text}

**STRUCTURED CLINICAL DATA**:
- Pain Type: {structured_data.get('pain_type', 'N/A')}
- Location: {structured_data.get('location', 'N/A')}
- Temporal Pattern: {structured_data.get('temporal_pattern', 'N/A')}
- Intensity: {structured_data.get('intensity', 'N/A')}
- Emotional Impact: {structured_data.get('emotion', 'None detected')}
- Functional Impact: {structured_data.get('functional_impact', 'Not stated')}

**TERM MAPPINGS** ({detected_language} → English):
{mappings_summary}{semantic_summary}

**CLINICAL RECOMMENDATIONS** (From rule engine):
{recommendations_summary}

Please generate a comprehensive {"bilingual" if not is_english_only else ""} clinical report."""

    try:
        response = client.chat.completions.create(
            model="gpt-5.2",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )
        
        report = response.choices[0].message.content
        return report
    
    except Exception as e:
        # Fallback: structured template
        fallback_report = f"""**Clinical Report | 临床报告**

**Patient Description** ({detected_language}):
{original_text}

**Assessment | 评估**:
- Pain Type: {structured_data.get('pain_type', 'N/A')}
- Location: {structured_data.get('location', 'N/A')}
- Duration: {structured_data.get('temporal_pattern', 'N/A')}

**Term Mappings | 术语映射**:
{mappings_summary}

**Recommendations | 建议**:
{recommendations_summary}

(Note: GPT report generation failed: {str(e)})"""
        
        return fallback_report