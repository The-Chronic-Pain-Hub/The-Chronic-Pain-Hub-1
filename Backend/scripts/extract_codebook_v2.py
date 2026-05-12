import re
import json
from pathlib import Path

def parse_codebook_simple(codebook_path):
    """
    Simple line-by-line parser for MTurk Pain Codebook
    """
    with open(codebook_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    scales = []
    current_scale = None
    current_scale_info = None
    in_scale_section = False
    scale_values = {}
    scale_stem = ''
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Detect scale start - ONLY look for "Scale Citation:"
        if 'Scale Citation:' in line:
            # Save previous scale if exists
            if current_scale and current_scale_info:
                scales.append({
                    'name': current_scale,
                    'questions': current_scale_info,
                    'stem': scale_stem,
                    'values': scale_values
                })
            
            # Start new scale
            # Look backwards for scale name (usually 1-3 lines above)
            for j in range(max(0, i-5), i):
                prev_line = lines[j].strip()
                # Scale name is usually a line with parentheses like "(PHQ-9)" or just a title
                if prev_line and len(prev_line) > 10 and '=' not in prev_line:
                    current_scale = prev_line
                    break
            
            current_scale_info = []
            in_scale_section = True
            scale_values = {}
            scale_stem = ''
            print(f"\n[*] Processing: {current_scale}")
        
        # Extract scale stem
        if in_scale_section and 'Scale Stem:' in line:
            stem_start = i + 1
            stem_lines = []
            while stem_start < len(lines) and lines[stem_start].strip() and 'Scoring:' not in lines[stem_start]:
                stem_lines.append(lines[stem_start].strip())
                stem_start += 1
            scale_stem = ' '.join(stem_lines).replace('-----', '').strip()
        
        # Extract SPSS Scoring values
        if in_scale_section and 'SPSS Scoring' in line:
            val_idx = i + 1
            while val_idx < len(lines) and '=' in lines[val_idx] and not lines[val_idx].strip().startswith(('Total', 'Reliability', 'Skewness')):
                val_line = lines[val_idx].strip()
                val_match = re.match(r'(\d+)\s*=\s*(.+)', val_line)
                if val_match:
                    scale_values[val_match.group(1)] = val_match.group(2).strip()
                val_idx += 1
        
        # Extract questions - look for patterns like "PHQ_1", "IEQ_2", etc.
        if in_scale_section:
            # Match question IDs at start of line
            q_match = re.match(r'^([A-Z_]+)_(\d+)\s+(.*)$', line)
            if q_match:
                prefix = q_match.group(1)
                q_num = q_match.group(2)
                rest_of_line = q_match.group(3)
                
                # Parse table columns: Subscale | Reverse | Question
                parts = rest_of_line.split('-----')
                if len(parts) >= 2:
                    subscale = parts[0].strip() if len(parts) > 0 else ''
                    reverse_code = parts[1].strip() if len(parts) > 1 else ''
                    question_text = parts[2].strip() if len(parts) > 2 else ''
                    
                    # Check for reverse coding
                    is_reverse = 'YES' in reverse_code.upper()
                    
                    # Clean question text
                    question_text = re.sub(r'^\d+\.\s*', '', question_text)
                    question_text = re.sub(r'\s+', ' ', question_text)
                    
                    if question_text and len(question_text) > 3:
                        current_scale_info.append({
                            'id': f'{prefix}_{q_num}',
                            'text': question_text[:300],
                            'number': int(q_num),
                            'subscale': subscale if subscale and subscale != '-----' else '',
                            'reverse': is_reverse
                        })
                        print(f"  ✓ {prefix}_{q_num}: {question_text[:50]}...")
        
        # Check for end of scale section
        if in_scale_section and ('Total(' in line or 'Reliability:' in line or 
                                  (line.startswith('Scale Citation:') and current_scale_info)):
            # End of current scale
            in_scale_section = False
        
        i += 1
    
    # Save last scale
    if current_scale and current_scale_info:
        scales.append({
            'name': current_scale,
            'questions': current_scale_info,
            'stem': scale_stem,
            'values': scale_values
        })
    
    return scales

if __name__ == '__main__':
    codebook_path = Path(__file__).parent.parent.parent / 'Documents' / 'MTurk_Pain_Codebook_Extracted.txt'
    
    print("="*80)
    print("Extracting all scales from MTurk Pain Codebook...")
    print("="*80)
    
    scales = parse_codebook_simple(codebook_path)
    
    print(f"\n{'='*80}")
    print("EXTRACTION SUMMARY:")
    print(f"{'='*80}")
    
    total_questions = 0
    for scale in scales:
        q_count = len(scale['questions'])
        total_questions += q_count
        reverse_count = sum(1 for q in scale['questions'] if q.get('reverse'))
        
        print(f"\n{scale['name']}")
        print(f"  Questions: {q_count}")
        if scale['stem']:
            print(f"  Stem: {scale['stem'][:70]}...")
        if scale['values']:
            vals = list(scale['values'].keys())
            print(f"  Scale: {min(vals)}-{max(vals)} ({len(scale['values'])} labels)")
        if reverse_count:
            print(f"  Reverse coded: {reverse_count} items")
    
    print(f"\n{'='*80}")
    print(f"TOTAL: {len(scales)} scales, {total_questions} questions")
    print(f"{'='*80}")
