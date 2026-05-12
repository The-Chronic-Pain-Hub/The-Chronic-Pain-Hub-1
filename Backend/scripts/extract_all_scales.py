import re
import json
from pathlib import Path

def parse_codebook(codebook_path):
    """
    Extract all scales from MTurk Pain Codebook
    Returns structured questionnaire data
    """
    with open(codebook_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    scales = []
    
    # Define scale patterns - each scale has a specific structure
    # Format: Variable Name | Subscale | Reverse Code | Question Wording | Values
    
    # Pattern to find scale sections
    scale_pattern = r'(?:^|\n)([A-Z].*?(?:Scale|Questionnaire|Inventory|Index).*?)\n.*?(?:Scale Citation:|Variable Name)'
    
    # Split content by scale sections
    sections = re.split(r'\n(?=[A-Z][a-z]+ (?:Health|Self|Pain|Discrimination|Experience|Catastrophizing|Acceptance|Medication|Scale|Questionnaire))', content)
    
    current_scale = None
    
    for line in content.split('\n'):
        # Detect scale headers
        if 'Scale Citation:' in line or 'Questionnaire (' in line:
            # Extract scale name from previous context
            pass
        
        # Detect question patterns like PHQ_1, IEQ_1, etc.
        question_match = re.match(r'^([A-Z_]+)_(\d+)', line)
        if question_match:
            scale_prefix = question_match.group(1)
            question_num = question_match.group(2)
            # Extract question text and options
    
    return scales

def extract_scale_info(content, scale_name, prefix):
    """
    Extract all questions for a specific scale
    Returns list of question objects with scale values and reverse coding
    """
    questions = []
    scale_info = {'stem': '', 'values': {}, 'min': 1, 'max': 5}
    
    # Find the scale section
    scale_pattern = rf'{re.escape(scale_name)}.*?(?=\n[A-Z][a-z]+.*?(?:Scale|Questionnaire|Inventory)|\Z)'
    scale_match = re.search(scale_pattern, content, re.DOTALL)
    
    if not scale_match:
        return questions, scale_info
    
    scale_section = scale_match.group(0)
    
    # Extract scale stem
    stem_match = re.search(r'Scale Stem:\s*(.+?)(?:\n\n|Scoring:)', scale_section, re.DOTALL)
    if stem_match:
        scale_info['stem'] = stem_match.group(1).strip().replace('-----', '').strip()
    
    # Extract scale values from first question
    values_match = re.search(r'Scale Scoring\s+(.*?)(?:SPSS Scoring|\n{2,})', scale_section, re.DOTALL)
    if values_match:
        values_text = values_match.group(1)
        for line in values_text.split('\n'):
            # Match patterns like "0=Not at all" or "1=never"
            value_pattern = r'(\d+)\s*=\s*(.+)'
            m = re.match(value_pattern, line.strip())
            if m:
                scale_info['values'][m.group(1)] = m.group(2).strip()
    
    # Extract SPSS Scoring (actual values used in questionnaire)
    spss_match = re.search(r'SPSS Scoring\s+(.*?)(?:\n{2,})', scale_section, re.DOTALL)
    if spss_match:
        spss_values = {}
        spss_text = spss_match.group(1)
        for line in spss_text.split('\n'):
            value_pattern = r'(\d+)\s*=\s*(.+)'
            m = re.match(value_pattern, line.strip())
            if m:
                spss_values[m.group(1)] = m.group(2).strip()
        if spss_values:
            scale_info['values'] = spss_values  # Use SPSS values if available
    
    # Calculate min/max
    if scale_info['values']:
        scale_info['min'] = min([int(k) for k in scale_info['values'].keys()])
        scale_info['max'] = max([int(k) for k in scale_info['values'].keys()])
    
    # Extract all questions - find pattern: PREFIX_NUMBER followed by optional subscale/reverse, then text
    # Format in codebook: PREFIX_N | Subscale | ----- or YES | Question text
    question_pattern = rf'{prefix}_(\d+)\s+([^\n]*?)\s+([^\n]*?)\s+(.+?)(?=\n{prefix}_\d+|\nTotal\(|\nReliability:|\Z)'
    matches = re.finditer(question_pattern, scale_section, re.DOTALL)
    
    for match in matches:
        q_num = match.group(1)
        subscale = match.group(2).strip()
        reverse_code = match.group(3).strip()
        q_text = match.group(4).strip()
        
        # Clean up question text - remove scale scoring if present
        q_text = re.sub(r'Scale Scoring.*$', '', q_text, flags=re.DOTALL).strip()
        q_text = re.sub(r'SPSS Scoring.*$', '', q_text, flags=re.DOTALL).strip()
        q_text = re.sub(r'\s+', ' ', q_text)
        q_text = re.sub(r'^\d+\.\s*', '', q_text)  # Remove leading number
        
        # Detect reverse coding
        is_reverse = 'YES' in reverse_code.upper() or 'REVERSE' in reverse_code.upper()
        
        if q_text and q_text != '-----':
            questions.append({
                'id': f'{prefix}_{q_num}',
                'text': q_text[:200],  # Limit text length
                'number': int(q_num),
                'subscale': subscale if subscale != '-----' else '',
                'reverse': is_reverse
            })
    
    return sorted(questions, key=lambda x: x['number']), scale_info

def extract_scale_values(content, scale_name):
    """
    Extract scale values/labels (e.g., 1=Never, 2=Rarely, etc.)
    """
    # Look for "Scale Scoring" or "Values" section
    scoring_pattern = r'Scale Scoring\s*(.*?)(?:SPSS Scoring|Total|Reliability)'
    match = re.search(scoring_pattern, content, re.DOTALL)
    
    if match:
        scoring_text = match.group(1)
        # Parse scale values
        values = {}
        for line in scoring_text.split('\n'):
            value_match = re.match(r'(\d+)\s*=\s*(.+)', line.strip())
            if value_match:
                values[value_match.group(1)] = value_match.group(2).strip()
        return values
    
    return None

def parse_full_codebook():
    """
    Main function to parse entire codebook and create questionnaire JSON
    """
    codebook_path = Path(__file__).parent.parent.parent / 'Documents' / 'MTurk_Pain_Codebook_Extracted.txt'
    
    with open(codebook_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define all scales from table of contents
    scales_config = [
        {'name': 'The Patient Health Questionnaire (PHQ-9)', 'prefix': 'PHQ', 'count': 9, 'dimension': 'dimension_2'},
        {'name': 'Injustice Experience Questionnaire (IEQ)', 'prefix': 'IEQ', 'count': 12, 'dimension': 'dimension_2'},
        {'name': 'The Everyday Discrimination Scale (EDS)', 'prefix': 'EDS', 'count': 9, 'dimension': 'dimension_5'},
        {'name': 'Pain Self-Efficacy Questionnaire (PSEQ)', 'prefix': 'PSEQ', 'count': 10, 'dimension': 'dimension_1'},
        {'name': 'Pain Behavior-Short Form (PB-SF)', 'prefix': 'PB', 'count': None, 'dimension': 'dimension_1'},
        {'name': 'Social Support and Pain Questionnaire (SSPQ)', 'prefix': 'SSPQ', 'count': 5, 'dimension': 'dimension_5'},
        {'name': 'Screener and Opioid Assessment for Patients with Pain (SOAPP)', 'prefix': 'SOAPP', 'count': None, 'dimension': 'dimension_6'},
        {'name': 'Painkiller Use and Misuse', 'prefix': 'PAIN_MED', 'count': None, 'dimension': 'dimension_6'},
        {'name': 'Athletic Fear Avoidance Questionnaire (AFAQ)', 'prefix': 'AFAQ', 'count': None, 'dimension': 'dimension_3'},
        {'name': 'Pain Catastrophizing Scale (PCS)', 'prefix': 'PCS', 'count': 13, 'dimension': 'dimension_2'},
        {'name': 'Chronic Pain Acceptance Questionnaire (CPAQ)', 'prefix': 'CPAQ', 'count': 8, 'dimension': 'dimension_2'},
        {'name': 'Short Form of the Pain Medication Attitudes Questionnaire (PMAQ-14)', 'prefix': 'PMAQ', 'count': 14, 'dimension': 'dimension_6'},
        {'name': 'Tampa Scale for Kinesiophobia (TSK)', 'prefix': 'TSK', 'count': None, 'dimension': 'dimension_3'},
        {'name': 'Pain Frequency, Intensity and Burden Scale (P-FIBS)', 'prefix': 'PFIBS', 'count': 9, 'dimension': 'dimension_1'},
        {'name': 'Pain Interference Item (PROMIS) Short Form', 'prefix': 'PROMIS', 'count': 8, 'dimension': 'dimension_4'},
        {'name': 'Parentification Inventory (PI)', 'prefix': 'PI', 'count': None, 'dimension': 'dimension_5'},
        {'name': 'Personal Growth Initiative Scale (PGIS)', 'prefix': 'PGIS', 'count': None, 'dimension': 'dimension_2'},
        {'name': 'Mindful Attention Awareness Scale (MAAS)', 'prefix': 'MAAS', 'count': None, 'dimension': 'dimension_2'},
        {'name': 'International Physical Activity Questionnaire (IPAQSF)', 'prefix': 'IPAQ', 'count': None, 'dimension': 'dimension_3'},
        {'name': 'Somatic Symptom Scale (SSS)', 'prefix': 'SSS', 'count': 8, 'dimension': 'dimension_1'},
        {'name': 'Pain Resilience Scale (PRS)', 'prefix': 'PRS', 'count': None, 'dimension': 'dimension_2'},
        {'name': 'Family Health Questionnaire (FHQ)', 'prefix': 'FHQ', 'count': None, 'dimension': 'dimension_5'},
        {'name': 'Multidimensional Scale of Perceived Social Support (MSPSS)', 'prefix': 'MSPSS', 'count': None, 'dimension': 'dimension_5'},
        {'name': 'Satisfaction with Life Scale (SWLS)', 'prefix': 'SWLS', 'count': None, 'dimension': 'dimension_2'},
        {'name': 'Patriarchal Beliefs Scale (PBS)', 'prefix': 'PBS', 'count': None, 'dimension': 'dimension_5'},
        {'name': 'Work Family Conflict (WFC)', 'prefix': 'WFC', 'count': None, 'dimension': 'dimension_5'},
        {'name': 'Conformity to Masculine Norm Inventory (CMNI)', 'prefix': 'CMNI', 'count': None, 'dimension': 'dimension_5'},
        {'name': 'Parentification Questionnaire (PQ)', 'prefix': 'PQ', 'count': None, 'dimension': 'dimension_5'},
        {'name': 'Filial Responsibility Scale--Adult (FRSA)', 'prefix': 'FRSA', 'count': None, 'dimension': 'dimension_5'},
        {'name': 'Mindfulness Self-Efficacy (MSE) Scale', 'prefix': 'MSE', 'count': None, 'dimension': 'dimension_2'},
        {'name': 'Economic Ladder', 'prefix': 'ECON', 'count': 1, 'dimension': 'dimension_5'},
        {'name': 'Family Satisfaction Scale (FSS)', 'prefix': 'FSS', 'count': None, 'dimension': 'dimension_5'},
        {'name': 'Relationship Assessment Scale (RAS)', 'prefix': 'RAS', 'count': None, 'dimension': 'dimension_5'},
        {'name': 'Job Satisfaction (JSBR)', 'prefix': 'JSBR', 'count': 5, 'dimension': 'dimension_5'},
        {'name': 'Individualism and Collectivism Scale (ICS)', 'prefix': 'ICS', 'count': None, 'dimension': 'dimension_5'},
        {'name': 'Health Behavior Information (HBI)', 'prefix': 'HBI', 'count': 10, 'dimension': 'dimension_6'},
    ]
    
    questionnaire = {
        "questionnaire": {
            "title": "Comprehensive Chronic Pain & Psychosocial Assessment",
            "description": "Complete MTurk Pain Codebook assessment covering all validated pain and psychosocial scales.",
            "estimated_time": "35-45 minutes",
            "sections": []
        }
    }
    
    total_questions = 0
    
    for scale_config in scales_config:
        print(f"\n{'='*80}")
        print(f"Processing: {scale_config['name']}")
        print(f"Prefix: {scale_config['prefix']}")
        
        # Extract questions for this scale
        questions, scale_info = extract_scale_info(content, scale_config['name'], scale_config['prefix'])
        
        if not questions:
            print(f"  ⚠️  No questions found for {scale_config['prefix']}")
            continue
        
        print(f"  ✅ Found {len(questions)} questions")
        print(f"     Scale: {scale_info['min']}-{scale_info['max']}, Values: {len(scale_info['values'])} labels")
        if scale_info['stem']:
            print(f"     Stem: {scale_info['stem'][:60]}...")
        
        reverse_count = sum(1 for q in questions if q.get('reverse'))
        if reverse_count:
            print(f"     Reverse coded: {reverse_count} items")
        
        total_questions += len(questions)
        
        # Print sample questions
        for q in questions[:2]:  # Print first 2
            print(f"    {q['id']}: {q['text'][:70]}...")
        if len(questions) > 2:
            print(f"    ... and {len(questions) - 2} more")
    
    print(f"\n{'='*80}")
    print(f"TOTAL QUESTIONS FOUND: {total_questions}")
    print(f"TOTAL SCALES: {len([s for s in scales_config if extract_scale_info(content, s['name'], s['prefix'])])}")
    
    return questionnaire

if __name__ == '__main__':
    print("Extracting all scales from MTurk Pain Codebook...")
    print("="*80)
    result = parse_full_codebook()
    
    # Save results
    output_path = Path(__file__).parent.parent / 'data' / 'module5_questionnaire_full.json'
    # Will implement full JSON generation after validating extraction
