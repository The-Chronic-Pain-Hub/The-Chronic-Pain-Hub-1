# Module 5 Codebook Data Entry Workflow

## Overview
This workflow allows research team members to systematically input all questionnaire data from the MTurk Pain Codebook into a structured Excel template, which is then automatically converted to the JSON format needed by Module 5.

## Files Created

### 1. Module5_Codebook_Template.xlsx
Location: `Documents/Module5_Codebook_Template.xlsx`

**Structure:**
- **Scale_Overview** - List of all 35 scales with prefixes and dimensions
- **Questions_TEMPLATE** - Example showing correct format (PHQ-9 samples)
- **Instructions** - Detailed column descriptions and guidelines
- **Dimension_Info** - Explanation of 6 clinical dimensions
- **PHQ, IEQ, EDS, etc.** - Individual sheets for each scale (35 total)

### 2. create_codebook_template.py
Script that generates the Excel template.

### 3. import_from_excel.py
Script that converts completed Excel → JSON questionnaire.

## Workflow for Research Team

### Step 1: Open Template
1. Open `Module5_Codebook_Template.xlsx`
2. Read the **Instructions** sheet carefully
3. Review **Questions_TEMPLATE** for examples

### Step 2: Fill Data for Each Scale
For each of the 35 scales:

1. **Navigate to scale sheet** (e.g., "PHQ", "IEQ", "EDS")
2. **Fill required columns:**
   - `Scale_Name` - Same for all rows in this scale
   - `Question_ID` - From codebook (e.g., PHQ_1, PHQ_2...)
   - `Question_Number` - Sequential (1, 2, 3...)
   - `Question_Text` - Exact wording from codebook
   - `Scale_Stem` - Common instruction (fill only in row 1)
   - `Scale_Min` - Minimum value (e.g., 1)
   - `Scale_Max` - Maximum value (e.g., 4, 5, 9)
   - `Scale_Label_1 to Scale_Label_7` - Text labels for scale points
   - `Reverse_Coded` - "Yes" or "No"
   - `Subscale` - If specified in codebook
   - `Notes` - Any clarifications

### Step 3: Important Guidelines

**Scale Labels:**
- For 1-4 scale: Fill Label_1, Label_2, Label_3, Label_4
- For 1-9 scale with gaps: Fill only labeled points (e.g., Label_1, Label_3, Label_5, Label_7, Label_9), leave others blank
- Example: P-FIBS uses 1-9 but only labels 1,3,5,7,9

**Scale Stem:**
- Common instruction shown once before all questions
- Fill ONLY in first row of each scale
- Leave blank in subsequent rows
- Example: "Over the past 2 weeks, how often have you been bothered by..."

**Reverse Coding:**
- Check codebook "Reverse Code" column
- Enter "Yes" if marked "YES" or "Reverse"
- Enter "No" otherwise
- Important for scoring accuracy!

**Question IDs:**
- Must match codebook exactly (e.g., PHQ_1, not PHQ1)
- Sequential numbering (PHQ_1, PHQ_2, PHQ_3...)

### Step 4: Save
- Save the Excel file when complete
- Keep original filename: `Module5_Codebook_Template.xlsx`

### Step 5: Generate JSON
Developer runs:
```bash
cd Backend/scripts
python import_from_excel.py
```

This creates: `Backend/data/module5_questionnaire_full.json`

## Data Validation Checklist

Before submitting completed Excel:

- [ ] All 35 scales have at least one question
- [ ] No empty Question_ID or Question_Text cells
- [ ] Scale_Min and Scale_Max are filled (first row of each scale)
- [ ] Scale labels are filled for used scale points
- [ ] Scale_Stem is filled (first row only)
- [ ] Reverse_Coded is "Yes" or "No" (no blanks)
- [ ] Question numbers are sequential (1,2,3...)
- [ ] Question IDs match codebook format (PREFIX_NUMBER)

## Expected Output

**Scales:** 35  
**Total Questions:** ~200-300 (depending on codebook)  
**Estimated completion time:** 30-45 minutes for respondents

**Dimension Breakdown:**
- dimension_1: Pain Severity & Somatic Symptoms
- dimension_2: Emotional Distress & Mental Health  
- dimension_3: Sleep, Function & Fear Avoidance
- dimension_4: Pain Interference
- dimension_5: Cultural/Social Context & Support
- dimension_6: Treatment Preferences & Medication

## Troubleshooting

**Q: What if a scale has no items in codebook?**  
A: Leave that sheet empty, skip it. The import script will handle it.

**Q: What if scale has more than 7 label points?**  
A: Use Scale_Label_1 through Scale_Label_7 for first 7. Add note if needed.

**Q: How to handle scales with different formats (not Likert)?**  
A: For now, adapt to Likert format. Add detailed note. We can customize later.

**Q: What if I'm unsure about reverse coding?**  
A: Check codebook "Reverse Code" column carefully. When in doubt, put "No" and add note.

## Contact

Questions during data entry? Contact development team or refer to:
- Original codebook: `Documents/MTurk_Pain_Codebook_Extracted.txt`
- Instructions sheet in Excel
- Example template (Questions_TEMPLATE sheet)

## Version History
- v1.0 (2026-05-12): Initial template with 35 scales, 6 dimensions
