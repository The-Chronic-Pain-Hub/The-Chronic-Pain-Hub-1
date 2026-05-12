import pandas as pd
import json
from pathlib import Path

def import_from_excel(excel_path, output_json_path):
    """
    Import questionnaire data from completed Excel template
    and generate module5_questionnaire.json
    """
    # Read Excel file
    excel_file = pd.ExcelFile(excel_path)
    
    # Get scale overview
    df_overview = pd.read_excel(excel_file, sheet_name='Scale_Overview')
    
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
    print("IMPORTING QUESTIONNAIRE FROM EXCEL")
    print("="*80)
    
    # Process each scale
    for idx, row in df_overview.iterrows():
        scale_name = row['Scale_Name']
        prefix = row['Prefix']
        dimension = row['Dimension']
        
        print(f"\n[{idx+1}/{len(df_overview)}] Processing: {scale_name} ({prefix})")
        
        try:
            # Read questions from scale's sheet
            df_scale = pd.read_excel(excel_file, sheet_name=prefix)
            
            if df_scale.empty or len(df_scale) == 0:
                print(f"  ⚠ No questions found - skipping")
                continue
            
            # Get scale info from first row
            scale_stem = df_scale.iloc[0]['Scale_Stem'] if pd.notna(df_scale.iloc[0]['Scale_Stem']) else ''
            scale_min = int(df_scale.iloc[0]['Scale_Min']) if pd.notna(df_scale.iloc[0]['Scale_Min']) else 1
            scale_max = int(df_scale.iloc[0]['Scale_Max']) if pd.notna(df_scale.iloc[0]['Scale_Max']) else 5
            
            # Build scale labels
            labels = {}
            for i in range(1, 8):  # Scale_Label_1 to Scale_Label_7
                col_name = f'Scale_Label_{i}'
                if col_name in df_scale.columns:
                    label_val = df_scale.iloc[0][col_name]
                    if pd.notna(label_val) and str(label_val).strip():
                        # Map label position to actual scale value
                        if scale_min + (i-1) <= scale_max:
                            labels[str(scale_min + (i-1))] = str(label_val).strip()
            
            # Process questions
            questions = []
            for q_idx, q_row in df_scale.iterrows():
                if pd.isna(q_row['Question_ID']) or pd.isna(q_row['Question_Text']):
                    continue
                
                question_id = str(q_row['Question_ID']).strip()
                question_text = str(q_row['Question_Text']).strip()
                
                # Check reverse coding
                reverse_coded = False
                if pd.notna(q_row['Reverse_Coded']):
                    reverse_val = str(q_row['Reverse_Coded']).strip().upper()
                    reverse_coded = reverse_val in ['YES', 'Y', 'TRUE', '1']
                
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
                
                if reverse_coded:
                    question_obj["reverse"] = True
                
                questions.append(question_obj)
            
            if questions:
                section = {
                    "section_id": prefix.lower(),
                    "title": scale_name,
                    "dimension": dimension,
                    "stem": scale_stem,
                    "questions": questions
                }
                
                questionnaire["questionnaire"]["sections"].append(section)
                total_questions += len(questions)
                
                print(f"  ✓ Added {len(questions)} questions")
                print(f"    Scale: {scale_min}-{scale_max}, {len(labels)} labels")
                if scale_stem:
                    print(f"    Stem: {scale_stem[:60]}...")
            
        except Exception as e:
            print(f"  ✗ Error processing {prefix}: {str(e)}")
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
    excel_path = Path(__file__).parent.parent.parent / 'Documents' / 'Module5_Codebook_Template.xlsx'
    output_path = Path(__file__).parent.parent / 'data' / 'module5_questionnaire_full.json'
    
    if not excel_path.exists():
        print(f"Error: Template file not found at {excel_path}")
        print("Please run create_codebook_template.py first to generate the template.")
    else:
        import_from_excel(excel_path, output_path)
