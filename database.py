import mysql.connector

def connect_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="abcd",
        database="schema_project"
    )
    return connection

def setup_database():
    conn = connect_db()
    cursor = conn.cursor()

    # Drop and recreate users table fresh
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("""
        CREATE TABLE users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            age VARCHAR(20)
        )
    """)

    # Drop and recreate audit log table fresh
    cursor.execute("DROP TABLE IF EXISTS audit_log")
    cursor.execute("""
        CREATE TABLE audit_log (
            id INT AUTO_INCREMENT PRIMARY KEY,
            action VARCHAR(50),
            column_name VARCHAR(100),
            column_type VARCHAR(50),
            status VARCHAR(20),
            changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("Database setup complete!")

if __name__ == "__main__":
    setup_database()
