import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2
import os
import subprocess
import sys
# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="🎾 Tennis Analytics Dashboard",
    layout="wide"
)

st.title("🎾 Tennis Analytics Dashboard")
st.caption("Real time Game Analytics: Unlocking Tennis Data with SportRadar API")

# ==================================================
# 2. AUTO-RUN ETL WHEN APP STARTS (ONCE PER SESSION)
# ==================================================
if "etl_ran" not in st.session_state:
    st.session_state.etl_ran = False

if not st.session_state.etl_ran:
    with st.spinner("Fetching latest data from SportRadar API..."):
        try:
            subprocess.run(
                [sys.executable, "ETL.py"],
                check=True
            )
            st.session_state.etl_ran = True
            st.success("Latest data loaded successfully")
        except Exception as e:
            st.error("ETL failed while fetching data")
            st.exception(e)

# ==================================================
# MANUAL REFRESH BUTTON (SIDEBAR)
# ==================================================
with st.sidebar:
    st.header("Data Controls")

    if st.button("Refresh Data (Run ETL)"):
        with st.spinner("Refreshing data from API..."):
            try:
                subprocess.run(
                    [sys.executable, "ETL.py"],
                    check=True
                )
                st.success("Data refreshed successfully")
            except Exception as e:
                st.error("Data refresh failed")
                st.exception(e)

# ==================================================
# DATABASE HELPER
# ==================================================
def run_query(query):
    conn = psycopg2.connect(
        dbname="sportradar_db",
        user="postgres",
        password=os.getenv("DB_PASSWORD"),
        host="localhost",
        port="5432"
    )
    try:
        return pd.read_sql(query, conn)
    finally:
        conn.close()

# ==================================================
# KPI CARDS (KPIs)
# ==================================================
st.subheader("📌 Key Performance Indicators")

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("Competitions", run_query("SELECT COUNT(*) FROM competitions").iloc[0, 0])
k2.metric("Categories", run_query("SELECT COUNT(*) FROM categories").iloc[0, 0])
k3.metric("Venues", run_query("SELECT COUNT(*) FROM venues").iloc[0, 0])
k4.metric("Complexes", run_query("SELECT COUNT(*) FROM complexes").iloc[0, 0])
k5.metric("Competitors", run_query("SELECT COUNT(*) FROM competitors").iloc[0, 0])

st.divider()
# ==================================================
# TABS
# ==================================================
tabs = st.tabs([
    "📊 Dashboard",
    "📈 Weekly Ranking Trend",
    "🧪 SQL Query Runner"
])

# ==================================================
# 📊 DASHBOARD TAB (ENHANCED CHARTS PER ROW)
# ==================================================
with tabs[0]:
    st.subheader("📊 Key Tennis Insights")

    # ---------- ROW 1 ----------
    col1, col2 = st.columns(2)

    with col1:
        df_comp_cat = run_query("SELECT * FROM Number_of_competitions_in_each_category")
        st.markdown("### Competitions per Category")
        st.plotly_chart(
            px.bar(
                df_comp_cat,
                x="category_name",
                y="total_competitions"
            ),
            use_container_width=True
        )

    with col2:
        df_comp_gender = run_query("SELECT * FROM Competitions_by_gender")
        st.markdown("### Competitions by Gender")
        st.plotly_chart(
            px.pie(
                df_comp_gender,
                names="gender",
                values="total_competitions"
            ),
            use_container_width=True
        )

    # ---------- ROW 2 ----------
    col3, col4 = st.columns(2)

    with col3:
        df_venues_complex = run_query("SELECT * FROM All_venues_by_complex")
        st.markdown("### Venues per Complex")
        st.plotly_chart(
            px.bar(
                df_venues_complex,
                x="complex_name",
                y="total_venues"
            ),
            use_container_width=True
        )

    with col4:
        df_timezone = run_query("SELECT * FROM All_venues_by_country_timezone")
        st.markdown("### Venues by Timezone")
        st.plotly_chart(
            px.pie(
                df_timezone,
                names="timezone",
                values="venue_count"
            ),
            use_container_width=True
        )

    # ---------- ROW 3 ----------
    col5, col6 = st.columns(2)

    with col5:
        df_rank = run_query("SELECT * FROM Competitors_rank_and_points")
        st.markdown("### Rank vs Points")
        fig = px.scatter(
            df_rank,
            x="rank",
            y="points",
            color="country"
        )
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)

    with col6:
        df_top = run_query("SELECT * FROM Top_5_competitors_ranked")
        st.markdown("### Top Competitors by Points")
        st.plotly_chart(
            px.bar(
                df_top,
                x="name",
                y="points"
            ),
            use_container_width=True
        )

    # ---------- ROW 4 ----------
    col7, col8 = st.columns(2)

    with col7:
        df_country = run_query("SELECT * FROM Number_of_competitors_per_country")
        st.markdown("### Top Countries by Competitors")
        st.plotly_chart(
            px.bar(
                df_country.head(10),
                x="country",
                y="competitor_count"
            ),
            use_container_width=True
        )

    with col8:
        df_active = run_query("SELECT * FROM Most_active_competitors")
        st.markdown("### Most Active Competitors")
        st.plotly_chart(
            px.bar(
                df_active,
                x="name",
                y="competitions_played"
            ),
            use_container_width=True
        )

