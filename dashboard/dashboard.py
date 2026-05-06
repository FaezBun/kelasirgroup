import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# Konfigurasi Tema Futuristik
st.set_page_config(page_title="Insight Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #00f2ff; text-transform: uppercase; letter-spacing: 2px; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Insight Dashboard")

# Fungsi Sambungan Database & Penyusunan Data
def get_data():
    try:
        conn = mysql.connector.connect(
            host="mysql_db", 
            user="root", 
            password="rootpassword", 
            database="socket_db"
        )
        # Ambil data
        df = pd.read_sql("SELECT user, points FROM user_points", conn)
        conn.close()
        
        # Senarai susunan tersuai (Custom Order)
        custom_order = [
            'c1_user', 'c2_user', 'c3_user', 'c4_user', 'c5_user', 'c6_user', 'c7_user', 'c8_user', 'c9_user',
            'py1_user', 'py2_user', 'py3_user', 'py4_user', 'py5_user', 'py6_user', 'py7_user', 'py8_user', 'py9_user'
        ]
        
        # Pastikan data dalam DataFrame mengikut urutan 'custom_order'
        # Hanya ambil kategori yang wujud dalam DB untuk mengelak ralat
        existing_categories = [u for u in custom_order if u in df['user'].values]
        
        # Tukar kepada categorical type untuk penyusunan yang tepat
        df['user'] = pd.Categorical(df['user'], categories=existing_categories, ordered=True)
        df = df.sort_values('user')
        
        return df
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return pd.DataFrame(columns=['user', 'points'])

# Load Data
df = get_data()

# Layout Dashboard
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("System Performance Grid")
    if not df.empty:
        # Guna Plotly untuk graf yang futuristik
        fig = px.bar(df, x='user', y='points', color='points',
                     color_continuous_scale='Viridis', template='plotly_dark')
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Tiada data ditemui dalam pangkalan data.")

with col2:
    st.subheader("Statistics Summary")
    st.metric("Total Active Nodes", len(df))
    if not df.empty:
        st.metric("Total Cumulative Points", int(df['points'].sum()))
    
    if st.button('FORCE REFRESH'):
        st.rerun()

st.info("Sistem sedang memantau trafik rangkaian secara *real-time*.")
