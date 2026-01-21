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

flowchart LR
    A[Sportradar Tennis API] --> B[ETL Scripts<br/>(Python)]
    B --> C[(PostgreSQL<br/>Neon / Cloud DB)]
    C --> D[Streamlit Analytics Dashboard]

    Subgraph ETL Layer
        B1[fetch_competitions.py]
        B2[fetch_complexes.py]
        B3[fetch_ranking.py]
    end

    B --> B1
    B --> B2
    B --> B3

 
---

## 📂 Project Structure

flowchart TB
    R[tennis-analytics-sportradar]

    R --> A[App.py<br/>Streamlit Dashboard]
    R --> E[ETL.py<br/>ETL Orchestrator]

    R --> F1[fetch_competitions.py]
    R --> F2[fetch_complexes.py]
    R --> F3[fetch_ranking.py]

    R --> D1[db_config.py]
    R --> D2[connection.py]

    R --> S1[tennis_schema.sql]
    R --> S2[tennis_queries.sql]

    R --> C1[requirements.txt]
    R --> C2[runtime.txt]

    R --> ST[.streamlit]
    ST --> SEC[secrets.toml<br/>(not committed)]



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



