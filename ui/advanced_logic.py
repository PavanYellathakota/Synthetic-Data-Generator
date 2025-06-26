# ui/advanced_logic.py
import streamlit as st

def advanced_logic_ui(schema):
    st.markdown("### 🧠 Advanced Column Dependencies & Logic")

    if "dependencies" not in st.session_state:
        st.session_state.dependencies = schema.get("dependencies", [])

    updated_dependencies = []

    for idx, rule in enumerate(st.session_state.dependencies):
        with st.expander(f"Rule {idx+1}: {rule.get('target', 'Unknown')}"):
            target_col = st.text_input(f"Target Column {idx+1}", value=rule.get("target", ""), key=f"dep_target_{idx}")
            condition_expr = st.text_input(f"Condition Expression {idx+1}", value=rule.get("condition", ""), key=f"dep_cond_{idx}")
            result_value = st.text_input(f"Value If True {idx+1}", value=rule.get("value", ""), key=f"dep_val_{idx}")

            updated_dependencies.append({
                "target": target_col,
                "condition": condition_expr,
                "value": result_value
            })

    if st.button("➕ Add New Logic Rule"):
        st.session_state.dependencies.append({"target": "", "condition": "", "value": ""})

    schema["dependencies"] = updated_dependencies
    return schema
