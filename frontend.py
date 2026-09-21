import streamlit as st
import streamlit.components.v1 as components
import requests
import os

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

# Dynamic Theme Variables
bg_color = "#0b0f19" if is_dark else "#f8fafc"
text_color = "#f1f5f9" if is_dark else "#0f172a"
subtext_color = "#94a3b8" if is_dark else "#64748b"

nav_btn_bg = "#1e293b" if is_dark else "#ffffff"
nav_btn_border = "#334155" if is_dark else "#cbd5e1"
nav_btn_text = "#ffffff" if is_dark else "#0f172a"

stat_bg = "rgba(30, 41, 59, 0.5)" if is_dark else "#ffffff"
stat_border = "rgba(255, 255, 255, 0.08)" if is_dark else "#e2e8f0"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap');

    html, body, [class*="stApp"] {{
        font-family: 'Outfit', sans-serif !important;
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}

    /* FIX 1: FIX BLANK WHITE HOME & MENU BUTTONS */
    div[data-testid="stBaseButton-secondary"],
    div[data-testid="stPopover"] > button {{
        background-color: {nav_btn_bg} !important;
        border: 1px solid {nav_btn_border} !important;
        border-radius: 10px !important;
        height: 42px !important;
        box-shadow: none !important;
    }}

    /* Force button text/icon color so it is visible in dark mode */
    div[data-testid="stBaseButton-secondary"] p,
    div[data-testid="stPopover"] > button p,
    div[data-testid="stBaseButton-secondary"] span,
    div[data-testid="stPopover"] > button span {{
        color: {nav_btn_text} !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }}

    div[data-testid="stBaseButton-secondary"]:hover,
    div[data-testid="stPopover"] > button:hover {{
        border-color: #38bdf8 !important;
        background-color: {'#334155' if is_dark else '#f1f5f9'} !important;
    }}

    /* FIX 2: SLEEK TOGGLE SWITCH STYLING */
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
    # REPLACED RADIO WITH NATIVE STREAMLIT TOGGLE SWITCH
    theme_toggle = st.toggle("Dark Mode 🌙" if is_dark else "Light Mode ☀️", value=is_dark, key="theme_toggle")
    new_theme = "Dark" if theme_toggle else "Light"
    
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

st.markdown("---")