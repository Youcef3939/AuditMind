import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
STANDARDS_DIR = PROJECT_ROOT / 'data' / 'standards'

def load_standard(file_path):
    """
    load a single standard JSON file
    returns:
        dict or list: raw JSON content
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_all_standards():
    """
    load all JSON standards from data/standards/
    returns:
        dict: {standard_code: standard_data}
    """
    standards = {}
    for file_path in STANDARDS_DIR.glob("*.json"):
        standard_data = load_standard(file_path)

        if isinstance(standard_data, dict):
            code = standard_data.get('standard_code', file_path.stem)
        elif isinstance(standard_data, list):
            code = file_path.stem
            standard_data = {"standard_code": code, "paragraphs": standard_data}
        else:
            raise ValueError(f"Unexpected JSON format in {file_path}")

        standards[code] = standard_data
    return standards

# test
if __name__ == "__main__":
    all_standards = load_all_standards()
    print(f"Loaded {len(all_standards)} standards.")
    sample_code = list(all_standards.keys())[0]
    print(f"Sample: {sample_code}")
    print(all_standards[sample_code])