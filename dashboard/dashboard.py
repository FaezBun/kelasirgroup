import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# Konfigurasi Tema Futuristik
st.set_page_config(page_title="LOC8 Ops Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #00f2ff; text-transform: uppercase; letter-spacing: 2px; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 LOC8 Real-Time Analytics")

# Fungsi Sambungan Database
def get_data():
    conn = mysql.connector.connect(
        host="mysql_db", user="root", password="rootpassword", database="socket_db"
    )
    return pd.read_sql("SELECT user, points FROM user_points", conn)

# Load Data
df = get_data()

# Layout Dashboard
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("System Performance Grid")
    # Guna Plotly untuk graf yang futuristik
    fig = px.bar(df, x='user', y='points', color='points',
                 color_continuous_scale='Viridis', template='plotly_dark')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Statistics Summary")
    st.metric("Total Active Nodes", len(df))
    st.metric("Total Cumulative Points", df['points'].sum())
    if st.button('FORCE REFRESH'):
        st.rerun()

st.info("Sistem sedang memantau trafik rangkaian secara *real-time*.")
