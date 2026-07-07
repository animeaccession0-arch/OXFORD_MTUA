import streamlit as st
import google.generativeai as genai
import time
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
st.set_page_config(page_title="MTUA AI Exam Hall by Anime", page_icon="📜", layout="wide")
st.markdown("<h1 style='text-align: center; color: #003366;'>📜 MTUA AI EXAM HALL</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: grey;'>Built by Anime | AI Questions + Past Papers + Certificate</h3>", unsafe_allow_html=True)
st.markdown("---")

student_name = st.text_input("Enter Your Full Name for Certificate:")
col1, col2 = st.columns(2)
with col1:
    exam_mode = st.selectbox("Exam Mode:", ["AI Generate New Paper", "Real Past Paper 2023"])
with col2:
    level = st.selectbox("Difficulty:", ["Easy", "Medium", "Hard"])
    num_questions = st.selectbox("Number of Questions:", [5, 10])

if st.button("🚀 Start Exam", use_container_width=True):
    if not student_name:
        st.warning("Please enter your name first")
        st.stop()
    st.success(f"Exam Started for {student_name} - {num_questions} Qs")

st.markdown("---")
st.caption("Built by Anime for Oxford MTUA")
