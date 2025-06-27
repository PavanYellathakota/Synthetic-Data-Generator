# ui/column_builder.py
import streamlit as st
import pandas as pd
import json
from datetime import datetime

DEFAULT_TYPES = ["Integer", "Float", "Categorical", "PII", "Date", "Conditional"]
PII_TYPES = ["name", "email", "phone", "address"]


def column_builder_ui(columns_config):
    # st.markdown("### 🧩 Define Schema Columns (Editable Table)")

    num_cols = st.number_input("How many columns do you want to define?", min_value=1, max_value=50, value=len(columns_config) or 4)

    # Optional: paste comma-separated headers to populate names
    headers_input = st.text_input("Paste comma-separated column names (optional)", value="")
    parsed_headers = [h.strip() for h in headers_input.split(",") if h.strip()] if headers_input else []

    # Initialize table only if row count changes or headers provided
    if ("columns_df" not in st.session_state
        or len(st.session_state.columns_df) != num_cols
        or parsed_headers):

        st.session_state.columns_df = pd.DataFrame([
            {
                "col_no": f"col{i+1}",
                "name": parsed_headers[i] if i < len(parsed_headers) else f"col_{i+1}",
                "type": "Integer",
                "range/categories": "0, 100",
                "logic": ""
            }
            for i in range(num_cols)
        ])

    column_config = {
        "type": st.column_config.SelectboxColumn(
            "Data Type",
            options=DEFAULT_TYPES,
        ),
        "range/categories": st.column_config.TextColumn(
            "Range or Categories",
            help="For numeric: min,max | For categorical: comma-separated values | For date: MM-DD-YYYY,MM-DD-YYYY"
        ),
        "logic": st.column_config.TextColumn(
            "Python Logic",
            help="Optional if-else expression (e.g., if dept == 'X': salary = ... )"
        )
    }

    df = st.data_editor(
        st.session_state.columns_df,
        column_config=column_config,
        num_rows="dynamic",
        use_container_width=True,
        key="editable_table"
    )

    updated_columns = []
    for _, row in df.iterrows():
        config = {
            "col_no": row["col_no"],
            "name": row["name"],
            "type": row["type"]
        }
        if row["type"] in ["Integer", "Float"]:
            try:
                rng = [float(v.strip()) for v in row["range/categories"].split(",")]
                if len(rng) == 2:
                    config["range"] = rng
            except:
                pass
        elif row["type"] == "Categorical":
            config["categories"] = [v.strip() for v in row["range/categories"].split(",") if v.strip()]
        elif row["type"] == "PII":
            config["subtype"] = row["range/categories"].strip() if row["range/categories"].strip() in PII_TYPES else "name"
        elif row["type"] == "Date":
            try:
                start, end = row["range/categories"].split(",")
                start_date = datetime.strptime(start.strip(), "%m-%d-%Y")
                end_date = datetime.strptime(end.strip(), "%m-%d-%Y")
                config["range"] = [start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")]
            except:
                pass

        if row["logic"]:
            config["logic"] = row["logic"]

        updated_columns.append(config)

    st.subheader("🔍 Parsed Schema Preview")
    st.json(updated_columns)

    return updated_columns
