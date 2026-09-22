def render_card_and_button(icon, title, tag, description, accent_color, page_name, key_id):
    # Pure HTML for the visual card
    card_html = f"""
    <div style="
        background: {c_bg};
        border: 1px solid {c_border};
        border-top: 4px solid {accent_color};
        border-radius: 16px;
        padding: 20px;
        box-shadow: {c_shadow};
        margin-bottom: 10px;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <span style="font-size: 1.2rem; font-weight: 700; color: {text_color};">{icon} {title}</span>
            <span style="font-size: 0.7rem; font-weight: 700; padding: 4px 10px; border-radius: 20px; background: {accent_color}22; color: {accent_color}; border: 1px solid {accent_color}44;">{tag}</span>
        </div>
        <p style="font-size: 0.9rem; color: {subtext_color}; margin: 0; line-height: 1.5;">{description}</p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    if st.button(f"Launch {title} →", key=key_id, use_container_width=True):
        navigate_to(page_name)
        st.rerun()