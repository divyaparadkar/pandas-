import streamlit as st
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Anime Data Analytics", layout="wide")

# --- DATA PROCESSING FUNCTIONS ---
def extract_episodes(txt):
    try:
        start = txt.find('(') + 1
        end = txt.find(' eps)')
        return int(txt[start:end])
    except:
        return 0

def extraction_time(txt):
    try:
        end_paren = txt.find(')')
        # Extract approximately 20 characters after the closing parenthesis
        return txt[end_paren+1 : end_paren+20].strip()
    except:
        return ""

def calculate_total_months(period):
    try:
        start_str, end_str = period.split(' - ')
        start_date = datetime.strptime(start_str.strip(), '%b %Y')
        end_date = datetime.strptime(end_str.strip(), '%b %Y')
        r = relativedelta(end_date, start_date)
        return r.years * 12 + r.months + 1
    except:
        return 0

# --- APP LAYOUT ---
st.title("🎬 Anime Data Insights")
st.markdown("Exploring the highest-rated and longest-running anime series.")

# Sidebar for Upload
uploaded_file = st.sidebar.file_uploader("Upload your anime.csv", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Apply your logic
    df['Episodes'] = df['Title'].apply(extract_episodes)
    df['Total Time'] = df['Title'].apply(extraction_time)
    df['Months'] = df['Total Time'].apply(calculate_total_months)
    
    # --- METRICS ---
    col1, col2, col3 = st.columns(3)
    
    highest_score_row = df.loc[df['Score'].idxmax()]
    longest_run_row = df.loc[df['Months'].idxmax()]
    most_episodes_row = df.loc[df['Episodes'].idxmax()]

    col1.metric("Top Rated", highest_score_row['Score'], highest_score_row['Title'][:20] + "...")
    col2.metric("Longest Duration", f"{longest_run_row['Months']} Mos", longest_run_row['Title'][:20] + "...")
    col3.metric("Most Episodes", most_episodes_row['Episodes'], most_episodes_row['Title'][:20] + "...")

    # --- TABS FOR VISUALIZATION ---
    tab1, tab2 = st.tabs(["📊 Leaderboards", "🔍 Raw Data"])

    with tab1:
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("Top 5 by Score")
            st.table(df.nlargest(5, 'Score')[['Title', 'Score']])
            
        with c2:
            st.subheader("Top 5 by Duration (Months)")
            st.bar_chart(df.nlargest(5, 'Months').set_index('Title')['Months'])

    with tab2:
        st.dataframe(df, use_container_width=True)
else:
    st.info("Please upload the 'anime.csv' file in the sidebar to begin analysis.")