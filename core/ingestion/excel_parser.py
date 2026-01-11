import pandas as pd

def split_tables(df):

    tables = []
    current_table = []
    
    for _, row in df.iterrows():
        if row.isnull().all():
            if current_table:
                tables.append(pd.DataFrame(current_table))
                current_table = []
        else:
            current_table.append(row)
            
    if current_table:
        tables.append(pd.DataFrame(current_table))
        
    return tables

def parse_excel(file_path):
    """
    parse an Excel file and return structured tables
    returns:
        dict: {
            'file_name': str,
            'sheets': [
                {'sheet_name': str,
                 'tables': [
                    {'table_index': int,
                     'columns': list,
                     'data': list of lists}
                 ]}
            ]
        }
    """
    output = {
        'file_name': file_path.split('/')[-1],
        'sheets': []
    }
    
    xls = pd.ExcelFile(file_path)
    
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        sheet_tables = split_tables(df)
        
        structured_tables = []
        for idx, table_df in enumerate(sheet_tables):
            structured_tables.append({
                'table_index': idx,
                'columns': table_df.columns.tolist(),
                'data': table_df.values.tolist()
            })
        
        output['sheets'].append({
            'sheet_name': sheet_name,
            'tables': structured_tables
        })
    
    return output

if __name__ == "__main__":
    parsed = parse_excel("data/raw/apple_fin.xlsx")
    for sheet in parsed['sheets']:
        print(f"Sheet: {sheet['sheet_name']}, Tables: {len(sheet['tables'])}")
