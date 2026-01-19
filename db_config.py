import os
import streamlit as st

def get_env(key, default=None):
    # Streamlit Cloud
    if hasattr(st, "secrets") and key in st.secrets:
        return st.secrets[key]
    # Local
    return os.getenv(key, default)

DB_CONNECT_ARGS = {
    "host": get_env("DB_HOST", "localhost"),
    "dbname": get_env("DB_NAME", "sportradar_db"),
    "user": get_env("DB_USER", "postgres"),
    "password": get_env("DB_PASSWORD", ""),
    "port": int(get_env("DB_PORT", 5432)),
}

# Neon requires SSL
if DB_CONNECT_ARGS["host"] != "localhost":
    DB_CONNECT_ARGS["sslmode"] = "require"
