import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "https://upsc-ai-backend.onrender.com")

st.set_page_config(page_title="UPSC AI Quest Hub", layout="wide")

# Sidebar Navigation
st.sidebar.title("🎮 Navigation")
module = st.sidebar.radio(
    "Select Module:",
    [
        "📚 Subject-Wise PYQ Explorer",
        "✍️ Mains Evaluator",
        "📊 CSAT Interactive Arena",
        "📈 Score Analytics & Trends",
        "🎯 Prelims Quiz Engine",
        "📚 Syllabus Mastery Tracker"
    ]
)

st.sidebar.markdown("---")
st.sidebar.write("🔥 **Prep Streak:** 6 Days")
st.sidebar.write("🏆 **Target Mains Score:** 100+ / paper")

# --- MODULE 1: PYQ EXPLORER ---
if module == "📚 Subject-Wise PYQ Explorer":
    st.title("📚 UPSC Subject-Wise PYQ Bank (2006–2025)")

    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        subject = st.selectbox(
            "Select Subject",
            [
                "Polity & Governance",
                "Economy",
                "Modern History",
                "Ancient & Medieval History",
                "Art & Culture",
                "Geography",
                "Environment & Ecology",
                "Science & Technology",
                "International Relations"
            ]
        )

    with col2:
        years = st.slider("Select Year Range", 2006, 2025, (2006, 2025))

    with col3:
        exam_type = st.radio("Exam", ["Prelims", "Mains"])

    if st.button("Load Questions", type="primary"):
        with st.spinner("Fetching questions..."):
            try:
                url = f"{BACKEND_URL}/api/v1/pyq/fetch"
                params = {
                    "subject": subject,
                    "year_start": years[0],
                    "year_end": years[1],
                    "exam_type": exam_type
                }
                res = requests.get(url, params=params)
                
                if res.status_code == 200:
                    data = res.json().get("data", [])
                    st.success(f"Found {len(data)} questions for {subject} ({years[0]}–{years[1]})")
                    
                    for idx, q in enumerate(data, 1):
                        with st.expander(f"Q{idx} [{q['year']}] - Topic: {q.get('topic', 'General')}"):
                            st.write(q["question"])
                            
                            if exam_type == "Prelims" and q.get("options"):
                                opts = q["options"]
                                for key, val in opts.items():
                                    st.write(f"**({key})** {val}")
                            
                            if st.checkbox("Show Answer & Explanation", key=f"ans_{q['id']}"):
                                st.info(f"**Correct Answer:** {q.get('correct_option', 'N/A')}")
                                st.write(f"**Explanation:** {q.get('explanation', 'No detailed explanation available.')}")
                else:
                    st.error("Failed to retrieve questions from server.")
            except Exception as e:
                st.error(f"Connection error: {e}")

# --- MODULE 2: SYLLABUS TRACKER ---
elif module == "📚 Syllabus Mastery Tracker":
    st.title("Syllabus Mastery Tracker")
    st.subheader("GS 1 - History & Art")
    st.checkbox("Indus Valley Civilization")
    st.checkbox("Bhakti Movement")
    st.checkbox("1857 Revolt")
    st.checkbox("Freedom Struggle 1919-1947")

    st.subheader("GS 2 - Polity & Governance")
    st.checkbox("Preamble & Article 21")
    st.checkbox("Federal Structure & Article 356")
    st.checkbox("Judicial Review")
    st.checkbox("Election Commission")

    st.subheader("GS 3 - Economy & Environment")
    st.checkbox("Monetary Policy & RBI")
    st.checkbox("GST & Fiscal Federalism")
    st.checkbox("Climate Change COP Declarations")
    st.checkbox("Renewable Energy Targets")

# --- OTHER MODULES ---
else:
    st.title(module)
    st.info("Module loading...")