from db_config import DB_CONFIG

import os
import requests
import psycopg
from psycopg2.extras import execute_values

# -----------------------------
# CONFIGURATION
# -----------------------------
API_KEY = os.getenv("SPORTRADAR_API_KEY")
if not API_KEY:
    raise ValueError("SPORTRADAR_API_KEY is not set")

API_URL = "https://api.sportradar.com/tennis/trial/v3/en/competitions.json"


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
    categories = {}
    competitions = []

    for comp in data.get("competitions", []):
        category = comp.get("category")
        if not category:
            continue

        category_id = category.get("id")
        categories[category_id] = category.get("name")

        competitions.append({
            "competition_id": comp.get("id"),
            "competition_name": comp.get("name"),
            "parent_id": comp.get("parent_id"),
            "type": comp.get("type", "unknown"),
            "gender": comp.get("gender", "unknown"),
            "category_id": category_id
        })

    conn = psycopg.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Insert categories
    execute_values(
        cur,
        """
        INSERT INTO categories (category_id, category_name)
        VALUES %s
        ON CONFLICT (category_id) DO NOTHING
        """,
        [(k, v) for k, v in categories.items()]
    )

    # Insert competitions WITHOUT parent_id
    execute_values(
        cur,
        """
        INSERT INTO competitions
        (competition_id, competition_name, parent_id, type, gender, category_id)
        VALUES %s
        ON CONFLICT (competition_id) DO NOTHING
        """,
        [
            (
                c["competition_id"],
                c["competition_name"],
                None,
                c["type"],
                c["gender"],
                c["category_id"]
            )
            for c in competitions
        ]
    )

    # Update parent_id ONLY IF PARENT EXISTS
    cur.execute("SELECT competition_id FROM competitions")
    existing_ids = {row[0] for row in cur.fetchall()}

    for c in competitions:
        parent_id = c["parent_id"]
        if parent_id and parent_id in existing_ids:
            cur.execute(
                """
                UPDATE competitions
                SET parent_id = %s
                WHERE competition_id = %s
                """,
                (parent_id, c["competition_id"])
            )

    conn.commit()
    cur.close()
    conn.close()


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    print("Fetching competitions data...")
    data = fetch_data()
    store_data(data)
    print("Competitions data stored successfully.")
    
import os
print("ETL DB HOST:", os.getenv("DB_HOST"))
