
import streamlit as st
from fabric_component import st_fabric_board
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Interactive AWW Board", layout="wide")
st.title("🎨 Interactive AWW Board (Fabric.js)")

# --------------------------
# User Info & Room
# --------------------------
st.sidebar.header("User / Room Setup")
username = st.sidebar.text_input("Enter your name", value="Guest")
room = st.sidebar.text_input("Room ID", value="Room1")

# --------------------------
# Fabric.js Canvas
# --------------------------
st.subheader("🖌 Canvas (Double-click to add editable text)")
st_fabric_board(width=1000, height=600)

# --------------------------
# Chat (Local Session)
# --------------------------
st.sidebar.header("Live Chat")
chat_input = st.sidebar.text_input("Type your message")
if st.sidebar.button("Send"):
    if "chat_log" not in st.session_state:
        st.session_state.chat_log = []
    st.session_state.chat_log.append({
        "user": username,
        "message": chat_input,
        "timestamp": str(datetime.now())
    })

st.subheader("💬 Chat")
for c in st.session_state.get("chat_log", [])[-20:]:
    st.markdown(f"**{c['user']}** ({c['timestamp'].split(' ')[1]}): {c['message']}")

# --------------------------
# Quiz / Poll
# --------------------------
st.sidebar.header("Quiz / Poll")
quiz_file = st.sidebar.file_uploader("Upload CSV Quiz", type=["csv"])
if quiz_file:
    quiz_df = pd.read_csv(quiz_file)
else:
    quiz_df = pd.read_csv("sample_quiz.csv")

st.header("📊 Live Quiz")
question_index = st.number_input("Select Question", 1, len(quiz_df), 1) - 1
q = quiz_df.iloc[question_index]
st.subheader(q["Question"])
options = [q["Option1"], q["Option2"], q["Option3"], q["Option4"]]
selected = st.radio("Choose an answer:", options)

if st.button("Submit Answer"):
    if "quiz_stats" not in st.session_state:
        st.session_state.quiz_stats = {opt:0 for opt in options}
    st.session_state.quiz_stats[selected] += 1

# Live Quiz Stats
quiz_stats = st.session_state.get("quiz_stats", {opt:0 for opt in options})
fig = px.bar(
    x=list(quiz_stats.keys()),
    y=list(quiz_stats.values()),
    labels={"x":"Options","y":"Votes"},
    text=list(quiz_stats.values()),
    color=list(quiz_stats.keys())
)
st.plotly_chart(fig, use_container_width=True)
