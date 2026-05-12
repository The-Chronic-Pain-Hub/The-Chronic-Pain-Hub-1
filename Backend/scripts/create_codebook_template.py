import pandas as pd
from pathlib import Path

# Create Excel template for codebook data entry
template_data = {
    'Scale_Name': [
        'The Patient Health Questionnaire (PHQ-9)',
        'Injustice Experience Questionnaire (IEQ)',
        'The Everyday Discrimination Scale (EDS)',
        'Pain Self-Efficacy Questionnaire (PSEQ)',
        'Pain Behavior-Short Form (PB-SF)',
        'Social Support and Pain Questionnaire (SSPQ)',
        'Screener and Opioid Assessment for Patients with Pain (SOAPP)',
        'Athletic Fear Avoidance Questionnaire (AFAQ)',
        'Pain Catastrophizing Scale (PCS)',
        'Chronic Pain Acceptance Questionnaire (CPAQ)',
        'Short Form of the Pain Medication Attitudes Questionnaire (PMAQ-14)',
        'Tampa Scale for Kinesiophobia (TSK)',
        'Pain Frequency, Intensity and Burden Scale (P-FIBS)',
        'Pain Interference Item (PROMIS) Short Form',
        'Parentification Inventory (PI)',
        'Personal Growth Initiative Scale (PGIS)',
        'Mindful Attention Awareness Scale (MAAS)',
        'International Physical Activity Questionnaire (IPAQ-SF)',
        'Somatic Symptom Scale (SSS)',
        'Pain Resilience Scale (PRS)',
        'Family Health Questionnaire (FHQ)',
        'Multidimensional Scale of Perceived Social Support (MSPSS)',
        'Satisfaction with Life Scale (SWLS)',
        'Patriarchal Beliefs Scale (PBS)',
        'Work Family Conflict (WFC)',
        'Conformity to Masculine Norm Inventory (CMNI)',
        'Parentification Questionnaire (PQ)',
        'Filial Responsibility Scale--Adult (FRSA)',
        'Mindfulness Self-Efficacy Scale (MSE)',
        'Economic Ladder',
        'Family Satisfaction Scale (FSS)',
        'Relationship Assessment Scale (RAS)',
        'Job Satisfaction (JSBR)',
        'Individualism and Collectivism Scale (ICS)',
        'Health Behavior Information (HBI)',
    ],
    'Prefix': [
        'PHQ', 'IEQ', 'EDS', 'PSEQ', 'PB', 'SSPQ', 'SOAPP', 'AFAQ', 'PCS', 'CPAQ', 
        'PMAQ', 'TSK', 'PFIBS', 'PROMIS', 'PI', 'PGIS', 'MAAS', 'IPAQ', 'SSS', 'PRS',
        'FHQ', 'MSPSS', 'SWLS', 'PBS', 'WFC', 'CMNI', 'PQ', 'FRSA', 'MSE', 'ECON',
        'FSS', 'RAS', 'JSBR', 'ICS', 'HBI'
    ],
    'Expected_Count': [
        9, 12, 9, 10, '?', 5, '?', '?', 13, 8, 
        14, '?', 9, 8, '?', '?', '?', '?', 8, '?',
        '?', '?', '?', '?', '?', '?', '?', '?', '?', 1,
        '?', '?', 5, '?', 10
    ],
    'Dimension': [
        'dimension_2', 'dimension_2', 'dimension_5', 'dimension_1', 'dimension_1',
        'dimension_5', 'dimension_6', 'dimension_3', 'dimension_2', 'dimension_2',
        'dimension_6', 'dimension_3', 'dimension_1', 'dimension_4', 'dimension_5',
        'dimension_2', 'dimension_2', 'dimension_3', 'dimension_1', 'dimension_2',
        'dimension_5', 'dimension_5', 'dimension_2', 'dimension_5', 'dimension_5',
        'dimension_5', 'dimension_5', 'dimension_5', 'dimension_2', 'dimension_5',
        'dimension_5', 'dimension_5', 'dimension_5', 'dimension_5', 'dimension_6'
    ],
    'Status': [
        'Ready to fill', 'Ready to fill', 'Ready to fill', 'Ready to fill', 'Ready to fill',
        'Ready to fill', 'Ready to fill', 'Ready to fill', 'Ready to fill', 'Ready to fill',
        'Ready to fill', 'Ready to fill', 'Ready to fill', 'Ready to fill', 'Ready to fill',
        'Ready to fill', 'Ready to fill', 'Ready to fill', 'Ready to fill', 'Ready to fill',
        'Ready to fill', 'Ready to fill', 'Ready to fill', 'Ready to fill', 'Ready to fill',
        'Ready to fill', 'Ready to fill', 'Ready to fill', 'Ready to fill', 'Ready to fill',
        'Ready to fill', 'Ready to fill', 'Ready to fill', 'Ready to fill', 'Ready to fill'
    ]
}

# Create detailed template with instructions
questions_template = {
    'Scale_Name': ['EXAMPLE: The Patient Health Questionnaire (PHQ-9)', 'PHQ-9 (copy from codebook)', 'PHQ-9', 'PHQ-9'],
    'Question_ID': ['PHQ_1', 'PHQ_2', 'PHQ_3', 'PHQ_9'],
    'Question_Number': [1, 2, 3, 9],
    'Question_Text': [
        'Little interest or pleasure in doing things',
        'Feeling down, depressed or hopeless',
        'Trouble falling asleep, staying asleep, or sleeping too much',
        'Thoughts that you would be better off dead or of hurting yourself in some way'
    ],
    'Scale_Stem': [
        'Over the past 2 weeks, how often have you been bothered by any of the following problems?',
        '', '', ''
    ],
    'Scale_Min': [1, '', '', ''],
    'Scale_Max': [4, '', '', ''],
    'Scale_Label_1': ['Not at all', '', '', ''],
    'Scale_Label_2': ['Several days', '', '', ''],
    'Scale_Label_3': ['More than half the days', '', '', ''],
    'Scale_Label_4': ['Nearly every day', '', '', ''],
    'Scale_Label_5': ['', '', '', ''],
    'Scale_Label_6': ['', '', '', ''],
    'Scale_Label_7': ['', '', '', ''],
    'Reverse_Coded': ['No', 'No', 'No', 'No'],
    'Subscale': ['', '', '', ''],
    'Notes': ['Fill stem only in first row of each scale', '', '', '']
}

