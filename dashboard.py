import streamlit as st
import pandas as pd
from run import scrape_news

st.set_page_config(page_title="News Aggregator", layout="wide")
st.title("Latest News Headlines with Summaries")

if st.button("Fetch Latest News"):
    with st.spinner("Scraping news and generating summaries..."):
        df = scrape_news()
        st.success("Done! News updated.")
else:
    try:
        df = pd.read_csv("news_headlines.csv")
    except FileNotFoundError:
        st.warning("No news file found. Please fetch the latest news.")
        df = pd.DataFrame()

if not df.empty:
    for _, row in df.iterrows():
        st.subheader(f"{row['title']} ({row['source']})")
        st.write(f"*Published:* {row['published']}")
        st.write(row['summary'])
        st.markdown(f"[Read more]({row['link']})", unsafe_allow_html=True)
        st.markdown("---")
