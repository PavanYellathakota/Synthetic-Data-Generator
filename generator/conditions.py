# generator/conditions.py
import pandas as pd
from simpleeval import simple_eval, NameNotDefined
import numpy as np


def apply_conditions(df: pd.DataFrame, dependencies: list) -> pd.DataFrame:
    for rule in dependencies:
        target = rule.get("target")
        condition = rule.get("condition")
        value_expr = rule.get("value")

        if not all([target, condition, value_expr]):
            continue

        for i in range(len(df)):
            row_context = df.iloc[i].to_dict()
            try:
                if simple_eval(condition, names=row_context):
                    try:
                        result = simple_eval(
                            value_expr,
                            names=row_context,
                            functions={"np": np, "randint": np.random.randint, "choice": np.random.choice}
                        )
                    except NameNotDefined:
                        result = value_expr  # fallback to literal if undefined
                    df.at[i, target] = result
            except Exception:
                continue

    return df
