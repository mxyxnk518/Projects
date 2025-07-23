import streamlit as st
import pandas as pd
from sqlalchemy import text
from utils.db import Session, engine, init_db
from utils.dark_mode_styles import apply_dark_mode, create_navigation_sidebar

st.set_page_config(
    page_title="PrePersona - DEBUG",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply dark mode styling
apply_dark_mode()

st.title("Database Debug View")
st.write("View tables and data in the database")

# Security warning
st.warning("This page is for debugging only. It provides direct access to your database.")

# Function to execute SQL queries
def execute_query(query):
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            return result.fetchall(), result.keys()
    except Exception as e:
        st.error(f"Error executing query: {str(e)}")
        return None, None

# List available tables
st.subheader("Available Tables")

try:
    if 'sqlite' in str(engine.url):
        # SQLite
        rows, cols = execute_query("SELECT name FROM sqlite_master WHERE type='table'")
        if rows:
            tables = [row[0] for row in rows]
    else:
        # PostgreSQL
        rows, cols = execute_query("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        if rows:
            tables = [row[0] for row in rows]
    
    if 'tables' in locals():
        st.write("Tables in the database:")
        for table in tables:
            st.write(f"- {table}")
    else:
        st.info("No tables found in the database.")
except Exception as e:
    st.error(f"Error listing tables: {str(e)}")

# Select a table to view
table_to_view = st.selectbox("Select table to view:", 
                            ['users', 'user_data', 'personality_profiles', 
                             'vector_stores', 'conversation_history'])

if st.button("View Table Data"):
    try:
        rows, cols = execute_query(f"SELECT * FROM {table_to_view}")
        if rows and cols:
            # Convert to DataFrame for better display
            df = pd.DataFrame(rows, columns=cols)
            st.subheader(f"Data in {table_to_view}")
            st.dataframe(df)
            
            # Show row count
            st.write(f"Total rows: {len(df)}")
        else:
            st.info(f"No data found in table {table_to_view}")
    except Exception as e:
        st.error(f"Error viewing table: {str(e)}")

# Custom SQL query section
st.subheader("Custom SQL Query")
st.write("Enter a custom SQL query to execute:")

query = st.text_area("SQL Query", "SELECT * FROM users LIMIT 10")

if st.button("Execute Query"):
    if query:
        try:
            rows, cols = execute_query(query)
            if rows and cols:
                # Convert to DataFrame for better display
                df = pd.DataFrame(rows, columns=cols)
                st.subheader("Query Result")
                st.dataframe(df)
                
                # Show row count
                st.write(f"Total rows: {len(df)}")
            else:
                st.info("No results returned by the query.")
        except Exception as e:
            st.error(f"Error executing query: {str(e)}")
    else:
        st.warning("Please enter a SQL query to execute.")

# Database file location info
st.subheader("Database Information")
st.code(f"Database URL: {engine.url}")
if 'sqlite' in str(engine.url):
    st.write("The SQLite database file is located at:")
    st.code("prepersona.db (in the root directory)")
else:
    st.write("Using PostgreSQL database from Replit environment.")