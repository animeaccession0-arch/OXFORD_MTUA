import streamlit as st
import google.generativeai as genai
import time
import json
from datetime import datetime

st.set_page_config(page_title="MTUA AI Exam Hall | Auto-Repair", page_icon="📜", layout="wide")

# AUTO REPAIR FUNCTION
def get_working_model():
    """Khud check karega kaunsa model chal raha hai"""
    models_to_try = [
        'gemini-1.5-flash-latest',  # 1st Priority - No Card
        'gemini-1.5-flash',         # 2nd Priority
        'gemini-1.5-pro-latest'     # 3rd Priority
    ]
    
    for model_name in models_to_try:
        try:
            test_model = genai.GenerativeModel(model_name)
            test_model.generate_content("Test")
            st.sidebar.success(f"✅ Active Model: {model_name}")
            return test_model
        except Exception as e:
            st.sidebar.warning(f"❌ {model_name} failed. Trying next...")
            continue
    
    st.error("🚨 All models failed. Check API Key")
    return None

# API SETUP
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = get_working_model() # YE KHUD REPAIR KAREGA

if model is None:
    st.stop()

# CSS
st.markdown("""
<style>
.main-header { font-size:42px; font-weight:800; color:#0A2540; text-align:center; }
.card { background:#F8FAFC; padding:25px; border-radius:16px; border:1px solid #DBEAFE; }
.stButton>button { background:linear-gradient(90deg, #0A2540 0%, #1E3A8A 100%); color:white; border-radius:10px; height:3.2em; width:100%; font-weight:700; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">📜 MTUA AI EXAM HALL</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:green;">🛡️ Auto-Repair System Active</p>', unsafe_allow_html=True)
st.markdown("---")

# SIDEBAR
with st.sidebar:
    st.title("🎯 System Status")
    st.info("If any model fails, system auto-switches to backup model")

# MAIN
student_name = st.text_input("Full Name *", placeholder="For Certificate")
subject = st.selectbox("Subject", ["General Knowledge", "Mathematics", "Science", "English"])
level = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
num_questions = st.slider("Number of Questions", 10, 100, 30)

# SAFE GENERATE FUNCTION
def safe_generate(prompt):
    """Error aaye to 3 baar retry karega"""
    for attempt in range(3):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                st.warning(f"Rate limit. Retrying in 3 sec... Attempt {attempt+1}/3")
                time.sleep(3)
            else:
                st.error(f"Error: {e}")
                return None
    return None

if st.button("🚀 Generate Exam Paper"):
    if student_name == "":
        st.error("⚠️ Please enter your name")
    elif model:
        with st.spinner("AI is generating questions..."):
            prompt = f"Generate {num_questions} {level} MCQ for {subject}. Return JSON: [{{'q':'','options':['A','B','C','D'],'answer':'A','explanation':''}}]"
            
            result = safe_generate(prompt) # YE SAFE HAI
            
            if result:
                try:
                    clean_text = result.replace("```json", "").replace("```", "")
                    questions = json.loads(clean_text)
                    st.success(f"✅ {len(questions)} Questions Generated!")
                    
                    with st.container():
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        for i, q in enumerate(questions):
                            st.markdown(f"**Q{i+1}. {q['q']}**")
                            st.radio("Choose:", q['options'], key=f"{i}_{time.time()}")
                        st.markdown('</div>', unsafe_allow_html=True)
                except:
                    st.error("JSON parse error. AI gave bad format. Click again.")

st.markdown("---")
st.caption("© 2026 MTUA AI | Auto-Repair v2.0 | If error comes, refresh once")
