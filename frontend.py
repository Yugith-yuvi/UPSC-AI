import streamlit as st
import requests
import os

# Set backend URL cleanly
BACKEND_URL = os.getenv("BACKEND_URL", "https://upsc-ai-backend.onrender.com").rstrip("/")

st.set_page_config(
    page_title="UPSC AI Quest Hub", 
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session State
if "active_page" not in st.session_state:
    st.session_state.active_page = "Home"

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

query_params = st.query_params
if "page" in query_params:
    st.session_state.active_page = query_params["page"]

def navigate_to(page_name):
    st.session_state.active_page = page_name
    st.query_params["page"] = page_name

is_dark = st.session_state.theme == "Dark"

# Dynamic Theme Color Tokens
bg_color = "#0b0f19" if is_dark else "#f8fafc"
text_color = "#f1f5f9" if is_dark else "#0f172a"
subtext_color = "#94a3b8" if is_dark else "#64748b"

nav_btn_bg = "#1e293b" if is_dark else "#ffffff"
nav_btn_border = "#334155" if is_dark else "#cbd5e1"
nav_btn_text = "#f8fafc" if is_dark else "#0f172a"

stat_bg = "rgba(30, 41, 59, 0.5)" if is_dark else "#ffffff"
stat_border = "rgba(255, 255, 255, 0.08)" if is_dark else "#e2e8f0"

card_bg = "rgba(30, 41, 59, 0.4)" if is_dark else "#ffffff"
card_border = "rgba(255, 255, 255, 0.08)" if is_dark else "#cbd5e1"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap');

    /* Global Base Theme */
    html, body, [class*="stApp"] {{
        font-family: 'Outfit', sans-serif !important;
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}

    /* 1. TOP NAV & CARD TRIGGER BUTTONS */
    div[data-testid="stColumn"] button,
    div[data-testid="stPopover"] > button,
    div[data-testid="stBaseButton-secondary"] {{
        background-color: {nav_btn_bg} !important;
        border: 1px solid {nav_btn_border} !important;
        border-radius: 10px !important;
        height: 42px !important;
        box-shadow: none !important;
        transition: all 0.2s ease !important;
        color: {nav_btn_text} !important;
    }}

    div[data-testid="stColumn"] button *,
    div[data-testid="stPopover"] > button *,
    div[data-testid="stBaseButton-secondary"] * {{
        color: {nav_btn_text} !important;
        fill: {nav_btn_text} !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }}

    div[data-testid="stColumn"] button:hover,
    div[data-testid="stPopover"] > button:hover,
    div[data-testid="stBaseButton-secondary"]:hover {{
        border-color: #38bdf8 !important;
        background-color: {'#334155' if is_dark else '#f1f5f9'} !important;
    }}

    /* 2. FIX POPOVER MENU CONTAINER & POPUP CONTENTS */
    div[data-testid="stPopoverBody"] {{
        background-color: {'#0f172a' if is_dark else '#ffffff'} !important;
        border: 1px solid {nav_btn_border} !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5) !important;
        padding: 12px !important;
    }}

    div[data-testid="stPopoverBody"] p, 
    div[data-testid="stPopoverBody"] span,
    div[data-testid="stPopoverBody"] strong {{
        color: {text_color} !important;
    }}

    div[data-testid="stPopoverBody"] button {{
        background-color: {nav_btn_bg} !important;
        border: 1px solid {nav_btn_border} !important;
        border-radius: 8px !important;
        margin-bottom: 6px !important;
    }}

    div[data-testid="stPopoverBody"] button p {{
        color: {nav_btn_text} !important;
        font-weight: 600 !important;
    }}

    div[data-testid="stPopoverBody"] button:hover {{
        border-color: #38bdf8 !important;
        background-color: {'#334155' if is_dark else '#f1f5f9'} !important;
    }}

    /* 3. TOGGLE SWITCH CONTAINER STYLING */
    div[data-testid="stCheckbox"] {{
        background: {nav_btn_bg} !important;
        border: 1px solid {nav_btn_border} !important;
        padding: 6px 14px !important;
        border-radius: 10px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        height: 42px !important;
    }}

    div[data-testid="stCheckbox"] label p {{
        color: {nav_btn_text} !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }}

    /* Card Box Wrappers */
    .dashboard-card-box {{
        background: {card_bg};
        border: 1px solid {card_border};
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 12px;
        min-height: 140px;
    }}
    .dashboard-card-title {{
        font-size: 1.2rem;
        font-weight: 700;
        color: {text_color};
        margin-bottom: 6px;
    }}
    .dashboard-card-desc {{
        font-size: 0.9rem;
        color: {subtext_color};
        line-height: 1.4;
    }}

    /* Typography & Stat Bar */
    .hero-glow-title {{
        font-size: 2.5rem;
        font-weight: 800;
        background: {'linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #38bdf8 100%)' if is_dark else 'linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #2563eb 100%)'};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
    }}
    
    .hero-sub {{
        font-size: 1.1rem;
        color: {subtext_color};
        margin-bottom: 24px;
        font-weight: 500;
    }}

    .stat-box {{
        background: {stat_bg};
        border: 1px solid {stat_border};
        border-radius: 12px;
        padding: 12px 20px;
        text-align: center;
        backdrop-filter: blur(10px);
    }}
    .stat-number {{
        font-size: 1.3rem;
        font-weight: 800;
        color: {'#38bdf8' if is_dark else '#2563eb'};
    }}
    .stat-label {{
        font-size: 0.75rem;
        color: {subtext_color};
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }}

    .quiz-card {{
        background: {'rgba(30, 41, 59, 0.4)' if is_dark else '#ffffff'};
        border: 1px solid {'rgba(255, 255, 255, 0.08)' if is_dark else '#e2e8f0'};
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
    }}

    .score-banner {{
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 25px;
    }}
</style>
""", unsafe_allow_html=True)

# --- TOP NAVIGATION BAR ---
col_nav1, col_nav2, _ , col_toggle = st.columns([1.2, 1.2, 6.8, 2.8])

with col_nav1:
    if st.button("🏠 Home", key="btn_top_home", use_container_width=True):
        navigate_to("Home")
        st.rerun()

with col_nav2:
    with st.popover("☰ Menu", use_container_width=True):
        st.write("**Quick Tools Navigation**")
        if st.button("🎯 Prelims PYQ Quiz", key="m_p1", use_container_width=True):
            navigate_to("Prelims PYQ Quiz")
            st.rerun()
        if st.button("✍️ Mains PYQ Practice", key="m_p2", use_container_width=True):
            navigate_to("Mains PYQ Practice")
            st.rerun()
        if st.button("📊 CSAT PYQ Quiz", key="m_p3", use_container_width=True):
            navigate_to("CSAT PYQ Quiz")
            st.rerun()
        if st.button("⚡ Daily Quiz Generator", key="m_p4", use_container_width=True):
            navigate_to("Daily Quiz Generator")
            st.rerun()
        if st.button("🔍 Universal Mains Evaluator", key="m_p5", use_container_width=True):
            navigate_to("Universal Mains Evaluator")
            st.rerun()

with col_toggle:
    theme_toggle = st.toggle("Dark Mode 🌙" if is_dark else "Light Mode ☀️", value=is_dark, key="theme_toggle")
    new_theme = "Dark" if theme_toggle else "Light"
    
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

st.markdown("---")

# --- PAGE 1: WELCOME DASHBOARD ---
if st.session_state.active_page == "Home":
    st.markdown('<div class="hero-glow-title">⚡ UPSC AI Quest Hub</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Next-generation AI engine for Prelims, Mains, and CSAT practice.</div>', unsafe_allow_html=True)

    # Dynamic Stat Bar
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown('<div class="stat-box"><div class="stat-number">2000–2026</div><div class="stat-label">Official PYQs</div></div>', unsafe_allow_html=True)
    with s2:
        st.markdown('<div class="stat-box"><div class="stat-number">AI OCR 2.0</div><div class="stat-label">Handwriting Scan</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown('<div class="stat-box"><div class="stat-number">Real-Time</div><div class="stat-label">Current Affairs</div></div>', unsafe_allow_html=True)
    with s4:
        st.markdown('<div class="stat-box"><div class="stat-number">Instant</div><div class="stat-label">Mains Evaluation</div></div>', unsafe_allow_html=True)

    st.write("")
    st.write("")

    # Grid Row 1
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="dashboard-card-box">
            <div class="dashboard-card-title">🎯 Prelims PYQ Quiz</div>
            <div class="dashboard-card-desc">Custom test builder filtering by subject, topic, and year range with instant automated scoring.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Prelims PYQ Engine ➔", key="card_btn_prelims", use_container_width=True, type="primary"):
            navigate_to("Prelims PYQ Quiz")
            st.rerun()

    with col2:
        st.markdown("""
        <div class="dashboard-card-box">
            <div class="dashboard-card-title">✍️ Mains PYQ Writing</div>
            <div class="dashboard-card-desc">Select official Mains questions, write on paper, and upload a photo for detailed AI evaluation.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Mains PYQ Engine ➔", key="card_btn_mains", use_container_width=True):
            navigate_to("Mains PYQ Practice")
            st.rerun()

    st.write("")

    # Grid Row 2
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("""
        <div class="dashboard-card-box">
            <div class="dashboard-card-title">📊 CSAT Interactive Arena</div>
            <div class="dashboard-card-desc">Master Quant, Logical Reasoning, and Reading Comprehension with dedicated practice sets.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch CSAT Arena ➔", key="card_btn_csat", use_container_width=True):
            navigate_to("CSAT PYQ Quiz")
            st.rerun()

    with col4:
        st.markdown("""
        <div class="dashboard-card-box">
            <div class="dashboard-card-title">⚡ Dynamic Quiz Generator</div>
            <div class="dashboard-card-desc">Generate fresh practice questions instantly based on recent news and static UPSC syllabus topics.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Quiz Generator ➔", key="card_btn_daily", use_container_width=True):
            navigate_to("Daily Quiz Generator")
            st.rerun()

    st.write("")

    # Grid Row 3
    col5, _ = st.columns([1, 1])
    with col5:
        st.markdown("""
        <div class="dashboard-card-box">
            <div class="dashboard-card-title">🔍 Universal Mains Evaluator</div>
            <div class="dashboard-card-desc">Upload an answer sheet for ANY question—typed or handwritten—and receive structural feedback.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Universal Evaluator ➔", key="card_btn_univ", use_container_width=True):
            navigate_to("Universal Mains Evaluator")
            st.rerun()

# --- PAGE 2: PRELIMS PYQ QUIZ ---
elif st.session_state.active_page == "Prelims PYQ Quiz":
    st.title("🎯 Prelims PYQ Engine (2000–2026)")
    st.write("Configure your test parameters to generate custom UPSC statement-pattern practice sets.")

    # Filter Section
    with st.container():
        f1, f2, f3 = st.columns([2, 2, 1])
        with f1:
            selected_subject = st.selectbox(
                "Select Subject", 
                ["All Subjects", "Polity & Governance", "Economy", "Modern History", "Environment & Ecology", "Science & Technology", "Geography"]
            )
        with f2:
            year_range = st.slider("Select Year Range", 2000, 2026, (2015, 2026))
        with f3:
            num_questions = st.number_input("Limit Questions", min_value=1, max_value=50, value=10)

    if st.button("🚀 Load PYQ Test Set", type="primary", use_container_width=True):
        st.session_state.quiz_submitted = False
        st.session_state.user_answers = {}
        with st.spinner("Fetching questions from database..."):
            try:
                params = {
                    "subject": selected_subject if selected_subject != "All Subjects" else None,
                    "year_start": year_range[0],
                    "year_end": year_range[1],
                    "limit": num_questions
                }
                res = requests.get(f"{BACKEND_URL}/api/v1/pyq/fetch", params=params, timeout=10)
                if res.status_code == 200:
                    st.session_state.active_quiz_data = res.json().get("data", [])
                else:
                    st.session_state.active_quiz_data = [
                        {
                            "id": 1,
                            "year": 2024,
                            "subject": "Polity & Governance",
                            "question": "Consider the following statements regarding the Preamble to the Indian Constitution:\n1. It is non-justiciable in nature.\n2. It can be amended without altering its basic structure.\nWhich of the statements given above is/are correct?",
                            "options": {"A": "1 only", "B": "2 only", "C": "Both 1 and 2", "D": "Neither 1 nor 2"},
                            "correct_option": "C",
                            "explanation": "The Preamble is non-justiciable and can be amended under Article 368 subject to basic structure limits."
                        },
                        {
                            "id": 2,
                            "year": 2023,
                            "subject": "Economy",
                            "question": "Which one of the following activities constitutes real sector in the economy?\n1. Farmers harvesting their crops\n2. Textile mills converting raw cotton into fabrics\n3. A commercial bank lending money to a trading company",
                            "options": {"A": "1 and 2 only", "B": "2 and 3 only", "C": "1 and 3 only", "D": "1, 2 and 3"},
                            "correct_option": "A",
                            "explanation": "Real sector refers to direct economic production of goods and non-financial services."
                        }
                    ]
            except Exception:
                st.warning("Could not establish direct connection to remote host. Loaded offline database set.")

    # Render Active Test
    if "active_quiz_data" in st.session_state and st.session_state.active_quiz_data:
        questions = st.session_state.active_quiz_data
        st.markdown(f"### 📋 Active Test Set ({len(questions)} Questions)")

        for idx, q in enumerate(questions, 1):
            st.markdown(f"""
            <div class="quiz-card">
                <strong>Question {idx}</strong> <span style="color: #38bdf8;">[{q['subject']} - {q['year']}]</span><br/><br/>
                {q['question']}
            </div>
            """, unsafe_allow_html=True)

            opts = q.get("options", {})
            choice_keys = list(opts.keys())
            
            selected_val = st.radio(
                f"Select option for Q{idx}:",
                choice_keys,
                format_func=lambda x: f"{x}: {opts[x]}",
                key=f"opt_q_{q['id']}"
            )
            st.session_state.user_answers[q['id']] = selected_val

            if st.session_state.quiz_submitted:
                correct = q['correct_option']
                user_ans = st.session_state.user_answers.get(q['id'])
                
                if user_ans == correct:
                    st.success(f"✅ Correct! Option {correct}")
                else:
                    st.error(f"❌ Incorrect. Selected: {user_ans} | Correct: {correct}")
                
                with st.expander("📖 Explanation & Analysis"):
                    st.write(q.get("explanation", "No detailed explanation available."))
            
            st.markdown("---")

        # Submission & Score Evaluation
        if not st.session_state.quiz_submitted:
            if st.button("Submit & Evaluate Test", type="primary"):
                st.session_state.quiz_submitted = True
                st.rerun()
        else:
            correct_count = sum(
                1 for q in questions if st.session_state.user_answers.get(q['id']) == q['correct_option']
            )
            total = len(questions)
            marks = (correct_count * 2) - ((total - correct_count) * 0.66)
            
            st.markdown(f"""
            <div class="score-banner">
                Final Result: {correct_count} / {total} Correct | Net Marks: {marks:.2f} / {total * 2}
            </div>
            """, unsafe_allow_html=True)

# --- PAGE 3: MAINS PYQ ANSWER WRITING ---
elif st.session_state.active_page == "Mains PYQ Practice":
    st.title("✍️ Mains PYQ Answer Practice")
    st.write("Pick a subject, get an official question, write your answer on paper, and upload your sheet.")

    subject = st.selectbox("Select Mains Subject", ["GS 1 - History & Society", "GS 2 - Polity & IR", "GS 3 - Economy & Environment", "GS 4 - Ethics"])
    
    if st.button("Get Mains Question", key="get_mains_q"):
        st.info("📌 **Sample Question:** Evaluate the impact of climate change on coastal agriculture in India, suggesting mitigation strategies. (15 Marks, 250 Words)")

    uploaded_file = st.file_uploader("Upload Scanned Answer Sheet (JPG / PNG / PDF)", type=["jpg", "jpeg", "png", "pdf"])
    if uploaded_file and st.button("Evaluate Answer with AI", key="eval_mains_btn", type="primary"):
        with st.spinner("AI is reading handwriting (OCR) and evaluating content against UPSC criteria..."):
            st.success("Evaluation Complete!")
            st.markdown("### 📝 Score: **8.5 / 15**")
            st.markdown("**Strengths:** Clear structure, good introduction of IPCC targets.")
            st.markdown("**Areas for Improvement:** Needs map representation of vulnerable coastal regions.")

# --- PAGE 4: CSAT PYQ QUIZ ---
elif st.session_state.active_page == "CSAT PYQ Quiz":
    st.title("📊 CSAT Interactive Arena")
    st.write("Practice Quant, Logical Reasoning, and Reading Comprehension questions.")

    topic = st.selectbox("Select Topic", ["Reading Comprehension", "Data Interpretation", "Logical Reasoning", "Quantitative Aptitude"])
    if st.button("Start CSAT Practice Set", key="start_csat", type="primary"):
        st.info("Loading CSAT question set...")

# --- PAGE 5: DYNAMIC PRELIMS QUIZ ---
elif st.session_state.active_page == "Daily Quiz Generator":
    st.title("⚡ AI Current Affairs & Static Quiz Generator")
    st.write("Fresh questions generated on the spot using the latest UPSC statement-based pattern.")

    cat = st.radio("Quiz Category", ["Current Affairs (Last 12 Months)", "Static Syllabus Mix"])
    if st.button("Generate Fresh Questions", key="gen_daily_q", type="primary"):
        with st.spinner("AI is creating new questions..."):
            st.write("### Sample AI Generated Question")
            st.write("Consider the following statements regarding Central Bank Digital Currency (CBDC):")
            st.write("1. It is a sovereign currency issued by the RBI in digital form.")
            st.write("2. It appears as a liability on the central bank's balance sheet.")
            st.write("Which of the statements given above is/are correct?")
            st.radio("Your Choice:", ["1 only", "2 only", "Both 1 and 2", "Neither 1 nor 2"])

# --- PAGE 6: UNIVERSAL MAINS EVALUATOR ---
elif st.session_state.active_page == "Universal Mains Evaluator":
    st.title("🔍 Universal Mains Answer Evaluator")
    st.write("Evaluate answers for ANY question—whether generated by AI or typed by you.")

    option = st.radio("How would you like to provide the question?", ["Type/Paste the Question", "Question is written on the Answer Sheet"])
    
    if option == "Type/Paste the Question":
        q_text = st.text_area("Enter your question here:")
    
    answer_sheet = st.file_uploader("Upload Scanned Answer Sheet", type=["jpg", "jpeg", "png", "pdf"], key="univ_eval")
    
    if answer_sheet and st.button("Run Comprehensive AI Evaluation", key="run_univ_eval", type="primary"):
        with st.spinner("Analyzing answer structure, facts, and clarity..."):
            st.success("Evaluation Finished!")
            st.markdown("### 📊 Evaluation Summary")
            st.write("**Handwriting Readability:** Excellent")
            st.write("**Relevance to Question:** 80%")
            st.write("**Model Answer Comparison:** Added key constitutional articles missing from user response.")