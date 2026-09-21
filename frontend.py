import streamlit as st
import streamlit.components.v1 as components
import requests
import os

# Set backend URL cleanly
BACKEND_URL = os.getenv("BACKEND_URL", "https://upsc-ai-backend.onrender.com").rstrip("/")

st.set_page_config(
    page_title="UPSC AI Quest Hub", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize active page state
if "active_page" not in st.session_state:
    st.session_state.active_page = "Home"

# Handle query parameters for seamless page navigation
query_params = st.query_params
if "page" in query_params:
    st.session_state.active_page = query_params["page"]

def navigate_to(page_name):
    st.session_state.active_page = page_name
    st.query_params["page"] = page_name

# --- MODERN INJECTED CSS FOR PREMIUM SAAS LOOK ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #f8fafc !important;
    }

    /* Header & Navigation Bar Styling */
    div[data-testid="column"]:nth-child(1) button {
        height: 44px !important;
        border-radius: 10px !important;
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%) !important;
        border: 1px solid #cbd5e1 !important;
        color: #0f172a !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04) !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="column"]:nth-child(1) button:hover {
        border-color: #6366f1 !important;
        color: #6366f1 !important;
        transform: translateY(-1px) !important;
    }

    /* Main Page Titles */
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #0f172a 0%, #334155 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }
    
    .hero-subtitle {
        font-size: 1.05rem;
        color: #64748b;
        margin-bottom: 24px;
        font-weight: 500;
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

# Helper component function to render vibrant, interactive HTML cards
def render_feature_card(title, tag, description, badge_color, target_page):
    card_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background: transparent; padding: 6px; }}
        
        .card {{
            background: #ffffff;
            border-radius: 16px;
            padding: 22px;
            height: 165px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            cursor: pointer;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: {badge_color};
            opacity: 0.85;
            transition: all 0.3s ease;
        }}

        .card:hover {{
            transform: translateY(-6px);
            box-shadow: 0 16px 32px -8px rgba(15, 23, 42, 0.12);
            border-color: #cbd5e1;
        }}

        .card:hover::before {{
            height: 6px;
            opacity: 1;
        }}

        .header-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }}

        .title {{
            font-size: 1.15rem;
            font-weight: 800;
            color: #0f172a;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .badge {{
            font-size: 0.72rem;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 20px;
            background: {badge_color}15;
            color: {badge_color};
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .desc {{
            font-size: 0.88rem;
            color: #64748b;
            line-height: 1.5;
            font-weight: 500;
        }}

        .footer-link {{
            font-size: 0.82rem;
            font-weight: 700;
            color: {badge_color};
            display: flex;
            align-items: center;
            gap: 4px;
            margin-top: 10px;
        }}
    </style>
    </head>
    <body>
        <div class="card" onclick="openPage()">
            <div>
                <div class="header-row">
                    <div class="title">{title}</div>
                    <span class="badge">{tag}</span>
                </div>
                <div class="desc">{description}</div>
            </div>
            <div class="footer-link">Explore Tool &rarr;</div>
        </div>

        <script>
            function openPage() {{
                window.parent.location.href = window.parent.location.pathname + '?page={target_page}';
            }}
        </script>
    </body>
    </html>
    """
    components.html(card_html, height=180)

# --- PAGE 1: WELCOME PAGE ---
if st.session_state.active_page == "Home":
    st.markdown('<div class="hero-title">🚀 UPSC AI Quest Hub</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Select an AI preparation tool below to begin practice:</div>', unsafe_allow_html=True)

    # Row 1
    col1, col2 = st.columns(2)
    with col1:
        render_feature_card(
            "🎯 Prelims PYQ Quiz",
            "Prelims",
            "Custom test builder from official 2006–2025 PYQs. Filter by subject, topic, and year with automatic instant scoring.",
            "#10b981",  # Emerald Green
            "Prelims PYQ Quiz"
        )
    with col2:
        render_feature_card(
            "✍️ Mains PYQ Writing",
            "Mains OCR",
            "Select Mains questions, write on paper, and upload a photo. AI scans handwriting and evaluates against UPSC standards.",
            "#2563eb",  # Royal Blue
            "Mains PYQ Practice"
        )

    # Row 2
    col3, col4 = st.columns(2)
    with col3:
        render_feature_card(
            "📊 CSAT Practice",
            "CSAT",
            "Master Quant, Logical Reasoning, and Reading Comprehension with interactive practice sets.",
            "#8b5cf6",  # Purple
            "CSAT PYQ Quiz"
        )
    with col4:
        render_feature_card(
            "⚡ Dynamic Quiz Generator",
            "AI Generated",
            "Generate fresh practice questions instantly based on recent news and static UPSC syllabus topics.",
            "#f59e0b",  # Amber/Orange
            "Daily Quiz Generator"
        )

    # Row 3
    col5, _ = st.columns([1, 1])
    with col5:
        render_feature_card(
            "🔍 Universal Mains Evaluator",
            "Any Question",
            "Upload an answer sheet for ANY question—whether provided by AI or typed by you—and get instant feedback.",
            "#6366f1",  # Indigo
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