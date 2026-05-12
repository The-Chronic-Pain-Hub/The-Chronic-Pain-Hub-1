import re
import json
from pathlib import Path

def extract_all_questions_regex(codebook_path):
    """
    Extract all questions using regex from the entire codebook text
    Pattern: PREFIX_NUMBER----------Question text
    """
    with open(codebook_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match question IDs and their text
    # Format: PREFIX_NUMBER followed by dashes (usually -----) then question text
    pattern = r'([A-Z][A-Z_]+)_(\d+)\s*-{3,}\s*(.+?)(?=[A-Z][A-Z_]+_\d+\s*-{3,}|Total\(|EXECUTE|Reliability|Scale Citation:|\Z)'
    
    matches = re.findall(pattern, content, re.DOTALL)
    
    questions_by_scale = {}
    
    for match in matches:
        prefix = match[0]
        q_num = match[1]
        q_text = match[2].strip()
        
        # Clean up question text
        q_text = re.sub(r'^\d+\.\s*', '', q_text)  # Remove leading number
        q_text = re.sub(r'\s+', ' ', q_text)  # Normalize whitespace
        q_text = re.sub(r'Scale Scoring.*$', '', q_text)[:300]  # Remove scale info, limit length
        
        if len(q_text) > 5:  # Only keep meaningful questions
            if prefix not in questions_by_scale:
                questions_by_scale[prefix] = []
            
            questions_by_scale[prefix].append({
                'id': f'{prefix}_{q_num}',
                'text': q_text.strip(),
                'number': int(q_num)
            })
    
    # Sort questions within each scale
    for prefix in questions_by_scale:
        questions_by_scale[prefix].sort(key=lambda x: x['number'])
    
    return questions_by_scale

def extract_scale_names(codebook_path):
    """
    Extract scale names and their prefixes
    """
    with open(codebook_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all scale citations
    pattern = r'([^.]+?)\s*Scale Citation:'
    matches = re.findall(pattern, content)
    
    # Clean up scale names
    scale_names = []
    for match in matches:
        name = match.strip().split('\n')[-1].strip()
        if len(name) > 10 and '=' not in name:
            scale_names.append(name)
    
    return scale_names

def extract_scale_info_enhanced(codebook_path, prefix):
    """
    Extract scale values and reverse coding for a specific prefix
    """
    with open(codebook_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    scale_info = {
        'stem': '',
        'values': {},
        'reverse_items': []
    }
    
    # Find scale section for this prefix
    # Look for first occurrence of this prefix followed by scale scoring
    pattern = rf'{prefix}_1.*?Scale Stem:\s*(.+?)(?:Scoring|Variable Name)'
    stem_match = re.search(pattern, content, re.DOTALL)
    if stem_match:
        scale_info['stem'] = stem_match.group(1).replace('-----', '').strip()[:200]
    
    # Extract SPSS Scoring values
    pattern = rf'{prefix}_1.*?SPSS Scoring\s+(.*?)(?:{prefix}_2|Total|$)'
    values_match = re.search(pattern, content, re.DOTALL)
    if values_match:
        values_text = values_match.group(1)
        for line in values_text.split('\n')[:10]:  # First 10 lines
            val_match = re.match(r'(\d+)\s*=\s*(.+)', line.strip())
            if val_match:
                scale_info['values'][val_match.group(1)] = val_match.group(2).strip()
    
    # Look for YES in reverse code column (simplified - would need more parsing)
    # For now, return empty reverse list
    
    return scale_info

if __name__ == '__main__':
    codebook_path = Path(__file__).parent.parent.parent / 'Documents' / 'MTurk_Pain_Codebook_Extracted.txt'
    
    print("="*80)
    print("EXTRACTING ALL QUESTIONS FROM CODEBOOK")
    print("="*80)
    
    questions_by_scale = extract_all_questions_regex(codebook_path)
    
    print(f"\nFound {len(questions_by_scale)} scales\n")
    
    total_questions = 0
    for prefix in sorted(questions_by_scale.keys()):
        questions = questions_by_scale[prefix]
        total_questions += len(questions)
        
        print(f"\n{prefix}: {len(questions)} questions")
        
        # Get scale info
        scale_info = extract_scale_info_enhanced(codebook_path, prefix)
        if scale_info['stem']:
            print(f"  Stem: {scale_info['stem'][:60]}...")
        if scale_info['values']:
            vals = list(scale_info['values'].keys())
            print(f"  Scale: {min(vals)}-{max(vals)} ({len(scale_info['values'])} labels)")
        
        # Show first 2 questions
        for q in questions[:2]:
            print(f"    {q['id']}: {q['text'][:60]}...")
        if len(questions) > 2:
            print(f"    ... and {len(questions)-2} more")
    
    print(f"\n{'='*80}")
    print(f"TOTAL: {len(questions_by_scale)} scales, {total_questions} questions")
    print(f"{'='*80}")
    
    # Save to JSON for further processing
    output = {
        'total_scales': len(questions_by_scale),
        'total_questions': total_questions,
        'scales': {}
    }
    
    for prefix in sorted(questions_by_scale.keys()):
        scale_info = extract_scale_info_enhanced(codebook_path, prefix)
        output['scales'][prefix] = {
            'questions': questions_by_scale[prefix],
            'stem': scale_info['stem'],
            'values': scale_info['values'],
            'count': len(questions_by_scale[prefix])
        }
    
    output_path = Path(__file__).parent.parent / 'data' / 'extracted_scales_raw.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Saved to: {output_path}")
