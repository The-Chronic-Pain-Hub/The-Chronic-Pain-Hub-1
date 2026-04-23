"""
Temporary script to read and display the xlsx content.
This will help us understand the structure and extend to multilingual support.
"""
import pandas as pd
import sys
import os

# Add Backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Read the xlsx file
    xlsx_path = os.path.join(os.path.dirname(__file__), 'data', 'questionnaire_form.xlsx')
    
    # Try to read all sheets
    xl_file = pd.ExcelFile(xlsx_path)
    print(f"📊 Found {len(xl_file.sheet_names)} sheet(s): {xl_file.sheet_names}\n")
    
    for sheet_name in xl_file.sheet_names:
        print(f"\n{'='*60}")
        print(f"📋 Sheet: {sheet_name}")
        print('='*60)
        
        df = pd.read_excel(xlsx_path, sheet_name=sheet_name)
        print(f"\nColumns: {df.columns.tolist()}")
        print(f"Rows: {len(df)}\n")
        print(df.head(20).to_string())
        
except Exception as e:
    print(f"❌ Error reading xlsx: {e}")
    print("\nℹ️ Make sure pandas and openpyxl are installed:")
    print("   pip install pandas openpyxl")