# ==================================================
# WEEKLY RANKING TREND
# ==================================================
with tabs[1]:
    st.subheader("📈 Weekly Ranking Trend")

    players = run_query("SELECT DISTINCT name FROM competitors ORDER BY name")
    selected_player = st.selectbox("Select Competitor", players["name"].tolist())

    trend_query = f"""
    SELECT r.ranking_week, r.rank
    FROM competitor_rankings r
    JOIN competitors c
        ON r.competitor_id = c.competitor_id
    WHERE c.name = '{selected_player}'
    ORDER BY r.ranking_week
    """

    trend_df = run_query(trend_query)

    if not trend_df.empty:
        fig = px.line(
            trend_df,
            x="ranking_week",
            y="rank",
            markers=True
        )
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No weekly ranking data available.")

# ==================================================
# 🧪 SQL QUERY RUNNER
# ==================================================
with tabs[2]:
    st.subheader("🧪 SQL Query Runner")

    QUERY_MAP = {
        "1.Competitions along with their category name":"SELECT * FROM All_competitions_with_category",
        "2.Competitions per Category": "SELECT * FROM Number_of_competitions_in_each_category",
        "3.All competitions of type 'doubles'": "SELECT * FROM Double_type_competitions",
        "4.Competitions that belong to a specific category": "SELECT * FROM Specific_category_competitions",
        "5.Parent competitions and their sub-competitions": "SELECT * FROM Parent_child_competitions",
        "6.Distribution of competition types by category": "SELECT * FROM Distribution_of_competition_types_by_category",
        "7.Top-level competitions": "SELECT * FROM Top_level_competitions",
        "8.All venues along with associated complex name": "SELECT * FROM Associated_venue_complex_name",
        "9.Count the number of venues in each complex": "SELECT * FROM Number_of_venues_in_each_complex",
        "10.Details of venues in a specific country": "SELECT * FROM Specific_country_venue_details",
        "11.Identify all venues and their timezones": "SELECT * FROM All_venues_with_timezones",
        "12.Complexes that have more than one venue": "SELECT * FROM Complexes_more_than_one_venue",
        "13.List venues grouped by country(TIMEZONES)": "SELECT * FROM All_venues_by_country_timezone",
        "14.All venues for a specific complex": "SELECT * FROM Venues_by_specific_complex",
        "15.All competitors with their rank and points": "SELECT * FROM Competitors_rank_and_points",
        "16.Competitors ranked in the top 5": "SELECT * FROM Top_5_competitors_ranked",
        "17.List competitors with no rank movement (stable rank)": "SELECT * FROM Stable_rank_competitors",
        "18.Total points of competitors from a specific country": "SELECT * FROM Competitors_Total_points_from_specific_country",
        "19.Find competitors with the highest points in the current week": "SELECT * FROM Current_week_competitors_highest_points",
        "20.Count the number of competitors per country": "SELECT * FROM Number_of_competitors_per_country",
        "21.All venues for with complex name": "SELECT * FROM  All_venues_by_complex",
        "22.Count competitions by gender": "SELECT * FROM Competitions_by_gender",
        "23.Categories with more than 10 competitions": "SELECT * FROM Categories_with_many_competitions",
        "24.Distribution of competitions by type": "SELECT * FROM Competition_type_distribution",
        "25.List venues missing city information": "SELECT * FROM  Venues_missing_city",
        "26.Venue distribution percentage by timezone": "SELECT * FROM Venue_distribution_percentage",
        "27.Best ranked competitor per country": "SELECT * FROM Best_ranked_competitor_per_country",
        "28.Competitors who improved ranking": "SELECT * FROM Improved_rank_competitors",
        "29.Average points by country": "SELECT * FROM Avg_points_by_country",
        "30.Competitors with highest competitions played": "SELECT * FROM Most_active_competitors"
    }

    selected_query = st.selectbox("Select Query", list(QUERY_MAP.keys()))
    sql = QUERY_MAP[selected_query]

    if st.button("▶ Run Query"):
        df = run_query(sql)
        st.dataframe(df, use_container_width=True)

        num_cols = df.select_dtypes(include="number").columns
        cat_cols = df.select_dtypes(exclude="number").columns

        if len(num_cols) > 0 and len(cat_cols) > 0:
            st.plotly_chart(
                px.bar(df.head(20), x=cat_cols[0], y=num_cols[0]),
                use_container_width=True
            )

st.success("Dashboard loaded successfully by TEAM")
st.success(f"Connected to DB Host: {os.getenv('DB_HOST')}")
