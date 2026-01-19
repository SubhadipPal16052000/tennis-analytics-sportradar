from db_config import DB_CONNECT_ARGS
import os
import requests
import psycopg
from psycopg.extras import execute_values

# -----------------------------
# CONFIGURATION
# -----------------------------
API_KEY = os.getenv("SPORTRADAR_API_KEY")
if not API_KEY:
    raise ValueError("SPORTRADAR_API_KEY is not set")

API_URL = "https://api.sportradar.com/tennis/trial/v3/en/complexes.json"


# -----------------------------
# FETCH DATA FROM API
# -----------------------------
def fetch_data():
    response = requests.get(
        API_URL,
        params={"api_key": API_KEY},
        timeout=300
    )
    response.raise_for_status()
    return response.json()

# -----------------------------
# STORE DATA INTO DATABASE
# -----------------------------
def store_data(data):
    complexes = []
    venues = []

    for comp in data.get("complexes", []):
        complex_id = comp["id"]
        complexes.append((complex_id, comp["name"]))

        for venue in comp.get("venues", []):
            venues.append((
                venue["id"],
                venue["name"],
                venue.get("city", {}).get("name", "Unknown"),
                venue.get("country", {}).get("name", "Unknown"),
                venue.get("country", {}).get("code", "UNK"),
                venue.get("timezone", "Unknown"),
                complex_id
            ))

    conn = psycopg.connect(**DB_CONNECT_ARGS)
    cur = conn.cursor()

    execute_values(
        cur,
        """
        INSERT INTO complexes (complex_id, complex_name)
        VALUES %s
        ON CONFLICT (complex_id) DO NOTHING
        """,
        complexes
    )

    execute_values(
        cur,
        """
        INSERT INTO venues
        (venue_id, venue_name, city_name, country_name, country_code, timezone, complex_id)
        VALUES %s
        ON CONFLICT (venue_id) DO NOTHING
        """,
        venues
    )

    conn.commit()
    cur.close()
    conn.close()


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    print("Fetching complexes data...")
    data = fetch_data()
    store_data(data)
    print("Complexes & venues stored successfully.")
