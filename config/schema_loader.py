# config/schema_loader.py
import json
import os
import yaml

def load_schema(file_obj) -> dict:
    try:
        if file_obj.name.endswith('.yaml') or file_obj.name.endswith('.yml'):
            return yaml.safe_load(file_obj)
        else:
            return json.load(file_obj)
    except Exception:
        return {}

def save_schema(schema: dict, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(schema, f, indent=4)

