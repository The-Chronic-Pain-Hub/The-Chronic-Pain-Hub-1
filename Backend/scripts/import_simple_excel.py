import pandas as pd
import json
import re
from pathlib import Path

def parse_scale_values(scale_str):
    """
    Parse scale values string like "1=Not at all, 2=Several Days, 3=More than half the days"
    Returns: (min, max, labels_dict)
    """
    if not scale_str or pd.isna(scale_str):
        return 1, 5, {}
    
    labels = {}
    # Split by comma and parse each value
    parts = str(scale_str).split(',')
    
    for part in parts:
        part = part.strip()
        # Match pattern like "1=Not at all" or "0=Never"
        match = re.match(r'(\d+)\s*=\s*(.+)', part)
        if match:
            value = match.group(1)
            label = match.group(2).strip()
            labels[value] = label
    
    if labels:
        values = [int(k) for k in labels.keys()]
        return min(values), max(values), labels
    else:
        return 1, 5, {}

def import_simple_excel(excel_path, output_json_path):
    """
    Import from simplified 3-column Excel template
    """
    excel_file = pd.ExcelFile(excel_path)
    
    # Dimension mapping (you can adjust these)
    dimension_map = {
        'IDENTITY': 'dimension_0',  # Pre-screening
        'PHQ': 'dimension_2',
        'IEQ': 'dimension_2',
        'EDS': 'dimension_5',
        'PSEQ': 'dimension_1',
        'PB': 'dimension_1',
        'SSPQ': 'dimension_5',
        'SOAPP': 'dimension_6',
        'AFAQ': 'dimension_3',
        'PCS': 'dimension_2',
        'CPAQ': 'dimension_2',
        'PMAQ': 'dimension_6',
        'TSK': 'dimension_3',
        'PFIBS': 'dimension_1',
        'PROMIS': 'dimension_4',
        'PI': 'dimension_5',
        'PGIS': 'dimension_2',
        'MAAS': 'dimension_2',
        'IPAQ': 'dimension_3',
        'SSS': 'dimension_1',
        'PRS': 'dimension_2',
        'FHQ': 'dimension_5',
        'MSPSS': 'dimension_5',
        'SWLS': 'dimension_2',
        'PBS': 'dimension_5',
        'WFC': 'dimension_5',
        'CMNI': 'dimension_5',
        'PQ': 'dimension_5',
        'FRSA': 'dimension_5',
        'MSE': 'dimension_2',
        'ECON': 'dimension_5',
        'FSS': 'dimension_5',
        'RAS': 'dimension_5',
        'JSBR': 'dimension_5',
        'ICS': 'dimension_5',
        'HBI': 'dimension_6'
    }
    
    questionnaire = {
        "questionnaire": {
            "title": "Comprehensive Chronic Pain & Psychosocial Assessment",
            "description": "Complete MTurk Pain Codebook assessment covering all validated pain and psychosocial scales.",
            "estimated_time": "35-45 minutes",
            "sections": []
        }
    }
    
    total_questions = 0
    
    print("="*80)
    print("IMPORTING FROM SIMPLIFIED EXCEL")
    print("="*80)
    
    # Process each sheet (skip only README)
    for sheet_name in excel_file.sheet_names:
        if sheet_name == 'README':
            continue
        
        # Extract prefix from sheet name (e.g., "PHQ (EXAMPLE)" -> "PHQ")
        prefix_match = re.match(r'([A-Z]+)', sheet_name)
        if prefix_match:
            prefix = prefix_match.group(1)
        else:
            prefix = sheet_name.strip()
        
        print(f"\n[*] Processing: {sheet_name}")
        
        try:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            
            # Filter out empty rows
            df = df[df['Question_ID'].notna() & (df['Question_ID'] != '')]
            
            if df.empty:
                print(f"  ⚠ No questions - skipping")
                continue
            
            # Check if first row has scale values (shared scale pattern)
            first_row_scale_str = df.iloc[0]['Scale_Values'] if pd.notna(df.iloc[0]['Scale_Values']) else ''
            has_shared_scale = bool(first_row_scale_str.strip())
            
            # Get dimension
            dimension = dimension_map.get(prefix, 'dimension_1')
            
            # Build questions
            questions = []
            for idx, row in df.iterrows():
                question_id = str(row['Question_ID']).strip()
                question_text = str(row['Question_Text']).strip()
                
                if not question_text or question_text == 'nan':
                    continue
                
                # Determine scale for this question
                # If current row has scale values, use it; otherwise use shared scale
                current_scale_str = str(row['Scale_Values']) if pd.notna(row['Scale_Values']) else ''
                
                if current_scale_str.strip() and '=' in current_scale_str:
                    # This row has its own scale
                    scale_min, scale_max, labels = parse_scale_values(current_scale_str)
                elif has_shared_scale:
                    # Use shared scale from first row
                    scale_min, scale_max, labels = parse_scale_values(first_row_scale_str)
                else:
                    # No scale info - use defaults
                    scale_min, scale_max, labels = 1, 5, {}
                
                question_obj = {
                    "id": question_id,
                    "text": question_text,
                    "type": "likert",
                    "scale": {
                        "min": scale_min,
                        "max": scale_max,
                        "labels": labels.copy()
                    },
                    "scoring": {
                        "weight": 1.0,
                        "dimension": dimension
                    }
                }
                
                questions.append(question_obj)
            
            if questions:
                section = {
                    "section_id": prefix.lower().replace(' ', '_'),
                    "title": f"{prefix} Scale",
                    "dimension": dimension,
                    "stem": "",  # Can be added manually later if needed
                    "questions": questions
                }
                
                questionnaire["questionnaire"]["sections"].append(section)
                total_questions += len(questions)
                
                # Check if questions have mixed scales
                unique_scales = set()
                for q in questions:
                    scale_key = f"{q['scale']['min']}-{q['scale']['max']}"
                    unique_scales.add(scale_key)
                
                if len(unique_scales) == 1:
                    # All questions share same scale
                    print(f"  ✓ {len(questions)} questions (shared scale)")
                    scale_info = list(unique_scales)[0]
                    print(f"    Scale: {scale_info}, {len(questions[0]['scale']['labels'])} labels")
                else:
                    # Questions have different scales
                    print(f"  ✓ {len(questions)} questions (mixed scales)")
                    print(f"    Scales: {', '.join(sorted(unique_scales))}")
        
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            continue
    
    # Save JSON
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(questionnaire, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*80}")
    print(f"IMPORT COMPLETE")
    print(f"{'='*80}")
    print(f"Total sections: {len(questionnaire['questionnaire']['sections'])}")
    print(f"Total questions: {total_questions}")
    print(f"Estimated time: {total_questions * 0.5:.0f}-{total_questions * 0.7:.0f} minutes")
    print(f"\nSaved to: {output_json_path}")
    print(f"{'='*80}")

if __name__ == '__main__':
    excel_path = Path(__file__).parent.parent.parent / 'Documents' / 'Module5_Codebook_Simple.xlsx'
    output_path = Path(__file__).parent.parent / 'data' / 'module5_questionnaire_full.json'
    
    if not excel_path.exists():
        print(f"Error: Excel file not found at {excel_path}")
        print("Please run create_simple_template.py first and have researchers fill it.")
    else:
        import_simple_excel(excel_path, output_path)
