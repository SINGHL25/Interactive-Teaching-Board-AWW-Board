
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import streamlit.components.v1 as components

st.set_page_config(page_title="Interactive AWW Board", layout="wide")
st.title("🎨 Interactive Classroom Board")

# --------------------------
# User & Room Setup
# --------------------------
st.sidebar.header("User / Room Setup")
username = st.sidebar.text_input("Enter your name", value="Guest")
room = st.sidebar.text_input("Room ID", value="Room1")

if "rooms" not in st.session_state:
    st.session_state.rooms = {}

if room not in st.session_state.rooms:
    st.session_state.rooms[room] = {
        "chat": [],
        "quiz_stats": {}
    }

room_state = st.session_state.rooms[room]

# --------------------------
# Fabric.js Canvas
# --------------------------
st.subheader("🖌 Canvas (Double-click to add editable text)")

canvas_html = f"""
<canvas id="canvas" width="1000" height="600" style="border:1px solid #000000;"></canvas>
<script src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.2.4/fabric.min.js"></script>
<script>
    var canvas = new fabric.Canvas('canvas', {{ selection: true }});
    canvas.isDrawingMode = true;
    canvas.freeDrawingBrush.width = 5;
    canvas.freeDrawingBrush.color = '#000000';

    // Double-click to add editable text
    canvas.on('mouse:dblclick', function(options) {{
        var text = new fabric.IText('Double-click to edit', {{
            left: options.pointer.x,
            top: options.pointer.y,
            fill: '#FF0000',
            fontSize: 24
        }});
        canvas.add(text);
        canvas.setActiveObject(text);
    }});
</script>
"""

components.html(canvas_html, height=620)

# --------------------------
# Live Chat (Session-Based)
# --------------------------
st.sidebar.header("Live Chat")
chat_input = st.sidebar.text_input("Type your message")
if st.sidebar.button("Send"):
    room_state["chat"].append({
        "user": username,
        "message": chat_input,
        "timestamp": str(datetime.now())
    })

st.subheader("💬 Chat")
for c in room_state["chat"][-20:]:
    st.markdown(f"**{c['user']}** ({c['timestamp'].split(' ')[1]}): {c['message']}")

# --------------------------
# Quiz / Poll
# --------------------------
st.sidebar.header("Quiz / Poll")
quiz_file = st.sidebar.file_uploader("Upload CSV Quiz", type=["csv"])
if quiz_file:
    quiz_df = pd.read_csv(quiz_file)
else:
    # Sample quiz
    quiz_df = pd.DataFrame({
        "Question": ["What is 2+2?", "Capital of France?"],
        "Option1": ["3","Paris"],
        "Option2": ["4","London"],
        "Option3": ["5","Berlin"],
        "Option4": ["6","Madrid"],
        "Answer": ["4","Paris"]
    })

st.header("📊 Live Quiz")
question_index = st.number_input("Select Question", 1, len(quiz_df), 1) - 1
q = quiz_df.iloc[question_index]
st.subheader(q["Question"])
options = [q["Option1"], q["Option2"], q["Option3"], q["Option4"]]
selected = st.radio("Choose an answer:", options)

if st.button("Submit Answer"):
    if selected not in room_state["quiz_stats"]:
        room_state["quiz_stats"][selected] = 0
    room_state["quiz_stats"][selected] += 1

# Display Quiz Stats
quiz_stats = room_state["quiz_stats"] or {opt:0 for opt in options}
fig = px.bar(
    x=list(quiz_stats.keys()),
    y=list(quiz_stats.values()),
    labels={"x":"Options","y":"Votes"},
    text=list(quiz_stats.values()),
    color=list(quiz_stats.keys())
)
st.plotly_chart(fig, use_container_width=True)