# Create instructions sheet
instructions = {
    'Column': [
        'Scale_Name',
        'Question_ID',
        'Question_Number',
        'Question_Text',
        'Scale_Stem',
        'Scale_Min',
        'Scale_Max',
        'Scale_Label_1 to Scale_Label_7',
        'Reverse_Coded',
        'Subscale',
        'Notes'
    ],
    'Description': [
        'Full name of the scale (e.g., "The Patient Health Questionnaire (PHQ-9)")',
        'Question identifier from codebook (e.g., PHQ_1, IEQ_2)',
        'Numeric order (1, 2, 3...)',
        'Complete question text from codebook',
        'Common stem/instruction shown before all questions in this scale (fill only in first row of each scale)',
        'Minimum scale value (e.g., 1)',
        'Maximum scale value (e.g., 4, 5, or 9)',
        'Labels for each scale point. Leave blank if not used (e.g., 1-9 scale may only have labels at 1,3,5,7,9)',
        'YES if this item should be reverse scored, NO otherwise',
        'Subscale name if specified in codebook (e.g., "Rumination", "Helplessness")',
        'Any additional notes or clarifications'
    ],
    'Example': [
        'The Patient Health Questionnaire (PHQ-9)',
        'PHQ_1',
        '1',
        'Little interest or pleasure in doing things',
        'Over the past 2 weeks, how often have you been bothered by any of the following problems?',
        '1',
        '4',
        '1=Not at all, 2=Several days, 3=More than half the days, 4=Nearly every day',
        'No',
        '(leave blank if none)',
        'PHQ-9: Depression screening, 9 items total'
    ]
}

# Create dimension mapping sheet
dimensions_info = {
    'Dimension_ID': ['dimension_1', 'dimension_2', 'dimension_3', 'dimension_4', 'dimension_5', 'dimension_6'],
    'Dimension_Name': [
        'Pain Severity & Somatic Symptoms',
        'Emotional Distress & Mental Health',
        'Sleep, Function & Fear Avoidance',
        'Pain Interference',
        'Cultural/Social Context & Support',
        'Treatment Preferences & Medication'
    ],
    'Description': [
        'Pain intensity, frequency, burden, somatic symptoms',
        'Depression, anxiety, catastrophizing, acceptance, resilience, growth',
        'Sleep quality, daily functioning, fear of movement, physical activity',
        'How pain interferes with daily activities and quality of life',
        'Social support, discrimination, family dynamics, cultural beliefs',
        'Medication attitudes, treatment history, health behaviors'
    ]
}

# Create workbook
output_path = Path(__file__).parent.parent.parent / 'Documents' / 'Module5_Codebook_Template.xlsx'

with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    # Sheet 1: Scale Overview
    df_overview = pd.DataFrame(template_data)
    df_overview.to_excel(writer, sheet_name='Scale_Overview', index=False)
    
    # Sheet 2: Question Template (with examples)
    df_questions = pd.DataFrame(questions_template)
    df_questions.to_excel(writer, sheet_name='Questions_TEMPLATE', index=False)
    
    # Sheet 3: Instructions
    df_instructions = pd.DataFrame(instructions)
    df_instructions.to_excel(writer, sheet_name='Instructions', index=False)
    
    # Sheet 4: Dimension Mapping
    df_dimensions = pd.DataFrame(dimensions_info)
    df_dimensions.to_excel(writer, sheet_name='Dimension_Info', index=False)
    
    # Sheet 5-39: Empty sheets for each scale (researchers fill these)
    for scale_name, prefix in zip(template_data['Scale_Name'], template_data['Prefix']):
        empty_template = {
            'Scale_Name': [],
            'Question_ID': [],
            'Question_Number': [],
            'Question_Text': [],
            'Scale_Stem': [],
            'Scale_Min': [],
            'Scale_Max': [],
            'Scale_Label_1': [],
            'Scale_Label_2': [],
            'Scale_Label_3': [],
            'Scale_Label_4': [],
            'Scale_Label_5': [],
            'Scale_Label_6': [],
            'Scale_Label_7': [],
            'Reverse_Coded': [],
            'Subscale': [],
            'Notes': []
        }
        df_empty = pd.DataFrame(empty_template)
        
        # Sheet name limited to 31 chars
        sheet_name = f"{prefix}"[:31]
        df_empty.to_excel(writer, sheet_name=sheet_name, index=False)

print("="*80)
print("Excel template created successfully!")
print("="*80)
print(f"\nLocation: {output_path}")
print(f"\nTotal scales: {len(template_data['Scale_Name'])}")
print("\nWhat researchers need to do:")
print("  1. Open the Excel file")
print("  2. Read 'Instructions' sheet")
print("  3. For each scale (PHQ, IEQ, EDS, etc.), go to that scale's sheet")
print("  4. Fill in all questions from the codebook")
print("  5. Include: Question ID, Text, Scale values, Labels, Reverse coding")
print("  6. Save the completed file")
print("\nAfter researchers complete the file, run the import script to generate JSON.")
print("="*80)
