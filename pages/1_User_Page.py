import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="User Registration", layout="centered")

st.markdown("""
    <style>
        .main { background-color: #f9f9f9; }
        .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

def connect_db():
    conn = sqlite3.connect("schema_project.db")
    return conn

st.title("User Registration")
st.markdown("<p style='color:gray;'>Fill in the form below to register.</p>", unsafe_allow_html=True)
st.markdown("---")

# Get current columns dynamically
conn = connect_db()
cursor = conn.cursor()

# SQLite-compatible query
cursor.execute("PRAGMA table_info(users)")

# Extract column names
all_columns = [col[1] for col in cursor.fetchall()]

conn.close()

# Fixed fields
name  = st.text_input("Full Name")
email = st.text_input("Email Address")
age   = st.text_input("Age")

# Extra fields added by admin
extra_columns = [c for c in all_columns if c not in ["id", "name", "email", "age"]]
extra_values  = {}
if extra_columns:
    st.markdown("**Additional Fields:**")
    for col in extra_columns:
        extra_values[col] = st.text_input(col.replace("_", " ").title())

st.markdown("")

if st.button("Register"):
    if not name or not email or not age:
        st.error("Please fill in all required fields.")
    else:
        try:
            conn2  = connect_db()
            cursor2 = conn2.cursor()

            if extra_columns:
                cols         = ["name", "email", "age"] + extra_columns
                placeholders = ", ".join(["%s"] * len(cols))
                col_str      = ", ".join(cols)
                vals         = [name, email, age] + [extra_values[c] for c in extra_columns]
                cursor2.execute(f"INSERT INTO users ({col_str}) VALUES ({placeholders})", vals)
            else:
                cursor2.execute(
                    "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)",
                    (name, email, age)
                )

            conn2.commit()
            conn2.close()
            st.success(f"User '{name}' registered successfully.")
        except Exception as e:
            st.error(f"Error: {e}")

