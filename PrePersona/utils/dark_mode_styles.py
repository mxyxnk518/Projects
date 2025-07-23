"""
Light mode styling for PrePersona pages.
This module provides minimal styling to maintain default Streamlit appearance.
"""
import streamlit as st

def apply_dark_mode():
    """
    Apply minimal styling to maintain clean Streamlit default appearance.
    This function should be called at the beginning of each page.
    """
    st.markdown("""
    <style>
    /* Remove Streamlit branding and menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide deploy button */
    .css-1rs6os {display: none;}
    .css-17eq0hr {display: none;}
    </style>
    """, unsafe_allow_html=True)

def create_navigation_sidebar():
    """
    Create a simple navigation sidebar for the PrePersona app.
    This function provides basic navigation without complex styling.
    """
    with st.sidebar:
        st.title("PREPERSONA NAVIGATION")
        
        if st.button("🏠 HOME"):
            st.switch_page("app.py")
        if st.button("💬 CHAT"):
            st.switch_page("pages/chat.py")
        if st.button("📁 UPLOAD DATA"):
            st.switch_page("pages/upload.py")
        if st.button("🔍 QUERY YOUR DATA"):
            st.switch_page("pages/query.py")
        if st.button("👤 YOUR PERSONALITY PROFILE"):
            st.switch_page("pages/profile.py")
        if st.button("🔧 DEBUG PANEL"):
            st.switch_page("pages/debug.py")
        if st.button("ℹ️ ABOUT"):
            st.switch_page("pages/about.py")