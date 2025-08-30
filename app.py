import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("steamspy_data.csv")

st.set_page_config(page_title="Steam Games Dashboard", layout="wide")

# Title
st.title("🎮 Steam Games Dashboard")

# ----------------------------------------------------
# Sidebar Filters
st.sidebar.header("Filter Options")
developer = st.sidebar.selectbox("Select Developer:", ["All"] + sorted(df["developer"].dropna().unique().tolist()))
genre = st.sidebar.selectbox("Select Genre:", ["All"] + sorted(df["genre"].dropna().unique().tolist()))

filtered_df = df.copy()
if developer != "All":
    filtered_df = filtered_df[filtered_df["developer"] == developer]
if genre != "All":
    filtered_df = filtered_df[filtered_df["genre"] == genre]

st.write(f"📊 Number of games after filtering: **{len(filtered_df)}**")

# ----------------------------------------------------
# 1. Top 10 Games by Owners
st.subheader("🔥 Top 10 Games by Owners")
top_games = filtered_df.sort_values("owners", ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(x="owners", y="name", data=top_games, ax=ax, palette="viridis")
ax.set_xlabel("Number of Owners")
ax.set_ylabel("Game Title")
st.pyplot(fig)

# ----------------------------------------------------
# 2. Positive vs Negative Reviews
st.subheader("⭐ Positive vs Negative Reviews")
if "positive" in filtered_df.columns and "negative" in filtered_df.columns:
    fig2, ax2 = plt.subplots(figsize=(6,6))
    ax2.pie(
        [filtered_df["positive"].sum(), filtered_df["negative"].sum()],
        labels=["Positive", "Negative"],
        autopct="%1.1f%%",
        startangle=90,
        colors=["#2ecc71", "#e74c3c"]
    )
    ax2.set_title("Review Sentiment Distribution")
    st.pyplot(fig2)
else:
    st.info("No review data available in this dataset.")

# ----------------------------------------------------
# 3. General Statistics
st.subheader("📈 General Statistics")
st.write(filtered_df[["owners", "price", "positive", "negative"]].describe())
