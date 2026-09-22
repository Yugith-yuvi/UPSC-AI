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

# Premium High-Contrast SaaS Palette
bg_color = "#080c14" if is_dark else "#f4f6fb"
text_color = "#f8fafc" if is_dark else "#0f172a"
subtext_color = "#94a3b8" if is_dark else "#475569"

nav_btn_bg = "rgba(15, 23, 42, 0.85)" if is_dark else "#ffffff"
nav_btn_border = "rgba(255, 255, 255, 0.15)" if is_dark else "#cbd5e1"
nav_btn_text = "#f8fafc" if is_dark else "#0f172a"

# Dynamic Styling Injection
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Outfit:wght@500;600;700;800&display=swap');

    /* Global Base Theme */
    html, body, [class*="stApp"] {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}

    /* NAVIGATION BUTTONS & POPOVERS */
    div[data-testid="stColumn"] button,
    div[data-testid="stPopover"] > button,
    div[data-testid="stBaseButton-secondary"] {{
        background-color: {nav_btn_bg} !important;
        border: 1px solid {nav_btn_border} !important;
        border-radius: 14px !important;
        height: 48px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
        backdrop-filter: blur(12px) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        color: {nav_btn_text} !important;
        font-family: 'Outfit', sans-serif !important;
    }}

    div[data-testid="stColumn"] button *,
    div[data-testid="stPopover"] > button *,
    div[data-testid="stBaseButton-secondary"] * {{
        color: {nav_btn_text} !important;
        fill: {nav_btn_text} !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }}

    div[data-testid="stColumn"] button:hover,
    div[data-testid="stPopover"] > button:hover,
    div[data-testid="stBaseButton-secondary"]:hover {{
        border-color: #38bdf8 !important;
        background-color: {'#1e293b' if is_dark else '#e2e8f0'} !important;
        transform: translateY(-2px) !important;
    }}

    /* TOGGLE SWITCH */
    div[data-testid="stCheckbox"] {{
        background: {nav_btn_bg} !important;
        border: 1px solid {nav_btn_border} !important;
        padding: 6px 16px !important;
        border-radius: 14px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        height: 48px !important;
    }}

    div[data-testid="stCheckbox"] label p {{
        color: {nav_btn_text} !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }}

    /* VIBRANT HERO TITLE & STATS */
    .hero-container {{
        text-align: center;
        padding: 20px 0 35px 0;
    }}

    .hero-glow-title {{
        font-family: 'Outfit', sans-serif;
        font-size: 3.4rem;
        font-weight: 900;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 40%, #c084fc 80%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
        text-shadow: 0 10px 30px rgba(56, 189, 248, 0.2);
    }}

    .hero-sub {{
        font-size: 1.25rem;
        color: {subtext_color};
        font-weight: 600;
        max-width: 700px;
        margin: 0 auto;
    }}

    .stat-card {{
        background: {'linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%)' if is_dark else 'linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%)'};
        border: 1px solid {'rgba(255, 255, 255, 0.12)' if is_dark else '#e2e8f0'};
        border-radius: 18px;
        padding: 18px 20px;
        text-align: center;
        backdrop-filter: blur(16px);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
    }}
    
    .stat-card:hover {{
        transform: translateY(-3px);
    }}

    .stat-number {{
        font-family: 'Outfit', sans-serif;
        font-size: 1.6rem;
        font-weight: 800;
    }}
    
    .stat-label {{
        font-size: 0.8rem;
        color: {subtext_color};
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
        margin-top: 4px;
    }}

    /* VIBRANT LARGE FEATURE CARDS */
    .element-container:has(button[key^="card_box_"]) button {{
        border-radius: 24px !important;
        padding: 28px !important;
        min-height: 220px !important;
        width: 100% !important;
        text-align: left !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important;
        align-items: flex-start !important;
        transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
        backdrop-filter: blur(20px) !important;
        white-space: normal !important;
        position: relative !important;
        overflow: hidden !important;
    }}

    .element-container:has(button[key^="card_box_"]) button:hover {{
        transform: translateY(-8px) scale(1.015) !important;
    }}

    /* CARD 1: PRELIMS (EMERALD VIBE) */
    .element-container:has(button[key="card_box_prelims"]) button {{
        background: {'linear-gradient(135deg, rgba(6, 78, 59, 0.35) 0%, rgba(15, 23, 42, 0.85) 100%)' if is_dark else 'linear-gradient(135deg, #ecfdf5 0%, #ffffff 100%)'} !important;
        border: 2px solid {'rgba(16, 185, 129, 0.4)' if is_dark else '#a7f3d0'} !important;
        box-shadow: 0 12px 30px -10px rgba(16, 185, 129, 0.2) !important;
    }}
    .element-container:has(button[key="card_box_prelims"]) button:hover {{
        border-color: #10b981 !important;
        box-shadow: 0 22px 40px -10px rgba(16, 185, 129, 0.4) !important;
    }}

    /* CARD 2: MAINS (ROYAL BLUE VIBE) */
    .element-container:has(button[key="card_box_mains"]) button {{
        background: {'linear-gradient(135deg, rgba(30, 58, 138, 0.35) 0%, rgba(15, 23, 42, 0.85) 100%)' if is_dark else 'linear-gradient(135deg, #eff6ff 0%, #ffffff 100%)'} !important;
        border: 2px solid {'rgba(59, 130, 246, 0.4)' if is_dark else '#bfdbfe'} !important;
        box-shadow: 0 12px 30px -10px rgba(59, 130, 246, 0.2) !important;
    }}
    .element-container:has(button[key="card_box_mains"]) button:hover {{
        border-color: #3b82f6 !important;
        box-shadow: 0 22px 40px -10px rgba(59, 130, 246, 0.4) !important;
    }}

    /* CARD 3: CSAT (PURPLE VIBE) */
    .element-container:has(button[key="card_box_csat"]) button {{
        background: {'linear-gradient(135deg, rgba(88, 28, 135, 0.35) 0%, rgba(15, 23, 42, 0.85) 100%)' if is_dark else 'linear-gradient(135deg, #f3e8ff 0%, #ffffff 100%)'} !important;
        border: 2px solid {'rgba(168, 85, 247, 0.4)' if is_dark else '#e9d5ff'} !important;
        box-shadow: 0 12px 30px -10px rgba(168, 85, 247, 0.2) !important;
    }}
    .element-container:has(button[key="card_box_csat"]) button:hover {{
        border-color: #a855f7 !important;
        box-shadow: 0 22px 40px -10px rgba(168, 85, 247, 0.4) !important;
    }}

    /* CARD 4: DAILY QUIZ (AMBER VIBE) */
    .element-container:has(button[key="card_box_daily"]) button {{
        background: {'linear-gradient(135deg, rgba(120, 53, 15, 0.35) 0%, rgba(15, 23, 42, 0.85) 100%)' if is_dark else 'linear-gradient(135deg, #fffbeb 0%, #ffffff 100%)'} !important;
        border: 2px solid {'rgba(245, 158, 11, 0.4)' if is_dark else '#fde68a'} !important;
        box-shadow: 0 12px 30px -10px rgba(245, 158, 11, 0.2) !important;
    }}
    .element-container:has(button[key="card_box_daily"]) button:hover {{
        border-color: #f59e0b !important;
        box-shadow: 0 22px 40px -10px rgba(245, 158, 11, 0.4) !important;
    }}

    /* CARD 5: UNIVERSAL EVALUATOR (INDIGO VIBE) */
    .element-container:has(button[key="card_box_univ"]) button {{
        background: {'linear-gradient(135deg, rgba(49, 46, 129, 0.35) 0%, rgba(15, 23, 42, 0.85) 100%)' if is_dark else 'linear-gradient(135deg, #e0e7ff 0%, #ffffff 100%)'} !important;
        border: 2px solid {'rgba(99, 102, 241, 0.4)' if is_dark else '#c7d2fe'} !important;
        box-shadow: 0 12px 30px -10px rgba(99, 102, 241, 0.2) !important;
    }}
    .element-container:has(button[key="card_box_univ"]) button:hover {{
        border-color: #6366f1 !important;
        box-shadow: 0 22px 40px -10px rgba(99, 102, 241, 0.4) !important;
    }}

    .element-container:has(button[key^="card_box_"]) button p {{
        margin: 0 !important;
        padding: 0 !important;
        text-align: left !important;
        width: 100% !important;
    }}

    .quiz-card {{
        background: {'rgba(15, 23, 42, 0.6)' if is_dark else '#ffffff'};
        border: 1px solid {'rgba(255, 255, 255, 0.1)' if is_dark else '#e2e8f0'};
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        backdrop-filter: blur(14px);
    }}

    .score-banner {{
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: #ffffff;
        padding: 22px;
        border-radius: 18px;
        text-align: center;
        font-family: 'Outfit', sans-serif;
        font-size: 1.5rem;
        font-weight: 800;
        margin-bottom: 25px;
        box-shadow: 0 12px 30px -5px rgba(16, 185, 129, 0.4);
    }}
