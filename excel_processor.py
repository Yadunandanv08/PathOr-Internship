import pandas as pd

def extract_excel(excel_path):
    sheets = pd.read_excel(excel_path, sheet_name=None)
    output = []
    for name, df in sheets.items():
        output.append(f"Sheet: {name}")
        output.append(df.to_csv(index=False))
    return '\n'.join(output)