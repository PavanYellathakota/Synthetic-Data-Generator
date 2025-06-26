# ui/options_panel.py
import streamlit as st

def options_panel_ui(schema):
    st.markdown("### ⚙️ Dataset Options")

    with st.expander("🔀 Data Distributions & Noise"):
        distribution = st.selectbox("Default Distribution", ["Uniform", "Normal", "Skewed"], index=0)
        null_injection = st.slider("% Null Values", 0, 30, 0)
        outlier_injection = st.slider("% Outliers", 0, 10, 0)

    with st.expander("🔐 PII Generation Settings"):
        enable_pii = st.checkbox("Enable Synthetic PII Generation", value=True)
        locale = st.selectbox("Locale for Names/Addresses", ["en_US", "en_IN", "en_GB"], index=0)

    schema["options"] = {
        "distribution": distribution,
        "null_percentage": null_injection,
        "outlier_percentage": outlier_injection,
        "enable_pii": enable_pii,
        "locale": locale
    }

    return schema
