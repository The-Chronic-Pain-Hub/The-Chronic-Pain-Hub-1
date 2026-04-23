"""
Convert multilingual_pain_data.json to Python dictionary format
for pain_mapping.py
"""
import json
import os

def format_dict_for_python(data, indent=1):
    """Format dictionary data as Python code"""
    lines = []
    tab = "    " * indent
    
    for key, value in data.items():
        if isinstance(value, dict):
            # Check if it's a descriptor dict or category dict
            if 'english' in value:
                # It's a descriptor
                lines.append(f'{tab}"{key}": {{')
                lines.append(f'{tab}    "english": "{value["english"]}",')
                lines.append(f'{tab}    "mcgill_dimension": "sensory",')
                
                # Add SNOMED CT if available
                if value.get('snomed_ct'):
                    lines.append(f'{tab}    "snomed_ct": "{value["snomed_ct"]}"')
                else:
                    lines.append(f'{tab}    "snomed_ct": None')
                
                lines.append(f'{tab}}},')
            else:
                # It's a category
                lines.append(f'{tab}"{key}": {{')
                lines.extend(format_dict_for_python(value, indent + 1))
                lines.append(f'{tab}}},')
    
    return lines

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'multilingual_pain_data.json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    output_lines = []
    
    # Generate dictionaries for each language
    lang_names = {
        'chinese': 'CHINESE',
        'korean': 'KOREAN',
        'spanish': 'SPANISH',
        'hmong': 'HMONG'
    }
    
    for lang_key, lang_upper in lang_names.items():
        output_lines.append(f"\n# {lang_upper} Pain Descriptors")
        output_lines.append(f"{lang_upper}_PAIN_DESCRIPTORS = {{")
        
        lang_data = data[lang_key]
        for category in ['neuropathic', 'nociceptive', 'affective']:
            if category in lang_data and lang_data[category]:
                output_lines.append(f'    "{category}": {{')
                
                for term, info in lang_data[category].items():
                    output_lines.append(f'        "{term}": {{')
                    output_lines.append(f'            "english": "{info["english"]}",')
                    output_lines.append(f'            "mcgill_dimension": "sensory"')
                    output_lines.append(f'        }},')
                
                output_lines.append(f'    }},')
        
        output_lines.append(f"}}\n")
    
    # Save to file
    output_path = os.path.join(script_dir, 'pain_descriptors_formatted.py')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print(f"✅ Formatted pain descriptors saved to: {output_path}")
    print(f"\nStatistics:")
    for lang_key, lang_upper in lang_names.items():
        total = sum(len(data[lang_key].get(cat, {})) for cat in ['neuropathic', 'nociceptive', 'affective'])
        print(f"  {lang_upper}: {total} terms")

if __name__ == '__main__':
    main()
