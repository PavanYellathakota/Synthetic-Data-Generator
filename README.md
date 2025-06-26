
# 🧾 Synthetic Data Generator — Phase 1 (Single Table Edition)

Welcome to the **Synthetic Data Generator** — a modular, production-ready Python platform to generate realistic synthetic datasets for analytics, testing, and ML workflows.

---

## 🚀 Features (Phase 1)

### ✅ Streamlit-Based Interactive UI
- Fully editable column builder in spreadsheet-style format
- Supports dynamic column count & custom names
- Live schema preview (JSON view)

### ✅ Supported Column Types

| Data Type   | Input Format Example                                 | Notes                                     |
|-------------|------------------------------------------------------|-------------------------------------------|
| Integer     | `0, 100`                                              | Range-based values                        |
| Float       | `10000.0, 200000.0`                                   | Range-based float values                  |
| Categorical | `Data, Dev, PM, Support`                              | Comma-separated list of categories        |
| PII         | `name`, `email`, `phone`, `address`                  | Uses `faker` to generate synthetic PII    |
| Date        | `01-01-2020, 12-31-2024`                              | Format: MM-DD-YYYY (auto ISO handled)     |
| Conditional | Python logic per row (see below)                     | E.g. `if salary > 100000: grade = 'A'`    |

---

### 🧠 Conditional Logic Support

Define column values using Python-style expressions:

#### ✅ Single-line:
```python
np.random.choice(['yes', 'no'])
```

#### ✅ Multi-line logic:
```python
if department == 'Data':
    salary = np.random.randint(40000, 120000)
elif department == 'PM':
    salary = np.random.randint(50000, 150000)
```

You may reference other columns using:
- `row['department']`
- `df['name']` (for sampling)
- `np.random.*` functions (safe subset)

---

## 🧱 Folder Layout
> For detailed breakdown see: `architecture_overview.md`

```
synthetic_data_generator/
├── app.py
├── config/         # schema loading/saving
├── generator/      # core generation logic
├── ui/             # Streamlit UI components
├── utils/          # helpers, validation, faker wrappers
├── assets/         # sample schemas
├── export/         # exported files
├── requirements.txt
└── README.md
```

---

## 🔧 Setup Instructions

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate (Windows)

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run Streamlit app
streamlit run app.py
```

---

## 📤 Output & Export
- First 10 rows previewed in UI
- Export to:
  - CSV
  - JSON
  - Excel (`.xlsx`)
- Download buttons available directly in UI

---

## 📦 Schema Save/Load
- Save current schema as `.json`
- Re-upload anytime to resume editing
- Samples in `assets/sample_schemas/`

---

## 🛣️ Phase 2 Sneak Peek
- Multi-table SQL-style schema generation
- Define foreign key relationships
- Export as SQL dump or multi-table ZIP
- Cross-table logic, referential integrity

---

## 🧠 Who is this for?
- Data Scientists and ML Engineers
- QA and Testing Teams
- Data Engineers / ETL Mocks
- Business Analysts building dashboards

---

> 🔖 Tag: `v1.0.0` —  Last updated: Phase 1 Final Patch (Release date: 2025-06-26)
