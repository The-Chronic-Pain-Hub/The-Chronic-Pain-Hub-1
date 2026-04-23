"""
Parse multilingual pain descriptor data from xlsx
Generate Python dictionaries for each language
"""
import pandas as pd
import json

def categorize_pain_type(english_word):
    """Categorize pain descriptor into neuropathic, nociceptive, or affective"""
    neuropathic_keywords = [
        'sharp', 'shooting', 'burning', 'tingling', 'numb', 'electric', 
        'stabbing', 'pricking', 'shock', 'sting', 'piercing', 'needle'
    ]
    
    nociceptive_keywords = [
        'aching', 'sore', 'throbbing', 'cramping', 'pressing', 'dull',
        'heavy', 'tight', 'tender', 'stiff', 'pulling', 'squeezing'
    ]
    
    affective_keywords = [
        'exhausting', 'tiring', 'unbearable', 'miserable', 'annoying',
        'troublesome', 'depressing', 'frustrating', 'worrying', 'frightening'
    ]
    
    word_lower = english_word.lower()
    
    # Check each category
    if any(kw in word_lower for kw in neuropathic_keywords):
        return 'neuropathic'
    elif any(kw in word_lower for kw in nociceptive_keywords):
        return 'nociceptive'
    elif any(kw in word_lower for kw in affective_keywords):
        return 'affective'
    else:
        return 'nociceptive'  # Default to nociceptive

def parse_sheet(xlsx_path, sheet_name, english_col, foreign_col):
    """Parse a specific sheet and return structured data"""
    df = pd.read_excel(xlsx_path, sheet_name=sheet_name)
    
    # Special handling for Korean sheet (header is in first row)
    if sheet_name == 'ko-en':
        # First row contains data, not headers
        # Read without header
        df = pd.read_excel(xlsx_path, sheet_name=sheet_name, header=None)
        # Assume column 0 is Korean, column 1 is English
        df.columns = ['Korean', 'English'] + [f'Col{i}' for i in range(len(df.columns) - 2)]
        english_col = 'English'
        foreign_col = 'Korean'
    
    # Remove rows with NaN in critical columns
    if english_col not in df.columns or foreign_col not in df.columns:
        print(f"⚠️  Warning: Expected columns not found in {sheet_name}")
        print(f"    Available columns: {list(df.columns)}")
        return {'neuropathic': {}, 'nociceptive': {}, 'affective': {}}
    
    df = df.dropna(subset=[english_col, foreign_col])
    
    pain_dict = {
        'neuropathic': {},
        'nociceptive': {},
        'affective': {}
    }
    
    for _, row in df.iterrows():
        english = str(row[english_col]).strip()
        foreign = str(row[foreign_col]).strip()
        
        # Skip empty or invalid entries
        if not english or not foreign or english == 'nan' or foreign == 'nan':
            continue
            
        # Categorize
        category = categorize_pain_type(english)
        
        # Add to dictionary (without snomed_ct)
        pain_dict[category][foreign] = {
            'english': english,
            'mcgill_dimension': 'sensory'  # Default, can be refined
        }
    
    return pain_dict

def main():
    xlsx_path = r'c:\Users\ChaCha ship\Documents\Github\PainReport\Backend\data\questionnaire_form.xlsx'
    
    # Parse each language sheet with correct column names
    # Format: (sheet_name, english_column, foreign_column)
    languages = {
        'chinese': ('cn-en', 'English', 'Chinese'),
        'korean': ('ko-en', 'English', 'Korean'),  # Will be handled specially
        'spanish': ('es-en', 'English', 'Spanish'),
        'hmong': ('hmong-en', 'English pain words', 'Hmong pain words')
    }
    
    results = {}
    
    for lang_name, (sheet_name, english_col, foreign_col) in languages.items():
        print(f"\n{'='*60}")
        print(f"Parsing {lang_name.upper()} ({sheet_name})")
        print(f"{'='*60}")
        
        pain_dict = parse_sheet(xlsx_path, sheet_name, english_col, foreign_col)
        results[lang_name] = pain_dict
        
        # Print statistics
        total = sum(len(pain_dict[cat]) for cat in pain_dict)
        print(f"Total terms: {total}")
        print(f"  - Neuropathic: {len(pain_dict['neuropathic'])}")
        print(f"  - Nociceptive: {len(pain_dict['nociceptive'])}")
        print(f"  - Affective: {len(pain_dict['affective'])}")
        
        # Show samples
        if len(pain_dict['neuropathic']) > 0:
            print(f"\nSample neuropathic terms:")
            for i, (foreign, data) in enumerate(list(pain_dict['neuropathic'].items())[:3]):
                print(f"  {foreign} -> {data['english']}")
    
    # Save to JSON for inspection
    import os
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(scripts_dir, 'multilingual_pain_data.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n\n✅ Multilingual data saved to: {output_path}")
    
    return results

if __name__ == '__main__':
    main()
