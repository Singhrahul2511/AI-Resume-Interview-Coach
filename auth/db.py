import mysql.connector
import os
import streamlit as st

def get_db_credentials():
    """
    Fetches database credentials from system environment variables (for Render)
    or from Streamlit secrets (for local/Streamlit Cloud).
    """
    creds = {
        "host": os.environ.get("DB_HOST") or st.secrets.get("DB_HOST"),
        "user": os.environ.get("DB_USER") or st.secrets.get("DB_USER"),
        "password": os.environ.get("DB_PASSWORD") or st.secrets.get("DB_PASSWORD"),
        "database": os.environ.get("DB_NAME") or st.secrets.get("DB_NAME")
    }
    return creds

# Get credentials
db_creds = get_db_credentials()

def get_db_connection():
    """Establishes a connection to the MySQL database."""
    if not all(db_creds.values()):
        # This error will show in the app if secrets are missing
        st.error("Database credentials are not fully configured.")
        return None
    
    try:
        conn = mysql.connector.connect(**db_creds)
        return conn
    except mysql.connector.Error as err:
        # Use print for build logs, st.error for the app
        print(f"Error connecting to database: {err}")
        st.error(f"Error connecting to database: {err}")
        return None

def init_db():
    """Initializes the database table. Called during the build process."""
    if not all(db_creds.values()):
        print("Error: Database credentials not found in environment variables. Build cannot initialize database.")
        # Exit with an error code to fail the build clearly
        exit(1)
        
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print("Database table initialized successfully.")
        except mysql.connector.Error as err:
            print(f"Failed to create table: {err}")
        finally:
            cursor.close()
            conn.close()

# The rest of your functions (add_user, get_user_by_email) remain the same...
def add_user(name, email, hashed_password):
    conn = get_db_connection()
    # ... (function body)
def get_user_by_email(email):
    conn = get_db_connection()
    # ... (function body)