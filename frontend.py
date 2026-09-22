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
subtext_color = "#cbd5e1" if is_dark else "#475569"  # Brighter text for better contrast

nav_btn_bg = "#1e293b" if is_dark else "#ffffff"
nav_btn_border = "#334155" if is_dark else "#cbd5e1"
nav_btn_text = "#f8fafc" if is_dark else "#0f172a"

stat_bg = "rgba(30, 41, 59, 0.5)" if is_dark else "#ffffff"
stat_border = "rgba(255, 255, 255, 0.08)" if is_dark else "#e2e8f0"

c_bg = "linear-gradient(145deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%)" if is_dark else "#ffffff"
c_border = "rgba(255, 255, 255, 0.1)" if is_dark else "#e2e8f0"
c_title = "#f8fafc" if is_dark else "#0f172a"
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
    div[data-testid="stColumn"] button,
    div[data-testid="stPopover"] > button,
    div[data-testid="stBaseButton-secondary"] {{
        background-color: {nav_btn_bg} !important;
        border: 1px solid {nav_btn_border} !important;
        border-radius: 10px !important;
        height: 44px !important;
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
        font-size: 1rem !important;
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

    /* 3. TOGGLE SWITCH CONTAINER STYLING */
    div[data-testid="stCheckbox"] {{
        background: {nav_btn_bg} !important;
        border: 1px solid {nav_btn_border} !important;
        padding: 6px 14px !important;
        border-radius: 10px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        height: 44px !important;
    }}

    div[data-testid="stCheckbox"] label p {{
        color: {nav_btn_text} !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }}

    /* Typography & Stat Bar */
    .hero-glow-title {{
        font-size: 2.8rem;
        font-weight: 800;
        background: {'linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #38bdf8 100%)' if is_dark else 'linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #2563eb 100%)'};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }}
    
    .hero-sub {{
        font-size: 1.25rem;
        color: {subtext_color};
        margin-bottom: 24px;
        font-weight: 500;
    }}

    .stat-box {{
        background: {stat_bg};
        border: 1px solid {stat_border};
        border-radius: 14px;
        padding: 16px 20px;
        text-align: center;
        backdrop-filter: blur(10px);
    }}
    .stat-number {{
        font-size: 1.5rem;
        font-weight: 800;
        color: {'#38bdf8' if is_dark else '#2563eb'};
    }}
    .stat-label {{
        font-size: 0.85rem;
        color: {subtext_color};
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 600;
    }}

    /* CLICKABLE CARD STYLING VIA STREAMLIT CONTAINER OVERRIDES */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(div.card-marker) {{
        background: {c_bg} !important;
        border: 1px solid {c_border} !important;
        border-radius: 20px !important;
        padding: 26px !important;
        box-shadow: {c_shadow} !important;
        transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
        position: relative !important;
    }}

    div[data-testid="stVerticalBlockBorderWrapper"]:has(div.card-marker):hover {{
        transform: translateY(-6px) !important;
    }}

    /* Inverted overlay button trick to make full container clickable */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(div.card-marker) button[aria-label="card_click"] {{
        position: absolute !important;
        inset: 0 !important;
        width: 100% !important;
        height: 100% !important;
        z-index: 10 !important;
        opacity: 0 !important;
        cursor: pointer !important;
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

# Helper function to render theme-aware native card components with boosted font sizing
def render_neon_card(icon, title, tag, description, accent_gradient, glow_color, target_page, card_id):
    st.markdown(f"""
    <style>
        div[data-testid="stVerticalBlockBorderWrapper"]:has(div.card-{card_id}) {{
            border-top: 4px solid {glow_color} !important;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"]:has(div.card-{card_id}):hover {{
            border-color: {glow_color}aa !important;
            box-shadow: 0 20px 35px -10px {glow_color}44, 0 0 20px {glow_color}22 !important;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown(f'<div class="card-marker card-{card_id}"></div>', unsafe_allow_html=True)
        
        # Upper portion with boosted fonts
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
            <div style="font-size: 1.45rem; font-weight: 700; color: {c_title}; display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.6rem;">{icon}</span> {title}
            </div>
            <span style="font-size: 0.78rem; font-weight: 700; padding: 5px 12px; border-radius: 20px; background: {glow_color}22; color: {glow_color}; border: 1px solid {glow_color}55; text-transform: uppercase; letter-spacing: 0.8px;">{tag}</span>
        </div>
        <div style="font-size: 1.05rem; color: {subtext_color}; line-height: 1.6; font-weight: 400; text-align: left; margin-bottom: 24px;">{description}</div>
        <div style="display: flex; justify-content: flex-end; align-items: center;">
            <div style="font-size: 0.95rem; font-weight: 700; color: #ffffff; background: {accent_gradient}; padding: 8px 18px; border-radius: 20px; display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 4px 14px {glow_color}44;">
                Launch Tool &rarr;
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Invisible full-card overlay button
        if st.button("card_click", key=f"card_btn_{card_id}", help=f"Open {title}"):
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
            "1"
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
            "2"
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
            "3"
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
            "4"
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
            "5"
        )