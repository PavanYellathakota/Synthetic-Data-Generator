# app.py — Main Streamlit entry point

import streamlit as st
from config.schema_loader import load_schema, save_schema
from generator.data_generator import generate_data
from utils.validators import validate_schema
from utils.helpers import get_export_formats
import pandas as pd

st.set_page_config(page_title="Synthetic Data Generator", layout="wide")
st.title("🧪 Synthetic Data Generator")

# Sidebar Configuration
st.sidebar.header("Dataset Configuration")
dataset_name = st.sidebar.text_input("Dataset Name", value="my_dataset")
row_count = st.sidebar.number_input("Number of Rows", min_value=10, max_value=1000000, value=1000)

# Load Schema
with st.sidebar.expander("⚙️ Load/Save Schema"):
    schema_file = st.file_uploader("Upload Schema (JSON)", type=["json"])
    if schema_file:
        schema = load_schema(schema_file)
    else:
        schema = {}

# Column Builder UI
st.subheader("📊 Define Columns")
if "columns" not in schema:
    schema["columns"] = []

# Import dynamic column builder module
from ui.column_builder import column_builder_ui
schema["columns"] = column_builder_ui(schema.get("columns", []))

# Advanced Logic UI
from ui.advanced_logic import advanced_logic_ui
schema = advanced_logic_ui(schema)

# PII Toggle & Distribution Settings
from ui.options_panel import options_panel_ui
schema = options_panel_ui(schema)

# Validate + Preview
if st.button("✅ Generate Preview"):
    errors = validate_schema(schema)
    if errors:
        st.error("Schema Validation Failed:")
        for err in errors:
            st.markdown(f"- ❌ {err}")
    else:
        with st.spinner("Generating synthetic data..."):
            df = generate_data(schema, row_count)
            st.success("Data generated successfully!")
            st.dataframe(df.head(10))

            # Export
            export_format = st.selectbox("Export Format", get_export_formats())
            if export_format == "CSV":
                st.download_button("⬇️ Download CSV", df.to_csv(index=False), f"{dataset_name}.csv")
            elif export_format == "JSON":
                st.download_button("⬇️ Download JSON", df.to_json(orient="records"), f"{dataset_name}.json")
            elif export_format == "Excel":
                from io import BytesIO
                output = BytesIO()
                df.to_excel(output, index=False)
                st.download_button("⬇️ Download Excel", output.getvalue(), f"{dataset_name}.xlsx")

# Save Schema
if st.sidebar.button("💾 Save Schema"):
    save_schema(schema, f"assets/sample_schemas/{dataset_name}_schema.json")
    st.sidebar.success("Schema saved!")
