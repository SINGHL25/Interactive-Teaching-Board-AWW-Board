
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import pandas as pd
import plotly.express as px
from datetime import datetime
from PIL import Image

st.set_page_config(page_title="Flexible AWW Board", layout="wide")
st.title("🌟 Flexible Classroom Board (Local Simulation)")

# --------------------------
# Multi-Room & User Setup
# --------------------------
st.sidebar.header("User / Room Setup")
username = st.sidebar.text_input("Enter your name", value="Guest")
room = st.sidebar.text_input("Room ID", value="Room1")

if "rooms" not in st.session_state:
    st.session_state.rooms = {}

if room not in st.session_state.rooms:
    st.session_state.rooms[room] = {
        "canvas": None,
        "chat": [],
        "quiz_stats": {}
    }

room_state = st.session_state.rooms[room]

# --------------------------
# Canvas Settings
# --------------------------
st.sidebar.header("Canvas Settings")
stroke_color = st.sidebar.color_picker("Stroke Color", "#000000")
stroke_width = st.sidebar.slider("Stroke Width", 1, 20, 3)
drawing_mode = st.sidebar.selectbox("Drawing Mode", ["freedraw", "line", "rect", "circle", "text"])
canvas_height = st.sidebar.slider("Canvas Height", 300, 800, 500)
canvas_width = st.sidebar.slider("Canvas Width", 500, 1200, 800)

# --------------------------
# Canvas Section
# --------------------------
canvas_obj = st_canvas(
    stroke_color=stroke_color,
    stroke_width=stroke_width,
    background_color="#ffffff",
    height=canvas_height,
    width=canvas_width,
    drawing_mode=drawing_mode,
    key=f"canvas_{room}",
    display_toolbar=True,
    initial_drawing=room_state["canvas"]
)

# Update room canvas
if canvas_obj.json_data is not None:
    room_state["canvas"] = canvas_obj.json_data
    room_state["last_updated_by"] = username
    room_state["last_update_time"] = str(datetime.now())

# --------------------------
# Live Chat
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
    quiz_df = pd.read_csv("sample_quiz.csv")

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
    color=list(quiz_stats.keys()),
)
st.plotly_chart(fig, use_container_width=True)

# --------------------------
# Save Canvas Locally
# --------------------------
if canvas_obj.image_data is not None:
    if st.button("Save Canvas Locally"):
        img = Image.fromarray(canvas_obj.image_data.astype("uint8"))
        img.save(f"{room}_canvas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        st.success("Canvas saved locally!")

# --------------------------
# Optional: Editable Shapes/Text (Flexible)
# --------------------------
st.sidebar.header("Add Text / Shape")
add_text = st.sidebar.text_input("Add Text Annotation")
shape_color = st.sidebar.color_picker("Shape Color", "#FF0000")
shape_size = st.sidebar.slider("Shape Size", 20, 200, 50)

if st.sidebar.button("Add Text/Shape"):
    # Add as a special JSON object in canvas state
    if "extra_elements" not in room_state:
        room_state["extra_elements"] = []
    room_state["extra_elements"].append({
        "type": "text_shape",
        "user": username,
        "text": add_text,
        "color": shape_color,
        "size": shape_size,
        "timestamp": str(datetime.now())
    })
    st.success(f"Added '{add_text}' to canvas!")

# Display extra elements
if "extra_elements" in room_state:
    for elem in room_state["extra_elements"]:
        st.markdown(f"**[{elem['user']}]** {elem['text']} (size: {elem['size']}, color: {elem['color']})")
