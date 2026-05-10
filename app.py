import streamlit as st

st.set_page_config(
    page_title="Schema Change Strategy",
    page_icon="🗄️",
    layout="centered"
)

st.markdown("""
    <style>
        .main { background-color: #f9f9f9; }
        .block-container { padding-top: 2rem; }
        .box {
            background-color: #f0f0f0;
            border-left: 4px solid #888;
            padding: 12px 16px;
            border-radius: 6px;
            margin-bottom: 10px;
            color: #2c2c2c;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Database Schema Change Strategy")
st.markdown("<p style='color:gray;'>A system to safely manage changes in database structure without losing data.</p>", unsafe_allow_html=True)
st.markdown("---")


st.markdown("#### Strategy: Expand and Contract")
st.markdown("""
- **Expand** — Add a new column to the database safely
- **Contract** — Remove a column when it is no longer needed
- **Audit Log** — Every change is saved with date and time
- **Data Safety** — No existing data is deleted during any schema change
""")
