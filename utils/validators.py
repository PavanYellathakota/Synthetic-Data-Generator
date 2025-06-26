# utils/validators.py

def validate_schema(schema: dict):
    errors = []
    seen_names = set()

    for col in schema.get("columns", []):
        if "col_no" in col:
            col = {k: v for k, v in col.items() if k != "col_no"}  # Strip col_no before validation

        name = col.get("name")
        if not name:
            errors.append("Column name is missing.")
        elif name in seen_names:
            errors.append(f"Duplicate column name: {name}")
        else:
            seen_names.add(name)

        col_type = col.get("type")
        if col_type in ["Integer", "Float"]:
            col_range = col.get("range")
            if not col_range or len(col_range) != 2:
                errors.append(f"Invalid range for column: {name}")
            elif col_range[0] > col_range[1]:
                errors.append(f"Min > Max in range for column: {name}")

        elif col_type == "Categorical":
            cats = col.get("categories")
            if not cats or not isinstance(cats, list):
                errors.append(f"Missing or invalid categories in column: {name}")

        elif col_type == "PII":
            if not col.get("subtype"):
                errors.append(f"Missing PII subtype in column: {name}")

        elif col_type == "Conditional":
            if not col.get("logic"):
                errors.append(f"Missing logic for conditional column: {name}")

    return errors
