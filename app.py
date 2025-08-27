
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Remote Teaching Board", layout="wide")
st.title("🎨 Interactive Remote Teaching Board")

# -------------------
# Sidebar Controls
# -------------------
st.sidebar.header("Canvas Settings")
stroke_color = st.sidebar.color_picker("Stroke Color", "#000000")
stroke_width = st.sidebar.slider("Stroke Width", 1, 20, 3)
drawing_mode = st.sidebar.selectbox("Drawing Mode", ["freedraw", "line", "rect", "circle"])
canvas_height = st.sidebar.slider("Canvas Height", 300, 800, 500)
canvas_width = st.sidebar.slider("Canvas Width", 500, 1200, 800)
show_canvas_buttons = st.sidebar.checkbox("Show Canvas Buttons", True)

# -------------------
# Canvas
# -------------------
canvas_result = st_canvas(
    stroke_color=stroke_color,
    stroke_width=stroke_width,
    background_color="#ffffff",
    update_streamlit=True,
    height=canvas_height,
    width=canvas_width,
    drawing_mode=drawing_mode,
    key="canvas",
    display_toolbar=show_canvas_buttons,
)

# -------------------
# Quiz Section
# -------------------
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
    if selected == q["Answer"]:
        st.success("✅ Correct!")
    else:
        st.error(f"❌ Incorrect! Correct answer: {q['Answer']}")

# -------------------
# Quiz Statistics
# -------------------
st.subheader("Quiz Stats")
if "quiz_stats" not in st.session_state:
    st.session_state.quiz_stats = {opt:0 for opt in options}

if selected:
    st.session_state.quiz_stats[selected] += 1

fig = px.bar(
    x=list(st.session_state.quiz_stats.keys()),
    y=list(st.session_state.quiz_stats.values()),
    labels={"x":"Options","y":"Votes"},
    text=list(st.session_state.quiz_stats.values())
)
st.plotly_chart(fig, use_container_width=True)

# -------------------
# Save Canvas
# -------------------
if canvas_result.image_data is not None:
    if st.button("Save Canvas"):
        canvas_result.image_data.astype("uint8")
        from PIL import Image
        img = Image.fromarray(canvas_result.image_data.astype("uint8"))
        img.save("canvas_image.png")
        st.success("Canvas saved as canvas_image.png")
