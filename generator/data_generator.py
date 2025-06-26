# generator/data_generator.py
import pandas as pd
import numpy as np
import uuid
from faker import Faker
from datetime import datetime, timedelta
from generator.conditions import apply_conditions
from utils.faker_utils import generate_pii_value
from utils.helpers import apply_distribution, inject_nulls_outliers


def generate_data(schema: dict, row_count: int) -> pd.DataFrame:
    fake = Faker(schema.get("options", {}).get("locale", "en_US"))
    options = schema.get("options", {})
    columns = schema.get("columns", [])
    data = {}

    for col in columns:
        col = {k: v for k, v in col.items() if k != "col_no"}
        col_name = col["name"]
        col_type = col["type"]

        if col_type in ["Integer", "Float"]:
            low, high = col.get("range", [0, 100])
            if col.get("unique", False):
                domain = np.arange(low, high + 1)
                if len(domain) < row_count:
                    raise ValueError(f"Cannot generate {row_count} unique values for column '{col_name}' in range [{low}, {high}].")
                values = np.random.choice(domain, size=row_count, replace=False)
            else:
                values = np.random.uniform(low, high, row_count) if col_type == "Float" else np.random.randint(low, high + 1, row_count)
            values = apply_distribution(values, options.get("distribution", "Uniform"))
            data[col_name] = values

        elif col_type == "Categorical":
            cats = col.get("categories", ["A", "B"])
            weights = col.get("weights", [1/len(cats)] * len(cats))
            values = np.random.choice(cats, size=row_count, p=weights)
            data[col_name] = values

        elif col_type == "PII" and options.get("enable_pii", True):
            subtype = col.get("subtype", "name")
            values = [generate_pii_value(fake, subtype) for _ in range(row_count)]
            data[col_name] = values

        elif col_type == "Date":
            start_str, end_str = col.get("range", ["2020-01-01", "2024-12-31"])
            try:
                start_date = datetime.strptime(start_str, "%Y-%m-%d")
                end_date = datetime.strptime(end_str, "%Y-%m-%d")
                delta_days = (end_date - start_date).days
                values = [start_date + timedelta(days=np.random.randint(0, delta_days + 1)) for _ in range(row_count)]
                values = [d.strftime("%m-%d-%Y") for d in values]
            except Exception:
                values = ["01-01-2023"] * row_count
            data[col_name] = values

        elif col_type == "Conditional":
            data[col_name] = [None] * row_count

        else:
            data[col_name] = [str(uuid.uuid4()) for _ in range(row_count)]

    df = pd.DataFrame(data)

    if "dependencies" in schema:
        df = apply_conditions(df, schema["dependencies"])

    df = inject_nulls_outliers(df, options)

    return df
