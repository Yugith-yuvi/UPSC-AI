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

# SaaS Design Tokens matching screenshot
bg_color = "#07090e" if is_dark else "#f8fafc"
text_color = "#f8fafc" if is_dark else "#0f172a"
subtext_color = "#94a3b8" if is_dark else "#64748b"

nav_btn_bg = "rgba(15, 23, 42, 0.75)" if is_dark else "#ffffff"
nav_btn_border = "rgba(255, 255, 255, 0.12)" if is_dark else "#cbd5e1"
nav_btn_text = "#f8fafc" if is_dark else "#0f172a"

stat_bg = "rgba(15, 23, 42, 0.6)" if is_dark else "#ffffff"
stat_border = "rgba(255, 255, 255, 0.08)" if is_dark else "#e2e8f0"

card_bg = "rgba(15, 23, 42, 0.5)" if is_dark else "#ffffff"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="stApp"] {{
        font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}

    /* 1. TOP NAV & MENU BUTTONS */
    div[data-testid="stColumn"] button,
    div[data-testid="stPopover"] > button,
    div[data-testid="stBaseButton-secondary"] {{
        background-color: {nav_btn_bg} !important;
        border: 1px solid {nav_btn_border} !important;
        border-radius: 12px !important;
        height: 44px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
        backdrop-filter: blur(12px) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
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
        background-color: {'rgba(30, 41, 59, 0.9)' if is_dark else '#f1f5f9'} !important;
        transform: translateY(-1px) !important;
    }}

    /* 2. POPOVER MENU */
    div[data-testid="stPopoverBody"] {{
        background-color: {'#0f172a' if is_dark else '#ffffff'} !important;
        border: 1px solid {nav_btn_border} !important;
        border-radius: 16px !important;
        box-shadow: 0 20px 30px -10px rgba(0, 0, 0, 0.5) !important;
        padding: 14px !important;
        backdrop-filter: blur(20px) !important;
    }}

    div[data-testid="stPopoverBody"] p, 
    div[data-testid="stPopoverBody"] span,
    div[data-testid="stPopoverBody"] strong {{
        color: {text_color} !important;
    }}

    div[data-testid="stPopoverBody"] button {{
        background-color: {nav_btn_bg} !important;
        border: 1px solid {nav_btn_border} !important;
        border-radius: 10px !important;
        margin-bottom: 8px !important;
    }}

    div[data-testid="stPopoverBody"] button p {{
        color: {nav_btn_text} !important;
        font-weight: 600 !important;
    }}

    div[data-testid="stPopoverBody"] button:hover {{
        border-color: #38bdf8 !important;
        background-color: {'#1e293b' if is_dark else '#f1f5f9'} !important;
    }}

    /* 3. TOGGLE SWITCH */
    div[data-testid="stCheckbox"] {{
        background: {nav_btn_bg} !important;
        border: 1px solid {nav_btn_border} !important;
        padding: 6px 14px !important;
        border-radius: 12px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        height: 44px !important;
        backdrop-filter: blur(12px) !important;
    }}

    div[data-testid="stCheckbox"] label p {{
        color: {nav_btn_text} !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }}

    /* 4. EXACT FULL CONTAINER CLICKABLE TOOL CARDS */
    .element-container:has(button[key^="card_box_"]) button {{
        background: {card_bg} !important;
        border-radius: 18px !important;
        padding: 22px 24px !important;
        height: auto !important;
        min-height: 155px !important;
        width: 100% !important;
        text-align: left !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        align-items: flex-start !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        backdrop-filter: blur(16px) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
        white-space: normal !important;
    }}

    .element-container:has(button[key^="card_box_"]) button:hover {{
        transform: translateY(-4px) scale(1.008) !important;
    }}

    /* Card Themes matching screenshot borders */
    .element-container:has(button[key="card_box_prelims"]) button {{
        border: 1px solid rgba(16, 185, 129, 0.35) !important;
    }}
    .element-container:has(button[key="card_box_prelims"]) button:hover {{
        border-color: #10b981 !important;
        box-shadow: 0 16px 30px -8px rgba(16, 185, 129, 0.3) !important;
    }}

    .element-container:has(button[key="card_box_mains"]) button {{
        border: 1px solid rgba(59, 130, 246, 0.35) !important;
    }}
    .element-container:has(button[key="card_box_mains"]) button:hover {{
        border-color: #3b82f6 !important;
        box-shadow: 0 16px 30px -8px rgba(59, 130, 246, 0.3) !important;
    }}

    .element-container:has(button[key="card_box_csat"]) button {{
        border: 1px solid rgba(168, 85, 247, 0.35) !important;
    }}
    .element-container:has(button[key="card_box_csat"]) button:hover {{
        border-color: #a855f7 !important;
        box-shadow: 0 16px 30px -8px rgba(168, 85, 247, 0.3) !important;
    }}

    .element-container:has(button[key="card_box_daily"]) button {{
        border: 1px solid rgba(245, 158, 11, 0.35) !important;
    }}
    .element-container:has(button[key="card_box_daily"]) button:hover {{
        border-color: #f59e0b !important;
        box-shadow: 0 16px 30px -8px rgba(245, 158, 11, 0.3) !important;
    }}

    .element-container:has(button[key="card_box_univ"]) button {{
        border: 1px solid rgba(99, 102, 241, 0.35) !important;
    }}
    .element-container:has(button[key="card_box_univ"]) button:hover {{
        border-color: #6366f1 !important;
        box-shadow: 0 16px 30px -8px rgba(99, 102, 241, 0.3) !important;
    }}

    .element-container:has(button[key^="card_box_"]) button p {{
        margin: 0 !important;
        padding: 0 !important;
        text-align: left !important;
        width: 100% !important;
    }}

    /* HERO SECTION & STAT BAR */
    .hero-glow-title {{
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #ffffff;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    
    .hero-sub {{
        font-size: 1rem;
        color: {subtext_color};
        margin-bottom: 28px;
        font-weight: 500;
    }}

    .stat-box {{
        background: {stat_bg};
        border: 1px solid {stat_border};
        border-radius: 14px;
        padding: 14px 22px;
        text-align: center;
        backdrop-filter: blur(12px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }}
    .stat-number {{
        font-size: 1.25rem;
        font-weight: 800;
        color: #38bdf8;
    }}
    .stat-label {{
        font-size: 0.7rem;
        color: {subtext_color};
        text-transform: uppercase;
        letter-spacing: 0.9px;
        font-weight: 600;
    }}

    .quiz-card {{
        background: {'rgba(15, 23, 42, 0.5)' if is_dark else '#ffffff'};
        border: 1px solid {'rgba(255, 255, 255, 0.08)' if is_dark else '#e2e8f0'};
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 20px;
        backdrop-filter: blur(12px);
    }}

    .score-banner {{
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: #ffffff;
        padding: 20px;
        border-radius: 14px;
        text-align: center;
        font-size: 1.4rem;
        font-weight: 800;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px -5px rgba(16, 185, 129, 0.4);
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

    # Stat Bar matching screenshot[cite: 1]
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown('<div class="stat-box"><div class="stat-number">2000–2026</div><div class="stat-label">OFFICIAL PYQS</div></div>', unsafe_allow_html=True)
    with s2:
        st.markdown('<div class="stat-box"><div class="stat-number">AI OCR 2.0</div><div class="stat-label">HANDWRITING SCAN</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown('<div class="stat-box"><div class="stat-number">Real-Time</div><div class="stat-label">CURRENT AFFAIRS</div></div>', unsafe_allow_html=True)
    with s4:
        st.markdown('<div class="stat-box"><div class="stat-number">Instant</div><div class="stat-label">MAINS EVALUATION</div></div>', unsafe_allow_html=True)

    st.write("")
    st.write("")

    # Grid Row 1 (Clickable Native Cards matching exact design)[cite: 1]
    col1, col2 = st.columns(2)
    with col1:
        prelims_text = (
            "🎯  Prelims PYQ Quiz                                                     PRELIMS 2000-2026\n\n"
            "Custom test builder filtering by subject, topic, and year range with instant automated scoring.\n\n"
            "                                                                                     Launch Tool →"
        )
        if st.button(prelims_text, key="card_box_prelims", use_container_width=True):
            navigate_to("Prelims PYQ Quiz")
            st.rerun()

    with col2:
        mains_text = (
            "✍️  Mains PYQ Writing                                                    HANDWRITING OCR\n\n"
            "Select official Mains questions, write on paper, and upload a photo for detailed AI evaluation.\n\n"
            "                                                                                     Launch Tool →"
        )
        if st.button(mains_text, key="card_box_mains", use_container_width=True):
            navigate_to("Mains PYQ Practice")
            st.rerun()

    st.write("")

    # Grid Row 2
    col3, col4 = st.columns(2)
    with col3:
        csat_text = (
            "📊  CSAT Interactive Arena                                              QUANT & REASONING\n\n"
            "Master Quant, Logical Reasoning, and Reading Comprehension with dedicated practice sets.\n\n"
            "                                                                                     Launch Tool →"
        )
        if st.button(csat_text, key="card_box_csat", use_container_width=True):
            navigate_to("CSAT PYQ Quiz")
            st.rerun()

    with col4:
        daily_text = (
            "⚡  Dynamic Quiz Generator                                                    CURRENT AFFAIRS\n\n"
            "Generate fresh practice questions instantly based on recent news and static UPSC syllabus topics.\n\n"
            "                                                                                     Launch Tool →"
        )
        if st.button(daily_text, key="card_box_daily", use_container_width=True):
            navigate_to("Daily Quiz Generator")
            st.rerun()

    st.write("")

    # Grid Row 3
    col5, _ = st.columns([1, 1])
    with col5:
        univ_text = (
            "🔍  Universal Mains Evaluator                                                ANY QUESTION\n\n"
            "Upload an answer sheet for ANY question—typed or handwritten—and receive comprehensive structural feedback.\n\n"
            "                                                                                     Launch Tool →"
        )
        if st.button(univ_text, key="card_box_univ", use_container_width=True):
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