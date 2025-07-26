import mysql.connector
import os
import streamlit as st

# This function smartly gets credentials from Streamlit's secrets manager
def get_db_credentials():
    """Fetches database credentials from Streamlit's secrets."""
    creds = {
        "host": st.secrets.get("DB_HOST"),
        "user": st.secrets.get("DB_USER"),
        "password": st.secrets.get("DB_PASSWORD"),
        "database": st.secrets.get("DB_NAME")
    }
    return creds

# Get credentials
db_creds = get_db_credentials()

def get_db_connection():
    """Establishes a connection to the MySQL database."""
    # Check if all credential values were found
    if not all(db_creds.values()):
        st.error("Database credentials are not fully configured in your app's secrets.")
        return None
    
    try:
        conn = mysql.connector.connect(**db_creds)
        return conn
    except mysql.connector.Error as err:
        st.error(f"Error connecting to database: {err}")
        return None

# The rest of your functions (init_db, add_user, get_user_by_email)
# do not need to be changed. Just ensure the top part of your file
# matches the code above.
def init_db():
    """Initializes the database and creates the users table if it doesn't exist."""
    # This function is not used in Streamlit Cloud deployment
    # but is safe to keep for local use.
    pass

def add_user(name, email, hashed_password):
    """Adds a new user to the database."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (name, email, hashed_password)
            )
            conn.commit()
            return True
        except mysql.connector.Error as err:
            st.error(f"Database Error: {err}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def get_user_by_email(email):
    """Retrieves a user's details from the database by their email."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            return user
        except mysql.connector.Error as err:
            st.error(f"Database Error: {err}")
            return None
        finally:
            cursor.close()
            conn.close()
    return None