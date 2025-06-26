# 🏗️ Synthetic Data Generator: Architecture Overview

## 📁 Project Directory Structure
```
synthetic_data_generator/
├── app.py                     # Streamlit UI entry point
├── config/
│   └── schema_loader.py       # Save/load dataset schema (JSON/YAML)
├── generator/
│   ├── data_generator.py      # Core logic to generate synthetic data
│   ├── conditions.py          # Evaluate conditional logic & dependencies
│   └── distributions.py       # Data distribution logic (Uniform, Normal, etc.)
├── ui/
│   ├── column_builder.py      # Streamlit component for schema building (editable table)
│   ├── advanced_logic.py      # (Optional, legacy conditional builder)
│   └── options_panel.py       # Controls for nulls, outliers, PII, distributions
├── utils/
│   ├── validators.py          # Input/schema validation
│   ├── faker_utils.py         # Fake PII generator using faker & APIs
│   └── helpers.py             # Common utility functions
├── assets/
│   └── sample_schemas/        # Predefined schema JSON/YAML examples
├── export/                    # Directory to store exported datasets
│   └── *.csv / *.json / *.sql
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore file
└── README.md                  # Project overview & usage

```

## 🧩 Module Summary

### 🔹 `app.py`
- Main Streamlit UI
- Includes multi-step pages or sidebar navigation:
  - Dataset setup
  - Column config
  - Advanced logic & conditions
  - PII generation toggle
  - Preview & export

### 🔹 `config/schema_loader.py`
- Functions:
  - `save_schema(dict, path)`
  - `load_schema(path)`
- Supports JSON (and optionally YAML)
- Enables reloading past configs

### 🔹 `generator/data_generator.py`
- Core engine to synthesize data
- Processes column rules, types, and distributions
- Applies conditional logic and handles dependencies
- Returns final pandas DataFrame

### 🔹 `generator/conditions.py`
- Safe evaluation of user-defined conditions
- Uses `simpleeval` or AST to sandbox expressions
- Supports inter-column dependencies

### 🔹 `generator/distributions.py`
- Handles data distribution types:
  - Uniform, Normal, Skewed
- Adds support for injection of outliers/nulls

### 🔹 `utils/validators.py`
- Schema and rule validators
- Checks for:
  - Duplicate column names
  - Conflicting ranges or types
  - Malformed expressions or circular dependencies

### 🔹 `utils/faker_utils.py`
- Wraps `faker` to generate:
  - Fake names, emails, phones
  - Random locations (country, city, state)
- Optional: gender, locale support

### 🔹 `utils/helpers.py`
- General helpers:
  - Seed management
  - Unique ID generation
  - Category weight sampling

### 🔹 `assets/sample_schemas/`
- Contains example schemas (in JSON/YAML)
- Can be loaded via UI for demo/testing

### 🔹 `export/`
- Stores output datasets
- Formats supported: CSV, JSON, SQL, Excel

### 🔹 `requirements.txt`
- Dependencies:
  - `streamlit`, `pandas`, `numpy`, `faker`, `uuid`, `simpleeval`, `PyYAML`

---
This modular architecture ensures:
- 🧩 Separation of concerns
- 🔄 Extensibility
- 🔐 Safe execution of user logic
- 📦 Reusability
- ✅ Ease of testing and maintenance

