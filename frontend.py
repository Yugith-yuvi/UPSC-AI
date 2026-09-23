import streamlit as st
import streamlit.components.v1 as components
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

# Helper function to render theme-aware card components
def render_neon_card(icon, title, tag, description, accent_gradient, glow_color, target_page, key):
    c_bg = "linear-gradient(145deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%)" if is_dark else "#ffffff"
    c_border = "rgba(255, 255, 255, 0.1)" if is_dark else "#e2e8f0"
    c_title = "#f8fafc" if is_dark else "#0f172a"
    c_desc = "#94a3b8" if is_dark else "#64748b"
    c_shadow = "0 10px 25px -5px rgba(0, 0, 0, 0.4)" if is_dark else "0 4px 12px rgba(15, 23, 42, 0.05)"

    # Safely encode the page name for the URL
    import urllib.parse
    page_url = "?page=" + urllib.parse.quote(target_page)

    card_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&display=swap" rel="stylesheet">

        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}

            body {{
                font-family: 'Outfit', sans-serif;
                background: transparent;
                padding: 6px;
            }}

            .card {{
                background: {c_bg};
                border: 1px solid {c_border};
                border-radius: 18px;
                padding: 22px;
                height: 175px;
                width: 100%;
                box-shadow: {c_shadow};
                transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
                position: relative;
                overflow: hidden;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                backdrop-filter: blur(12px);
            }}

            .card::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 3px;
                background: {accent_gradient};
                transition: all 0.3s ease;
            }}

            .card:hover {{
                transform: translateY(-8px) scale(1.01);
                border-color: {glow_color}88;
                box-shadow:
                    0 20px 35px -10px {glow_color}33,
                    0 0 15px {glow_color}22;
            }}

            .card:hover::before {{
                height: 5px;
            }}

            .header-row {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
            }}

            .title {{
                font-size: 1.2rem;
                font-weight: 700;
                color: {c_title};
                display: flex;
                align-items: center;
                gap: 10px;
            }}

            .badge {{
                font-size: 0.7rem;
                font-weight: 700;
                padding: 4px 10px;
                border-radius: 20px;
                background: {glow_color}22;
                color: {glow_color};
                border: 1px solid {glow_color}44;
                text-transform: uppercase;
                letter-spacing: 0.6px;
            }}

            .desc {{
                font-size: 0.88rem;
                color: {c_desc};
                line-height: 1.5;
                font-weight: 400;
            }}

            .action-row {{
                display: flex;
                justify-content: flex-end;
                align-items: center;
            }}

            .launch-btn {{
                font-size: 0.8rem;
                font-weight: 700;
                color: #ffffff;
                background: {accent_gradient};
                padding: 7px 14px;
                border-radius: 20px;
                display: inline-flex;
                align-items: center;
                gap: 6px;
                box-shadow: 0 4px 12px {glow_color}44;
                transition: all 0.2s ease;
                text-decoration: none;
                cursor: pointer;
            }}

            .launch-btn:hover {{
                transform: translateX(3px);
                filter: brightness(1.1);
            }}
        </style>
    </head>

    <body>

        <div class="card">

            <div>
                <div class="header-row">
                    <div class="title">
                        <span>{icon}</span>
                        {title}
                    </div>

                    <span class="badge">
                        {tag}
                    </span>
                </div>

                <div class="desc">
                    {description}
                </div>
            </div>

                    <div class="action-row">
                <div class="launch-btn">
                    Launch Tool &rarr;
                </div>
            </div>

    </body>
    </html>
    """

       # Extra height prevents the card from being cut off
       # Extra height prevents the card from being cut off
    CARD_HEIGHT = 215

    # Extra height prevents the card from being cut off
    components.html(card_html, height=CARD_HEIGHT)

    # REAL STREAMLIT BUTTON — stretched invisibly over the ENTIRE card so the whole box is clickable
    with st.container(key=f"wrap_{key}"):
        st.markdown(f"""
        <style>
        .st-key-wrap_{key} {{
            margin-top: -{CARD_HEIGHT}px;
            margin-bottom: 10px;
        }}
        .st-key-wrap_{key} button {{
            width: 100% !important;
            height: {CARD_HEIGHT}px !important;
            background: transparent !important;
            border: none !important;
            color: transparent !important;
            box-shadow: none !important;
            cursor: pointer !important;
        }}
        .st-key-wrap_{key} button:focus {{
            outline: none !important;
            box-shadow: none !important;
        }}
        </style>
        """, unsafe_allow_html=True)

        if st.button("Launch Tool →", key=key, use_container_width=True):
            navigate_to(target_page)
            st.rerun()
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
        render_neon_card(
            "🎯",
            "Prelims PYQ Quiz",
            "Prelims 2000–2026",
            "Custom test builder filtering by subject, topic, and year range with instant automated scoring.",
            "linear-gradient(135deg, #10b981 0%, #059669 100%)",
            "#10b981",
            "Prelims PYQ Quiz",
            key="launch_prelims"
        )
    with col2:
        render_neon_card(
            "✍️",
            "Mains PYQ Writing",
            "Handwriting OCR",
            "Select official Mains questions, write on paper, and upload a photo for detailed AI evaluation.",
            "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)",
            "#3b82f6",
            "Mains PYQ Practice",
            key="launch_mains"
        )

    # Grid Row 2
    col3, col4 = st.columns(2)
    with col3:
        render_neon_card(
            "📊",
            "CSAT Interactive Arena",
            "Quant & Reasoning",
            "Master Quant, Logical Reasoning, and Reading Comprehension with dedicated practice sets.",
            "linear-gradient(135deg, #a855f7 0%, #7e22ce 100%)",
            "#a855f7",
            "CSAT PYQ Quiz",
            key="launch_csat"
        )
    with col4:
        render_neon_card(
            "⚡",
            "Dynamic Quiz Generator",
            "Current Affairs",
            "Generate fresh practice questions instantly based on recent news and static UPSC syllabus topics.",
            "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
            "#f59e0b",
            "Daily Quiz Generator",
            key="launch_daily"
        )

    # Grid Row 3
    col5, _ = st.columns([1, 1])
    with col5:
        render_neon_card(
            "🔍",
            "Universal Mains Evaluator",
            "Any Question",
            "Upload an answer sheet for ANY question—typed or handwritten—and receive comprehensive structural feedback.",
            "linear-gradient(135deg, #f43f5e 0%, #be123c 100%)",
            "#f43f5e",
            "Universal Mains Evaluator",
            key="launch_universal"
        )

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
