import streamlit as st
import requests
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="UPSC AI Quest Hub",
    page_icon="⚡",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button {
        background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%);
        color: white;
        border-radius: 12px;
        padding: 0.6rem 1.2rem;
        font-weight: bold;
        border: none;
        transition: transform 0.2s;
    }
    .stButton>button:hover { transform: scale(1.02); }
    .pro-card {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

API_BASE = "http://127.0.0.1:8000/api/v1"

st.title("⚡ UPSC AI Quest Hub")
st.caption("Master GS & CSAT with Interactive AI Practice & Mastery Analytics")

# Sidebar Navigation
st.sidebar.title("🎮 Navigation")
module = st.sidebar.radio(
    "Select Module:",
    [
        "✍️ Mains Evaluator", 
        "🧮 CSAT Interactive Arena", 
        "📊 Score Analytics & Trends", 
        "🎯 Prelims Quiz Engine", 
        "📚 Syllabus Mastery Tracker"
    ]
)

st.sidebar.markdown("---")
st.sidebar.metric(label="🔥 Prep Streak", value="6 Days")
st.sidebar.metric(label="🏆 Target Mains Score", value="100+ / paper")

# ---------------- MONETIZATION SIDEBAR WIDGET ----------------
st.sidebar.markdown("---")
st.sidebar.subheader("👑 Upgrade to Pro")
st.sidebar.caption("Get Unlimited OCR Mains Evaluations & Model Answers")

if st.sidebar.button("Upgrade for ₹499/mo 🚀"):
    with st.spinner("Connecting to Secure Checkout..."):
        try:
            res = requests.post(f"{API_BASE}/payment/create-order", data={"plan_type": "pro_monthly"}).json()
            st.sidebar.success(f"Order Created! ID: {res['order_id']}")
            st.sidebar.info("Proceeding to Razorpay Gateway...")
        except Exception as e:
            st.sidebar.error("Payment Service temporarily offline.")

# ---------------- MODULE 1: MAINS EVALUATOR ----------------
if module == "✍️ Mains Evaluator":
    st.header("✍️ Mains Answer Evaluator")
    st.write("Submit text or upload a photo/PDF of your handwritten answer sheet for evaluation.")
    
    q_text = st.text_input("Question:", "Discuss the constitutional safeguards available to civil servants under Article 311.")
    tab1, tab2 = st.tabs(["📝 Text Submission", "📷 Upload Image / PDF"])
    
    with tab1:
        ans_text = st.text_area("Your Response:", height=150)
        if st.button("Evaluate Text Answer 🚀"):
            if ans_text:
                with st.spinner("AI Evaluator analyzing response..."):
                    res = requests.post(f"{API_BASE}/mains/evaluate", data={"question": q_text, "student_answer": ans_text}).json()
                    st.success("Evaluation Completed!")
                    st.markdown(res["content"])
            else:
                st.warning("Please enter your answer text.")
                
    with tab2:
        uploaded_file = st.file_uploader("Upload handwritten sheet (JPG, PNG, PDF)", type=["jpg", "jpeg", "png", "pdf"])
        if st.button("OCR & Evaluate Upload 📸"):
            if uploaded_file:
                with st.spinner("Processing file & running AI evaluation..."):
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    res = requests.post(f"{API_BASE}/mains/evaluate-file", data={"question": q_text}, files=files).json()
                    st.success("Evaluation Completed!")
                    if "extracted_text" in res:
                        with st.expander("🔍 View OCR Extracted Text"):
                            st.write(res["extracted_text"])
                    st.markdown(res["content"])
            else:
                st.warning("Please attach a file first.")

# ---------------- MODULE 2: INTERACTIVE CSAT ARENA ----------------
elif module == "🧮 CSAT Interactive Arena":
    st.header("🧮 CSAT Interactive Practice & Solver")
    
    st.subheader("⚡ Speed Challenge Question")
    st.info("A train 150m long is running at 54 km/h. How many seconds will it take to cross a platform 250m long?")
    
    user_choice = st.radio("Select your answer:", ["(A) 20 seconds", "(B) 26.67 seconds", "(C) 30 seconds", "(D) 35 seconds"])
    
    if st.button("Check Answer ✅"):
        if "(B)" in user_choice:
            st.balloons()
            st.success("🎉 Correct! Total Distance = 150 + 250 = 400m. Speed = 54 × (5/18) = 15 m/s. Time = 400 / 15 = 26.67s.")
        else:
            st.error("❌ Incorrect. Try using the Speed-Time conversion shortcut!")

    st.markdown("---")
    st.subheader("💡 Solve Any Custom CSAT Question")
    csat_q = st.text_area("Paste CSAT Question for AI Shortcut Solution:", "A and B can finish a task in 12 and 15 days respectively. How long if working together?")
    if st.button("Generate AI Shortcut Solution ⚡"):
        with st.spinner("Calculating shortcut..."):
            res = requests.post(f"{API_BASE}/csat/solve", data={"question": csat_q}).json()
            st.info(res["content"])

# ---------------- MODULE 3: SCORE ANALYTICS & TRENDS ----------------
elif module == "📊 Score Analytics & Trends":
    st.header("📊 Mains Score Progress & Analytics")
    st.write("Track your performance growth over time.")
    
    try:
        data = requests.get(f"{API_BASE}/analytics/scores").json()["history"]
        df = pd.DataFrame(data)
        if not df.empty and "score" in df.columns:
            st.line_chart(df, y="score")
            col1, col2, col3 = st.columns(3)
            col1.metric("Average Score", f"{df['score'].mean():.2f} / 10")
            col2.metric("Highest Score", f"{df['score'].max():.2f} / 10")
            col3.metric("Total Answers Evaluated", len(df))
        else:
            st.info("No score data recorded yet. Complete some Mains evaluations!")
    except Exception as e:
        st.error(f"Could not load analytics: {e}")

# ---------------- MODULE 4: PRELIMS QUIZ ENGINE ----------------
elif module == "🎯 Prelims Quiz Engine":
    st.header("🎯 Rapid-Fire Prelims MCQ Generator")
    topic = st.text_input("Enter Topic for MCQ:", "Preamble & Fundamental Rights")
    
    if st.button("Generate MCQ Flashcard 🎲"):
        with st.spinner("Setting question..."):
            res = requests.post(f"{API_BASE}/quiz/generate", data={"topic": topic}).json()
            st.markdown(res["content"])

# ---------------- MODULE 5: SYLLABUS MASTERY TRACKER ----------------
elif module == "📚 Syllabus Mastery Tracker":
    st.header("📚 GS Micro-Topic Mastery Tracker")
    st.write("Check off completed micro-topics to update your overall syllabus progress.")
    
    topics = {
        "GS 1 - History & Art": ["Indus Valley Civilization", "Bhakti Movement", "1857 Revolt", "Freedom Struggle 1919-1947"],
        "GS 2 - Polity & Governance": ["Preamble & Article 21", "Federal Structure & Article 356", "Judicial Review", "Election Commission"],
        "GS 3 - Economy & Environment": ["Monetary Policy & RBI", "GST & Fiscal Federalism", "Climate Change COP Declarations", "Renewable Energy Targets"]
    }
    
    completed_count = 0
    total_count = 0
    
    for subject, topic_list in topics.items():
        st.subheader(subject)
        for t in topic_list:
            total_count += 1
            if st.checkbox(t, key=f"cb_{t}"):
                completed_count += 1
                
    progress_pct = int((completed_count / total_count) * 100) if total_count > 0 else 0
    st.markdown("---")
    st.subheader(f"🏆 Total Syllabus Completion: {progress_pct}%")
    st.progress(progress_pct / 100)