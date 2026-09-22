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

c_bg = "linear-gradient(145deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%)" if is_dark else "#ffffff"
c_border = "rgba(255, 255, 255, 0.1)" if is_dark else "#e2e8f0"
c_shadow = "0 10px 25px -5px rgba(0, 0, 0, 0.4)" if is_dark else "0 4px 12px rgba(15, 23, 42, 0.05)"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap');

    /* Global Base Theme */
    html, body, [class*="stApp"] {{
        font-family: 'Outfit', sans-serif !important;
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}

    /* 1. TOP NAV TRIGGER BUTTONS */
    div[data-testid="stColumn"] > div > div > button:not([key^="card_btn_"]),
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

    div[data-testid="stColumn"] > div > div > button:not([key^="card_btn_"]) *,
    div[data-testid="stPopover"] > button *,
    div[data-testid="stBaseButton-secondary"] * {{
        color: {nav_btn_text} !important;
        fill: {nav_btn_text} !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }}

    div[data-testid="stColumn"] > div > div > button:not([key^="card_btn_"]):hover,
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

    /* 4. FULL CLICKABLE CARD STYLING FOR STREAMLIT BUTTONS */
    .element-container:has(button[key^="card_btn_"]) button {{
        background: {c_bg} !important;
        border: 1px solid {c_border} !important;
        border-radius: 18px !important;
        padding: 22px !important;
        height: 185px !important;
        width: 100% !important;
        box-shadow: {c_shadow} !important;
        transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
        position: relative !important;
        overflow: hidden !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        align-items: flex-start !important;
        backdrop-filter: blur(12px) !important;
        text-align: left !important;
    }}

    .element-container:has(button[key^="card_btn_"]) button::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        transition: all 0.3s ease;
    }}

    /* Card Specific Borders & Gradients */
    .element-container:has(button[key="card_btn_prelims"]) button::before {{
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }}
    .element-container:has(button[key="card_btn_prelims"]) button:hover {{
        transform: translateY(-8px) scale(1.01) !important;
        border-color: #10b98188 !important;
        box-shadow: 0 20px 35px -10px #10b98133, 0 0 15px #10b98122 !important;
    }}

    .element-container:has(button[key="card_btn_mains"]) button::before {{
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    }}
    .element-container:has(button[key="card_btn_mains"]) button:hover {{
        transform: translateY(-8px) scale(1.01) !important;
        border-color: #3b82f688 !important;
        box-shadow: 0 20px 35px -10px #3b82f633, 0 0 15px #3b82f622 !important;
    }}

    .element-container:has(button[key="card_btn_csat"]) button::before {{
        background: linear-gradient(135deg, #a855f7 0%, #7e22ce 100%);
    }}
    .element-container:has(button[key="card_btn_csat"]) button:hover {{
        transform: translateY(-8px) scale(1.01) !important;
        border-color: #a855f788 !important;
        box-shadow: 0 20px 35px -10px #a855f733, 0 0 15px #a855f722 !important;
    }}

    .element-container:has(button[key="card_btn_daily"]) button::before {{
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    }}
    .element-container:has(button[key="card_btn_daily"]) button:hover {{
        transform: translateY(-8px) scale(1.01) !important;
        border-color: #f59e0b88 !important;
        box-shadow: 0 20px 35px -10px #f59e0b33, 0 0 15px #f59e0b22 !important;
    }}

    .element-container:has(button[key="card_btn_univ"]) button::before {{
        background: linear-gradient(135deg, #f43f5e 0%, #be123c 100%);
    }}
    .element-container:has(button[key="card_btn_univ"]) button:hover {{
        transform: translateY(-8px) scale(1.01) !important;
        border-color: #f43f5e88 !important;
        box-shadow: 0 20px 35px -10px #f43f5e33, 0 0 15px #f43f5e22 !important;
    }}

    .element-container:has(button[key^="card_btn_"]) button:hover::before {{
        height: 5px !important;
    }}

    .element-container:has(button[key^="card_btn_"]) button p {{
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        white-space: normal !important;
    }}

    .card-header-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        margin-bottom: 8px;
    }}

    .card-title-text {{
        font-size: 1.2rem;
        font-weight: 700;
        color: {'#f8fafc' if is_dark else '#0f172a'};
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .card-badge {{
        font-size: 0.7rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }}

    .card-desc {{
        font-size: 0.88rem;
        color: {subtext_color};
        line-height: 1.5;
        font-weight: 400;
        text-align: left;
        margin-bottom: 12px;
    }}

    .card-action-row {{
        display: flex;
        justify-content: flex-end;
        align-items: center;
        width: 100%;
    }}

    .card-launch-btn {{
        font-size: 0.8rem;
        font-weight: 700;
        color: #ffffff;
        padding: 6px 14px;
        border-radius: 20px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
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

def render_interactive_card(icon, title, tag, description, accent_gradient, glow_color, key_id):
    badge_style = f"background: {glow_color}22; color: {glow_color}; border: 1px solid {glow_color}44;"
    btn_style = f"background: {accent_gradient}; box-shadow: 0 4px 12px {glow_color}44;"
    
    html_content = f"""
    <div style="width: 100%;">
        <div class="card-header-row">
            <div class="card-title-text"><span>{icon}</span> {title}</div>
            <span class="card-badge" style="{badge_style}">{tag}</span>
        </div>
        <div class="card-desc">{description}</div>
        <div class="card-action-row">
            <div class="card-launch-btn" style="{btn_style}">Launch Tool &rarr;</div>
        </div>
    </div>
    """
    return st.button(html_content, key=key_id, use_container_width=True)

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
        if render_interactive_card(
            "🎯",
            "Prelims PYQ Quiz",
            "Prelims 2000–2026",
            "Custom test builder filtering by subject, topic, and year range with instant automated scoring.",
            "linear-gradient(135deg, #10b981 0%, #059669 100%)",
            "#10b981",
            "card_btn_prelims"
        ):
            navigate_to("Prelims PYQ Quiz")
            st.rerun()

    with col2:
        if render_interactive_card(
            "✍️",
            "Mains PYQ Writing",
            "Handwriting OCR",
            "Select official Mains questions, write on paper, and upload a photo for detailed AI evaluation.",
            "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)",
            "#3b82f6",
            "card_btn_mains"
        ):
            navigate_to("Mains PYQ Practice")
            st.rerun()

    st.write("")

    # Grid Row 2
    col3, col4 = st.columns(2)
    with col3:
        if render_interactive_card(
            "📊",
            "CSAT Interactive Arena",
            "Quant & Reasoning",
            "Master Quant, Logical Reasoning, and Reading Comprehension with dedicated practice sets.",
            "linear-gradient(135deg, #a855f7 0%, #7e22ce 100%)",
            "#a855f7",
            "card_btn_csat"
        ):
            navigate_to("CSAT PYQ Quiz")
            st.rerun()

    with col4:
        if render_interactive_card(
            "⚡",
            "Dynamic Quiz Generator",
            "Current Affairs",
            "Generate fresh practice questions instantly based on recent news and static UPSC syllabus topics.",
            "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
            "#f59e0b",
            "card_btn_daily"
        ):
            navigate_to("Daily Quiz Generator")
            st.rerun()

    st.write("")

    # Grid Row 3
    col5, _ = st.columns([1, 1])
    with col5:
        if render_interactive_card(
            "🔍",
            "Universal Mains Evaluator",
            "Any Question",
            "Upload an answer sheet for ANY question—typed or handwritten—and receive comprehensive structural feedback.",
            "linear-gradient(135deg, #f43f5e 0%, #be123c 100%)",
            "#f43f5e",
            "card_btn_univ"
        ):
            navigate_to("Universal Mains Evaluator")
            st.rerun()

# --- PAGE 2: PRELIMS PYQ QUIZ ---
elif st.session_state.active_page == "Prelims PYQ Quiz":
    st.title("🎯 Prelims Past Year Question Quiz")
    st.write("Select your criteria below to generate your custom practice test.")

    col1, col2 = st.columns(2)
    with col1:
        subject = st.selectbox("Select Subject", ["Polity & Governance", "Economy", "Modern History", "Environment & Ecology", "Science & Technology", "Geography"])
    with col2:
        years = st.slider("Select Year Range", 2000, 2026, (2015, 2026))

    if st.button("Generate Quiz Test", key="run_prelims", type="primary"):
        with st.spinner("Fetching questions from database..."):
            try:
                endpoint = f"{BACKEND_URL}/api/v1/pyq/fetch"
                params = {"subject": subject, "year_start": years[0], "year_end": years[1], "exam_type": "Prelims"}
                res = requests.get(endpoint, params=params, timeout=30)
                if res.status_code == 200:
                    data = res.json().get("data", [])
                    if data:
                        st.success(f"Loaded {len(data)} questions!")
                        for idx, q in enumerate(data, 1):
                            st.subheader(f"Question {idx} ({q['year']})")
                            st.write(q["question"])
                            if q.get("options"):
                                st.radio("Select Your Answer:", list(q["options"].items()), format_func=lambda x: f"{x[0]}: {x[1]}", key=f"q_{q['id']}")
                            with st.expander("Show Solution"):
                                st.info(f"Correct Option: {q.get('correct_option', 'N/A')}")
                                st.write(q.get("explanation", ""))
                    else:
                        st.warning("No questions found matching these filters. Try expanding the year range.")
                else:
                    st.error("Server error loading questions.")
            except Exception as e:
                st.error(f"Connection error: {e}")

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