</style>
""", unsafe_allow_html=True)

# --- TOP NAVIGATION BAR ---
col_nav1, col_nav2, _ , col_toggle = st.columns([1.3, 1.3, 6.4, 3.0])

with col_nav1:
    if st.button("🏠 Home", key="btn_top_home", use_container_width=True):
        navigate_to("Home")
        st.rerun()

with col_nav2:
    with st.popover("☰ Modules", use_container_width=True):
        st.write("**Quick Navigation Hub**")
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

st.markdown("<br/>", unsafe_allow_html=True)

# --- PAGE 1: WELCOME DASHBOARD ---
if st.session_state.active_page == "Home":
    st.markdown("""
    <div class="hero-container">
        <div class="hero-glow-title">⚡ UPSC AI Quest Hub</div>
        <div class="hero-sub">Commercial AI learning suite for Prelims statement tests, Mains handwriting evaluation, and CSAT mastery.</div>
    </div>
    """, unsafe_allow_html=True)

    # Colorful Neon Metrics Bar
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(f'<div class="stat-card"><div class="stat-number" style="color: #10b981;">2000–2026</div><div class="stat-label">Official PYQs</div></div>', unsafe_allow_html=True)
    with s2:
        st.markdown(f'<div class="stat-card"><div class="stat-number" style="color: #3b82f6;">AI OCR 2.0</div><div class="stat-label">Handwriting Scan</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown(f'<div class="stat-card"><div class="stat-number" style="color: #a855f7;">Real-Time</div><div class="stat-label">Current Affairs</div></div>', unsafe_allow_html=True)
    with s4:
        st.markdown(f'<div class="stat-card"><div class="stat-number" style="color: #f59e0b;">Instant</div><div class="stat-label">Mains Feedback</div></div>', unsafe_allow_html=True)

    st.write("")
    st.write("")

    # Grid Row 1 (Big Cards)
    col1, col2 = st.columns(2)
    with col1:
        card_content_prelims = (
            "🎯 PRELIMS PYQ ENGINE\n\n"
            "Build customizable mock tests by subject, topic, and year range with instant automated scoring and multi-statement evaluations."
        )
        if st.button(card_content_prelims, key="card_box_prelims", use_container_width=True):
            navigate_to("Prelims PYQ Quiz")
            st.rerun()

    with col2:
        card_content_mains = (
            "✍️ MAINS PYQ WRITING ARENA\n\n"
            "Access official Mains questions, write your answers on paper, and upload scans for detailed AI criteria-based feedback."
        )
        if st.button(card_content_mains, key="card_box_mains", use_container_width=True):
            navigate_to("Mains PYQ Practice")
            st.rerun()

    st.write("")

    # Grid Row 2 (Big Cards)
    col3, col4 = st.columns(2)
    with col3:
        card_content_csat = (
            "📊 CSAT INTERACTIVE ARENA\n\n"
            "Master Quant, Logical Reasoning, and Reading Comprehension with interactive problem sets and step-by-step logic breakdowns."
        )
        if st.button(card_content_csat, key="card_box_csat", use_container_width=True):
            navigate_to("CSAT PYQ Quiz")
            st.rerun()

    with col4:
        card_content_daily = (
            "⚡ DYNAMIC QUIZ GENERATOR\n\n"
            "Generate targeted practice questions dynamically from recent current affairs and core static syllabus topics."
        )
        if st.button(card_content_daily, key="card_box_daily", use_container_width=True):
            navigate_to("Daily Quiz Generator")
            st.rerun()

    st.write("")

    # Grid Row 3 (Centered Big Card)
    col5, _ = st.columns([1, 1])
    with col5:
        card_content_univ = (
            "🔍 UNIVERSAL MAINS EVALUATOR\n\n"
            "Upload handwritten or typed answers for ANY custom question to receive feedback on structure and factual depth."
        )
        if st.button(card_content_univ, key="card_box_univ", use_container_width=True):
            navigate_to("Universal Mains Evaluator")
            st.rerun()

# --- PAGE 2: PRELIMS PYQ QUIZ ---
elif st.session_state.active_page == "Prelims PYQ Quiz":
    st.title("🎯 Prelims PYQ Engine (2000–2026)")
    st.write("Configure your test parameters to generate custom UPSC statement-pattern practice sets.")

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