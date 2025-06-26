# utils/helpers.py
import numpy as np
import random

def apply_distribution(values, distribution_type):
    if distribution_type == "Uniform":
        return values
    elif distribution_type == "Normal":
        mean = np.mean(values)
        std = np.std(values) or 1
        return np.random.normal(loc=mean, scale=std, size=len(values))
    elif distribution_type == "Skewed":
        return np.random.exponential(scale=np.mean(values)/2, size=len(values))
    return values

def inject_nulls_outliers(df, options):
    null_pct = options.get("null_percentage", 0)
    outlier_pct = options.get("outlier_percentage", 0)

    for col in df.columns:
        if df[col].dtype in [np.float64, np.int64]:
            if outlier_pct > 0:
                n_outliers = int(len(df) * outlier_pct / 100)
                indices = random.sample(range(len(df)), n_outliers)
                df.loc[indices, col] = df[col].mean() * 10

        if null_pct > 0:
            n_nulls = int(len(df) * null_pct / 100)
            null_indices = random.sample(range(len(df)), n_nulls)
            df.loc[null_indices, col] = None

    return df

def get_export_formats():
    return ["CSV", "JSON", "Excel"]
