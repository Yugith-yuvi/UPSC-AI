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

# Initialize active page state
if "active_page" not in st.session_state:
    st.session_state.active_page = "Home"

# Handle query parameters for page navigation
query_params = st.query_params
if "page" in query_params:
    st.session_state.active_page = query_params["page"]

def navigate_to(page_name):
    st.session_state.active_page = page_name
    st.query_params["page"] = page_name

# --- MODERN INJECTED CSS FOR DARK DASHBOARD & GLASSMORPHISM ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap');

    /* Dark Mode Core Theme */
    html, body, [class*="stApp"] {
        font-family: 'Outfit', sans-serif !important;
        background-color: #0b0f19 !important;
        color: #f1f5f9 !important;
    }

    /* Clean Header Navigation Button Styling */
    div[data-testid="column"]:nth-child(1) button {
        height: 42px !important;
        border-radius: 12px !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        color: #38bdf8 !important;
        font-weight: 700 !important;
        backdrop-filter: blur(8px) !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="column"]:nth-child(1) button:hover {
        background: rgba(56, 189, 248, 0.15) !important;
        border-color: #38bdf8 !important;
        color: #ffffff !important;
        transform: translateY(-2px) !important;
    }

    /* Hero Text Styling */
    .hero-glow-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
    }
    
    .hero-sub {
        font-size: 1.1rem;
        color: #94a3b8;
        margin-bottom: 24px;
        font-weight: 500;
    }

    /* Stats Banner Styling */
    .stat-box {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 12px 20px;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    .stat-number {
        font-size: 1.3rem;
        font-weight: 800;
        color: #38bdf8;
    }
    .stat-label {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
</style>
""", unsafe_allow_html=True)

# --- TOP NAVIGATION BAR ---
col_nav1, col_nav2, _ = st.columns([1.2, 1.2, 9.6])

with col_nav1:
    if st.button("🏠 Home", key="btn_top_home", use_container_width=True):
        navigate_to("Home")
        st.rerun()

with col_nav2:
    with st.popover("☰ Menu"):
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

st.markdown("---")

# Helper function to render neon glassmorphic cards
def render_neon_card(icon, title, tag, description, accent_gradient, glow_color, target_page):
    card_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: 'Outfit', sans-serif; background: transparent; padding: 6px; }}
        
        .card {{
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 18px;
            padding: 22px;
            height: 175px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
            cursor: pointer;
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
            box-shadow: 0 20px 35px -10px {glow_color}33, 0 0 15px {glow_color}22;
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
            color: #f8fafc;
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
            color: #94a3b8;
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
            padding: 6px 14px;
            border-radius: 20px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            box-shadow: 0 4px 12px {glow_color}44;
            transition: all 0.2s ease;
        }}

        .card:hover .launch-btn {{
            transform: translateX(3px);
        }}
    </style>
    </head>
    <body>
        <div class="card" onclick="openPage()">
            <div>
                <div class="header-row">
                    <div class="title"><span>{icon}</span> {title}</div>
                    <span class="badge">{tag}</span>
                </div>
                <div class="desc">{description}</div>
            </div>
            <div class="action-row">
                <div class="launch-btn">Launch Tool &rarr;</div>
            </div>
        </div>

        <script>
            function openPage() {{
                window.parent.location.href = window.parent.location.pathname + '?page={target_page}';
            }}
        </script>
    </body>
    </html>
    """
    components.html(card_html, height=190)

# --- PAGE 1: WELCOME DASHBOARD ---
if st.session_state.active_page == "Home":
    st.markdown('<div class="hero-glow-title">⚡ UPSC AI Quest Hub</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Next-generation AI engine for Prelims, Mains, and CSAT practice.</div>', unsafe_allow_html=True)

    # Dynamic Stat Bar
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown('<div class="stat-box"><div class="stat-number">2006–2025</div><div class="stat-label">Official PYQs</div></div>', unsafe_allow_html=True)
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
            "Prelims 2006–2025",
            "Custom test builder filtering by subject, topic, and year range with instant automated scoring.",
            "linear-gradient(135deg, #10b981 0%, #059669 100%)",
            "#10b981",
            "Prelims PYQ Quiz"
        )
    with col2:
        render_neon_card(
            "✍️",
            "Mains PYQ Writing",
            "Handwriting OCR",
            "Select official Mains questions, write on paper, and upload a photo for detailed AI evaluation.",
            "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)",
            "#3b82f6",
            "Mains PYQ Practice"
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
            "CSAT PYQ Quiz"
        )
    with col4:
        render_neon_card(
            "⚡",
            "Dynamic Quiz Generator",
            "Current Affairs",
            "Generate fresh practice questions instantly based on recent news and static UPSC syllabus topics.",
            "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
            "#f59e0b",
            "Daily Quiz Generator"
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
            "Universal Mains Evaluator"
        )

# --- PAGE 2: PRELIMS PYQ QUIZ ---
elif st.session_state.active_page == "Prelims PYQ Quiz":
    st.title("🎯 Prelims Past Year Question Quiz")
    st.write("Select your criteria below to generate your custom practice test.")

    col1, col2 = st.columns(2)
    with col1:
        subject = st.selectbox("Select Subject", ["Polity & Governance", "Economy", "Modern History", "Environment & Ecology", "Science & Technology", "Geography"])
    with col2:
        years = st.slider("Select Year Range", 2006, 2025, (2015, 2025))

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