import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Admin Dashboard", layout="centered")

st.markdown("""
    <style>
        .main { background-color: #f9f9f9; }
        .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)


# ── Database Connection ───────────────────────────────────────────────────────
def connect_db():
    conn = sqlite3.connect("schema_project.db")
    return conn


# ── Helper Function: Get Columns ──────────────────────────────────────────────
def get_columns(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    return cursor.fetchall()


st.title("Admin Dashboard")
st.markdown(
    "<p style='color:gray;'>Manage database schema and monitor all changes.</p>",
    unsafe_allow_html=True
)

st.markdown("---")


# ── Users Data ────────────────────────────────────────────────────────────────
st.markdown("#### Current Users")

try:
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()

    columns_info = get_columns(cursor, "users")
    columns = [c[1] for c in columns_info]

    conn.close()

    if data:
        st.table(pd.DataFrame(data, columns=columns))
    else:
        st.info("No users registered yet.")

except Exception as e:
    st.error(f"Error: {e}")

st.markdown("---")


# ── Current Schema ────────────────────────────────────────────────────────────
st.markdown("#### Current Schema")

try:
    conn = connect_db()
    cursor = conn.cursor()

    schema_data = get_columns(cursor, "users")

    conn.close()

    schema_rows = []

    for col in schema_data:
        schema_rows.append({
            "Column": col[1],
            "Type": col[2],
            "Not Null": "YES" if col[3] else "NO",
            "Primary Key": "YES" if col[5] else "NO"
        })

    schema_df = pd.DataFrame(schema_rows)

    st.table(schema_df)

except Exception as e:
    st.error(f"Error: {e}")

st.markdown("---")


# ── Schema Changes ────────────────────────────────────────────────────────────
st.markdown("#### Schema Changes")

col1, col2 = st.columns(2)


# ── Add Column ────────────────────────────────────────────────────────────────
with col1:
    st.markdown("**Expand — Add Column**")

    new_col = st.text_input("Column name", key="add_col")

    new_type = st.selectbox(
        "Column type",
        ["TEXT", "INTEGER", "REAL", "DATE"],
        key="add_type"
    )

    if st.button("Add Column"):

        if not new_col:
            st.error("Enter a column name.")

        else:
            try:
                conn = connect_db()
                cursor = conn.cursor()

                existing_columns = get_columns(cursor, "users")
                existing = [c[1] for c in existing_columns]

                if new_col in existing:
                    st.error(f"Column '{new_col}' already exists.")

                else:
                    cursor.execute(
                        f"ALTER TABLE users ADD COLUMN {new_col} {new_type}"
                    )

                    cursor.execute("""
                        INSERT INTO audit_log 
                        (action, column_name, column_type, status)
                        VALUES (?, ?, ?, ?)
                    """, (
                        "ADD COLUMN",
                        new_col,
                        new_type,
                        "SUCCESS"
                    ))

                    conn.commit()
                    conn.close()

                    st.success(
                        f"Column '{new_col}' added. Existing data is safe."
                    )

                    st.rerun()

            except Exception as e:
                st.error(f"Error: {e}")


# ── Remove Column ─────────────────────────────────────────────────────────────
with col2:
    st.markdown("**Contract — Remove Column**")

    try:
        conn = connect_db()
        cursor = conn.cursor()

        all_columns_info = get_columns(cursor, "users")
        all_cols = [c[1] for c in all_columns_info]

        conn.close()

        protected = ["id", "name", "email", "age"]

        removable = [c for c in all_cols if c not in protected]

    except:
        removable = []

    if removable:

        rem_col = st.selectbox(
            "Select column to remove",
            removable,
            key="rem_col"
        )

        if st.button("Remove Column"):

            try:
                conn = connect_db()
                cursor = conn.cursor()

                # SQLite supports DROP COLUMN only in newer versions
                cursor.execute(f"ALTER TABLE users DROP COLUMN {rem_col}")

                cursor.execute("""
                    INSERT INTO audit_log
                    (action, column_name, column_type, status)
                    VALUES (?, ?, ?, ?)
                """, (
                    "REMOVE COLUMN",
                    rem_col,
                    "-",
                    "SUCCESS"
                ))

                conn.commit()
                conn.close()

                st.success(
                    f"Column '{rem_col}' removed. Other data is safe."
                )

                st.rerun()

            except Exception as e:
                st.error(f"Error: {e}")

    else:
        st.markdown("""
            <p style='color:gray; font-size:14px;'>
                No extra columns to remove.<br>
                Original columns are protected.
            </p>
        """, unsafe_allow_html=True)

st.markdown("---")


# ── Audit Log ─────────────────────────────────────────────────────────────────
st.markdown("#### Audit Log")

st.markdown("""
    <p style='color:gray; font-size:14px;'>
        Record of all schema changes made.
    </p>
""", unsafe_allow_html=True)

try:
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM audit_log
        ORDER BY changed_at DESC
    """)

    logs = cursor.fetchall()

    conn.close()

    if logs:
        log_df = pd.DataFrame(
            logs,
            columns=[
                "ID",
                "Action",
                "Column",
                "Type",
                "Status",
                "Timestamp"
            ]
        )

        st.table(log_df)

    else:
        st.info("No changes recorded yet.")

except Exception as e:
    st.error(f"Error loading audit log: {e}")