# 🎾 Tennis Analytics Dashboard  
**End-to-End ETL & Analytics using Sportradar API, PostgreSQL, and Streamlit**

---

## 📌 Overview

This project is an **end-to-end tennis analytics platform** built using real-time data from the **Sportradar Tennis API**.  
It includes:

- A robust **ETL pipeline** to ingest, transform, and store tennis data
- A **PostgreSQL analytics database** (Neon-compatible)
- An interactive **Streamlit dashboard** for analytics and visualization
- Cloud-ready deployment with **Streamlit Cloud**

The system is designed with **production constraints in mind**, including cloud environment limitations, dependency stability, and separation of concerns.

---

## 🏗️ Architecture Overview

Sportradar API
      |
      v
 ETL Scripts (Python)
      |
      v
 PostgreSQL (Neon / Cloud DB)
      |
      v
 Streamlit Analytics Dashboard
 
---

## 📂 Project Structure

tennis-analytics-sportradar/
│
├── App.py                  # Streamlit dashboard (read-only analytics)
├── ETL.py                  # Orchestrates ETL jobs (local execution)
│
├── fetch_competitions.py   # ETL: competitions data
├── fetch_complexes.py      # ETL: complexes & venues data
├── fetch_ranking.py        # ETL: player rankings data
│
├── db_config.py            # Centralised DB configuration
├── connection.py           # Database connection helpers
│
├── tennis_schema.sql       # Database schema
├── tennis_queries.sql      # Analytical SQL queries
│
├── requirements.txt        # Python dependencies
├── runtime.txt             # Python version pin for Streamlit Cloud
│
└── .streamlit/
    └── secrets.toml        # Local secrets (not committed)


---

## 🔄 ETL Design

### Key Principles

- **ETL is isolated from the dashboard**
- **No ETL runs automatically on Streamlit Cloud**
- **ETL scripts are safe to import without side effects**

### How ETL Works

- Each `fetch_*.py` file:
  - Fetches data from the Sportradar API
  - Transforms nested JSON into a relational schema
  - Inserts data using bulk database operations
- `ETL.py` orchestrates all ETL jobs sequentially
- ETL is intended to be run:
  - Locally
  - Or via a scheduler (cron / CI / external job runner)

🚫 ETL is **disabled on Streamlit Cloud** to avoid crashes and permission issues.

---

## 📊 Streamlit Dashboard Design

### Dashboard Characteristics

- **Read-only analytics layer**
- Uses **cached SQL queries** for performance
- Does **not trigger ETL**
- Safe for public cloud deployment

### Key Features

- KPI metrics (competitions, venues, players, rankings)
- Interactive Plotly visualisations
- PostgreSQL-backed analytics queries
- Responsive wide-layout UI

---

## 🗄️ Database Layer

- PostgreSQL (Neon compatible)
- SSL-aware configuration for cloud databases
- Bulk inserts using `psycopg.extras.execute_values`
- Schema optimised for analytical queries

---

## ☁️ Cloud Deployment (Streamlit Cloud)

### Python Version Pinning

Streamlit Cloud defaults to the **latest Python version**, which can cause dependency issues.

To ensure stability, this project **pins Python 3.11**:



