import streamlit as st
import pandas as pd

st.set_page_config(page_title="News Aggregator", layout="wide")
st.title("🗞️ Latest News Headlines")

df = pd.read_csv("news_headlines.csv")

sources = st.multiselect("Filter by source", df["source"].unique(), default=df["source"].unique())
search = st.text_input("Search in titles")

filtered = df[df["source"].isin(sources)]
if search:
    filtered = filtered[filtered["title"].str.contains(search, case=False)]

for _, row in filtered.iterrows():
    st.markdown(f"### [{row['title']}]({row['link']})")
    st.write(f"*{row['source']} – {row['published']}*")
    if pd.notna(row["summary"]) and row["summary"].strip():
        st.markdown(f"> {row['summary']}")
    else:
        st.markdown("_No summary available._")
    st.markdown("---")
