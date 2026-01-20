from db_config import DB_CONNECT_ARGS
import os
import requests
import psycopg
# pyright: reportMissingImports=false
from psycopg.extras import execute_values
from datetime import date

# -----------------------------
# CONFIGURATION
# -----------------------------
API_KEY = os.getenv("SPORTRADAR_API_KEY")
if not API_KEY:
    raise ValueError("SPORTRADAR_API_KEY is not set")

DOUBLES_URL = "https://api.sportradar.com/tennis/trial/v3/en/doubles-competitor-rankings.json"
SINGLES_URL = "https://api.sportradar.com/tennis/trial/v3/en/rankings.json"


# -----------------------------
# FETCH DATA (WITH FALLBACK)
# -----------------------------
def fetch_data():
    # Try doubles rankings
    response = requests.get(
        DOUBLES_URL,
        params={"api_key": API_KEY},
        timeout=300
    )

    if response.status_code == 200:
        print("Using DOUBLES rankings endpoint")
        return response.json()

    if response.status_code == 404:
        print("Doubles rankings not available. Falling back to singles rankings.")

    else:
        response.raise_for_status()

    # Fallback to singles rankings
    response = requests.get(
        SINGLES_URL,
        params={"api_key": API_KEY},
        timeout=300
    )
    response.raise_for_status()
    print("Using SINGLES rankings endpoint")
    return response.json()

# -----------------------------
# STORE DATA
# -----------------------------
def store_data(data):
    competitors = []
    rankings = []

    for group in data.get("rankings", []):
        year = group.get("year")
        week = group.get("week")

        try:
            ranking_week = date.fromisocalendar(year, week, 1)
        except Exception:
            ranking_week = None

        for item in group.get("competitor_rankings", []):
            comp = item.get("competitor")
            if not comp:
                continue

            competitor_id = comp.get("id")
            if not competitor_id:
                continue

            # Country can be dict or string
            country_data = comp.get("country")
            if isinstance(country_data, dict):
                country_name = country_data.get("name", "Unknown")
                country_code = country_data.get("code", "UNK")
            elif isinstance(country_data, str):
                country_name = country_data
                country_code = "UNK"
            else:
                country_name = "Unknown"
                country_code = "UNK"

            competitors.append((
                competitor_id,
                comp.get("name", "Unknown"),
                country_name,
                country_code,
                comp.get("abbreviation", comp.get("name", "UNK")[:10].upper())
            ))

            rankings.append((
                item.get("rank"),
                item.get("movement", 0),
                item.get("points", 0),
                item.get("competitions_played", 0),
                competitor_id,
                ranking_week
            ))

    conn = psycopg.connect(**DB_CONNECT_ARGS)
    cur = conn.cursor()

    execute_values(
        cur,
        """
        INSERT INTO competitors
        (competitor_id, name, country, country_code, abbreviation)
        VALUES %s
        ON CONFLICT (competitor_id) DO NOTHING
        """,
        competitors
    )

    execute_values(
        cur,
        """
        INSERT INTO competitor_rankings
        (rank, movement, points, competitions_played, competitor_id, ranking_week)
        VALUES %s
        """,
        rankings
    )

    conn.commit()
    cur.close()
    conn.close()

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    print("Fetching competitor rankings...")
    data = fetch_data()
    store_data(data)
    print("Competitor rankings stored successfully.")
