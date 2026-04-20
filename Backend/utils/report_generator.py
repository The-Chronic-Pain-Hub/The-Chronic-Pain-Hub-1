from typing import Dict, List, Any
import os
from openai import OpenAI

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available, use system env vars

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_comprehensive_report(
        original_text: str,
        structured_data: Dict[str, Any],
        ontology_mappings: List[Dict],
        clinical_recommendations: List[Dict],
        detected_language: str,
        semantic_analysis: Dict = None
    
)  -> str:
    """
    Generate comprehensive clinical report using Medical Anthropologist framework.
    
    Uses detailed 4-layer analysis (linguistic, cultural, clinical, psychosocial).
    Outputs as Markdown text for frontend display.
    
    Args:
        original_text: Patient's original pain description
        structured_data: Structured PainOntology data
        ontology_mappings: Ontology mapping trace
        clinical_recommendations: List of triggered recommendations
        detected_language: Detected language name
        semantic_analysis: Optional semantic distance analysis for unmapped terms
        
    Returns:
        Markdown-formatted clinical report for frontend rendering
    """
    
    # Prepare ontology mappings summary (MAPPED TERMS ONLY - exact dictionary matches)
    mapped_terms_summary = []
    for mapping in ontology_mappings[:10]:  # Limit to first 10
        # Skip suggestions - only show exact/direct mappings
        if mapping.get('is_suggestion') or mapping.get('confidence') == 'suggestion_only':
            continue
        
        original = mapping.get('original_term', '')
        english = mapping.get('mapped_english', '')
        pain_type = mapping.get('pain_type', '')
        if original and english:
            mapped_terms_summary.append(f"  - '{original}' → {english} ({pain_type})")
    
    mappings_text = '\n'.join(mapped_terms_summary) if mapped_terms_summary else "  (No direct dictionary mappings found)"
    
    # Prepare recommendations summary
    rec_summary = []
    for rec in clinical_recommendations:
        rule = rec.get('triggered_by_rule', 'Clinical Recommendation')
        text = rec.get('recommendation', '')
        rec_summary.append(f"  - {rule}: {text}")
    
    recs_text = '\n'.join(rec_summary) if rec_summary else "  (Standard pain assessment recommended)"
    
    # Prepare UNMAPPED terms semantic analysis summary
    unmapped_text = ""
    if semantic_analysis and semantic_analysis.get('unmapped_analysis'):
        semantic_items = []
        for item in semantic_analysis['unmapped_analysis']:
            original = item['original_term']
            matches = item['closest_matches']
            confidence = item['confidence']
            if matches:
                # Show ALL top matches (usually top 3)
                match_list = []
                for i, match in enumerate(matches[:3], 1):
                    # V2: Use new field names (native_term + english)
                    native = match.get('native_term', match.get('chinese_term', match.get('term', 'Unknown')))
                    english = match.get('english', '')
                    match_list.append(f"    {i}. {native} ({english}) - similarity: {match['score']:.3f}")
                
                semantic_items.append(
                    f"  - Original: '{original}'\n"
                    f"    Confidence: {confidence}\n"
                    f"    Top matches:\n" + '\n'.join(match_list)
                )
        if semantic_items:
            unmapped_text = "\n\n===== UNMAPPED TERMS - SEMANTIC DISTANCE ANALYSIS (AI-Assisted Interpretation) =====\n"
            unmapped_text += "These terms were NOT found in the standard medical dictionary. AI semantic analysis suggests possible matches:\n\n"
            unmapped_text += '\n'.join(semantic_items)
            unmapped_text += "\n\n  ⚠️ Important: These are AI-generated suggestions based on semantic similarity, NOT exact dictionary matches.\n  Scores closer to 1.0 indicate stronger semantic relationship. Always verify with clinical context."
    
    prompt = f"""You are an expert Medical Anthropologist specializing in cross-cultural pain expression.

Your goal is to translate cultural pain metaphors into structured medical ontologies.
⚠️ DO NOT act as a doctor making a final diagnosis.
⚠️ DO NOT infer beyond the given information.

===== PATIENT INPUT =====
Language: {detected_language}
Original Words: "{original_text}"

===== STRUCTURED CLINICAL DATA (from neuro-symbolic pipeline) =====
Pain Type: {structured_data.get('pain_type', 'Not specified')}
Location: {structured_data.get('location', 'Not specified')}
Temporal Pattern: {structured_data.get('temporal_pattern', 'Not specified')}
Intensity: {structured_data.get('intensity', 'Not stated')}
Emotional Impact: {structured_data.get('emotion', 'None noted')}
Functional Impact: {structured_data.get('functional_impact', 'None noted')}

===== MAPPED TERMS (Direct Matches from Medical Dictionary) =====
{mappings_text}{unmapped_text}

===== CLINICAL RECOMMENDATIONS (from rule engine) =====
{recs_text}

===== YOUR TASK =====
Generate a comprehensive clinical report using this MANDATORY four-layer analytical framework:

**Layer 1: Linguistic Layer (Patient's Voice)**
- Provide literal translation preserving the patient's EXACT wording
- Keep cultural expressions intact (e.g., "死疼死疼的", "불같이 아파요")
- Do NOT simplify or standardize the patient's words

**Layer 2: Cultural-Semantic Layer**
- Identify any culturally specific metaphors or expressions
- Explain their clinical meaning
- If no cultural metaphors exist, clearly state that

**Layer 3: Clinical Abstraction Layer (McGill Pain Questionnaire)**
- Sensory qualities (e.g., sharp, burning, aching)
- Affective qualities (e.g., tiring, distressing)
- Temporal pattern and intensity
- Body location

**Layer 4: Psychosocial Layer**
- Emotional distress indicators
- Under-reporting risk (stoicism patterns)
- Communication considerations

**Layer 5: Semantic Distance Analysis (CRITICAL - if applicable)**
- IF semantic analysis data is provided in the input:
  - Display EACH unmapped term's semantic similarity scores
  - Show the top 3 closest medical terms with similarity scores
  - Include confidence levels (high/medium/low)
  - Explain in plain language what the similarity scores suggest
- IF no semantic analysis data: skip this layer entirely

===== OUTPUT FORMAT =====
Generate in clear Markdown format with these sections:

**📝 Patient's Description (Literal Translation)**
[First quote patient's exact words in original language, then provide word-for-word English translation preserving sentence structure and cultural expressions]
Example format:
> Original: "死疼死疼的，真的受不了了"
> English: "Deadly painful, deadly painful, really can't bear it anymore"

**🔗 Cultural Expression Analysis**
[Analyze any cultural metaphors. If none: "No specific cultural metaphors identified."]

**🏥 McGill Pain Assessment**
- **Sensory Qualities:** [list descriptors]
- **Affective Qualities:** [list descriptors]  
- **Temporal Pattern:** [pattern]
- **Location:** [body location]
- **Intensity:** [severity estimate]

**🧠 Psychosocial Considerations**
- **Emotional Distress:** [Yes/No with brief evidence]
- **Under-reporting Risk:** [Low/Medium/High with reasoning]
- **Communication Notes:** [any relevant observations]

**🔬 Semantic Distance Analysis (AI-Based Interpretation)**
[ONLY include this section IF semantic analysis data exists in the input]
For each unmapped creative expression/metaphor:
- **Original Term:** [patient's exact words]
- **Top 3 Similar Medical Terms:** 
  1. [term] (similarity: X.XX, confidence: high/medium/low)
  2. [term] (similarity: X.XX)
  3. [term] (similarity: X.XX)
- **Clinical Interpretation:** [1-sentence plain-language explanation of what these similarities suggest about the pain quality]

[If NO semantic analysis data provided, completely omit this section]

**⚕️ Clinical Action Plan**
[Synthesize the clinical recommendations above into 2-3 actionable sentences]

===== CRITICAL RULES =====
1. Preserve patient's exact words and emotional tone
2. Base all assessments on actual evidence - don't speculate
3. If no cultural metaphors, state clearly
4. Integrate the provided clinical recommendations
5. **MANDATORY: If semantic analysis data is provided above, you MUST include the "🔬 Semantic Distance Analysis" section with all similarity scores displayed clearly**
6. Keep report professional but comprehensive

Generate the report now:"""

    try:
        response = client.chat.completions.create(
            model='gpt-5.2',
            messages=[
                {"role": "system", "content": "You are a Medical Anthropologist generating clinical reports. Output clear Markdown text. ALWAYS include the Clinical Action Plan section at the end."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_completion_tokens=2500  # Increased for longer reports
        )

        return response.choices[0].message.content
        
    except Exception as e:
        print(f"[Warning] Report generation error: {e}")
        # Fallback to template matching new format
        return f"""**📝 Patient's Description**
"{original_text[:300]}..."

**🔗 Cultural Expression Analysis**
Unable to analyze cultural expressions at this time.

**🏥 McGill Pain Assessment**
- **Sensory Qualities:** Based on structured data
- **Pain Type:** {structured_data.get('pain_type', 'Not specified')}
- **Location:** {structured_data.get('location', 'Not specified')}
- **Temporal Pattern:** {structured_data.get('temporal_pattern', 'Not specified')}
- **Intensity:** {structured_data.get('intensity', 'Not stated')}

**🧠 Psychosocial Considerations**
- **Emotional Distress:** {'Yes' if structured_data.get('emotion') else 'Unknown'}
- **Functional Impact:** {structured_data.get('functional_impact', 'Not noted')}

**⚕️ Clinical Action Plan**
{chr(10).join([f"- {rec.get('recommendation', '')}" for rec in clinical_recommendations[:3]]) if clinical_recommendations else 'Standard pain assessment and management recommended.'}

(Note: Full anthropological analysis unavailable. Using template fallback.)
"""


def translate_to_english_simple(text: str) -> str:
    """
    Simple translation utility to convert short phrases to English.
    
    Used for translating intensity levels, functional impacts, etc.
    If text is already in English, returns it unchanged.
    
    Args:
        text: Short text to translate (e.g., "很痛", "difficulty walking")
        
    Returns:
        English translation or original text if already English
    """
    if not text or text.strip() == "":
        return text
    
    # Quick check: if text is already mostly English (ASCII), return as-is
    try:
        text.encode('ascii')
        return text  # Already English
    except UnicodeEncodeError:
        pass  # Contains non-ASCII, needs translation
    
    system_prompt = """You are a medical translator. Translate the given text into concise medical English.

Rules:
- Keep it brief and clinical
- Preserve medical meaning
- If already English, return unchanged
- Output ONLY the translation, no explanations"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-5.2",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.1,
            max_tokens=50
        )
        
        translation = response.choices[0].message.content.strip()
        
        # Remove quotes if present
        if translation.startswith('"') and translation.endswith('"'):
            translation = translation[1:-1]
        if translation.startswith("'") and translation.endswith("'"):
            translation = translation[1:-1]
            
        return translation
    
    except Exception as e:
        # Fallback: return original
        return text