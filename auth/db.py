# auth/db.py

import mysql.connector
import os
import streamlit as st

# Use Streamlit secrets for database credentials
DB_HOST = st.secrets["mysql"]["host"]
DB_USER = st.secrets["mysql"]["user"]
DB_PASSWORD = st.secrets["mysql"]["password"]
DB_NAME = st.secrets["mysql"]["database"]

def get_db_connection():
    """Establishes a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Error connecting to database: {err}")
        return None

def init_db():
    """Initializes the database and creates the users table if it doesn't exist."""
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
        except mysql.connector.Error as err:
            st.error(f"Failed to create table: {err}")
        finally:
            cursor.close()
            conn.close()

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
            # Check for duplicate entry error (1062)
            if err.errno == 1062:
                st.error("Error: This email is already registered.")
            else:
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
        cursor = conn.cursor(dictionary=True) # Fetch as dictionary
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