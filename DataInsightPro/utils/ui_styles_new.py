"""
UI Styling utilities for PrePersona.
This module handles custom CSS and styling for the application.
"""
import streamlit as st
from utils.mood_colors import get_user_mood, set_color_scheme

# Theme settings store - Force light mode
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = 'light'  # Force light theme
else:
    st.session_state.theme_mode = 'light'  # Force light theme always

def toggle_theme():
    """Toggle between dark and light mode."""
    if st.session_state.theme_mode == 'light':
        st.session_state.theme_mode = 'dark'
    else:
        st.session_state.theme_mode = 'light'

def get_theme_colors():
    """Get colors based on current theme."""
    if st.session_state.theme_mode == 'dark':
        return {
            'bg_primary': '#121212',
            'bg_secondary': '#1e1e1e',
            'bg_card': '#2d2d2d',
            'text_primary': '#ffffff',
            'text_secondary': '#aaaaaa',
            'accent': '#4f8bf9',
            'border': 'rgba(255,255,255,0.1)',
            'user_message_bg': '#263238',
            'ai_message_bg': '#202020',
            'button_bg': '#3d4e5d',
            'card_border': '#444444',
            'card_shadow': 'rgba(0,0,0,0.5)'
        }
    else:  # Light theme
        return {
            'bg_primary': '#ffffff',
            'bg_secondary': '#f8f9fa',
            'bg_card': '#ffffff',
            'text_primary': '#212529',
            'text_secondary': '#6c757d',
            'accent': '#4f8bf9',
            'border': 'rgba(0,0,0,0.1)',
            'user_message_bg': '#e6f7ff',
            'ai_message_bg': '#f6f6f6',
            'button_bg': '#4f8bf9',
            'card_border': '#e0e0e0',
            'card_shadow': 'rgba(0,0,0,0.05)'
        }

def apply_custom_styles():
    """Apply custom CSS styles to enhance the UI based on current theme."""
    colors = get_theme_colors()
    
    st.markdown(f"""
    <style>
    /* Theme-based colors */
    :root {{
        --bg-primary: {colors['bg_primary']};
        --bg-secondary: {colors['bg_secondary']};
        --bg-card: {colors['bg_card']};
        --text-primary: {colors['text_primary']};
        --text-secondary: {colors['text_secondary']};
        --accent: {colors['accent']};
        --border: {colors['border']};
    }}
    
    /* Global overrides for theme */
    .reportview-container .main .block-container,
    .main .block-container {{
        background-color: var(--bg-primary);
        color: var(--text-primary);
    }}
    
    .stApp {{
        background-color: var(--bg-primary);
    }}
    
    /* Main heading styles */
    h1, h2, h3, h4, h5, h6 {{
        font-weight: 600 !important;
        letter-spacing: -0.3px;
        color: {colors['text_primary']};
    }}
    
    /* Paragraph text */
    p, div, span {{
        color: {colors['text_primary']};
    }}
    
    /* Navigation menu styling */
    .css-1q8dd3e, .css-wjbhl0, .st-emotion-cache-1q8dd3e, .st-emotion-cache-wjbhl0 {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        background-color: {colors['bg_secondary']};
    }}
    
    /* Capitalize navigation menu items */
    section[data-testid="stSidebar"] .css-pkbazv, 
    section[data-testid="stSidebar"] .st-emotion-cache-pkbazv,
    section[data-testid="stSidebar"] .st-emotion-cache-16txtl3,
    section[data-testid="stSidebar"] .css-16txtl3 {{
        text-transform: capitalize !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        color: {colors['text_primary']} !important;
    }}
    
    /* Enhance buttons */
    .stButton > button {{
        border-radius: 6px !important;
        font-weight: 500 !important;
        padding: 0.5rem 1rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
        color: {colors['text_primary']} !important;
        background-color: {colors['bg_secondary']} !important;
        border-color: {colors['border']} !important;
    }}
    
    /* Primary buttons */
    .stButton > button[data-baseweb="button"][kind="primary"] {{
        background-color: {colors['accent']} !important;
        color: white !important;
    }}
    
    /* Enhance input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {{
        border-radius: 6px !important;
        padding: 0.75rem !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
        background-color: {colors['bg_secondary']} !important;
        color: {colors['text_primary']} !important;
        border-color: {colors['border']} !important;
    }}
    
    /* Style expanders */
    .streamlit-expanderHeader {{
        font-weight: 500 !important;
        font-size: 1.05rem !important;
        color: {colors['text_primary']} !important;
        background-color: {colors['bg_secondary']} !important;
    }}
    
    /* Style dividers */
    hr {{
        margin-top: 2rem !important;
        margin-bottom: 2rem !important;
        border-color: {colors['border']} !important;
    }}
    
    /* Add shadow to cards/containers */
    div.css-12w0qpk, div.st-emotion-cache-12w0qpk {{
        border-radius: 10px !important;
        box-shadow: 0 2px 10px {colors['card_shadow']} !important;
        background-color: {colors['bg_card']} !important;
        border: 1px solid {colors['card_border']} !important;
    }}
    
    /* Enhance sidebar */
    section[data-testid="stSidebar"] {{
        background-color: {colors['bg_secondary']} !important;
        box-shadow: 0 0 10px {colors['card_shadow']} !important;
    }}
    
    /* Style footer */
    footer {{
        font-size: 0.8rem !important;
        font-weight: 400 !important;
        border-top: 1px solid {colors['border']} !important;
        padding-top: 1rem !important;
        color: {colors['text_secondary']} !important;
    }}
    
    /* Hero section styling */
    .hero-container {{
        padding: 2rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #4f8bf9, #3a7bd5);
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px {colors['card_shadow']};
    }}
    
    .hero-title {{
        font-weight: 700 !important;
        margin-bottom: 1rem;
        font-size: 2.5rem !important;
        color: white !important;
    }}
    
    .hero-subtitle {{
        font-weight: 400 !important;
        margin-bottom: 1.5rem;
        font-size: 1.2rem !important;
        opacity: 0.9;
        color: white !important;
    }}
    
    /* Card styling */
    .card-container {{
        background-color: {colors['bg_card']};
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 5px {colors['card_shadow']};
        margin-bottom: 1.5rem;
        border-left: 4px solid {colors['accent']};
        color: {colors['text_primary']};
    }}
    
    .card-title {{
        font-weight: 600 !important;
        margin-bottom: 0.75rem;
        font-size: 1.25rem !important;
        color: {colors['text_primary']};
    }}
    
    /* Profile section styling */
    .profile-header {{
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
    }}
    
    .profile-avatar {{
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background-color: {colors['accent']};
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 1rem;
        font-size: 2rem;
        color: white;
    }}
    
    .profile-info {{
        flex: 1;
    }}
    
    .profile-name {{
        font-weight: 600 !important;
        margin-bottom: 0.3rem;
        font-size: 1.5rem !important;
        color: {colors['text_primary']};
    }}
    
    .profile-meta {{
        color: {colors['text_secondary']};
        font-size: 0.9rem;
    }}
    
    /* Animation for theme transitions */
    @keyframes themeTransition {{
        0% {{ opacity: 0.8; }}
        100% {{ opacity: 1; }}
    }}
    
    .theme-transition {{
        animation: themeTransition 0.5s ease;
    }}
    
    /* Theme toggle button */
    .theme-toggle {{
        display: flex;
        align-items: center;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        background-color: {colors['button_bg']};
        color: white;
        margin: 0.5rem 0;
        justify-content: center;
        font-weight: 500;
    }}
    
    .theme-toggle i {{
        margin-right: 0.5rem;
    }}
    </style>
    """, unsafe_allow_html=True)

def display_theme_toggle():
    """Display a theme toggle button."""
    current_theme = st.session_state.theme_mode
    icon = "moon" if current_theme == "light" else "sun"
    text = "Dark Mode" if current_theme == "light" else "Light Mode"
    
    toggle_html = f"""
    <div class="theme-toggle" onclick="document.querySelector('.theme-toggle-button').click()">
        <i class="fas fa-{icon}"></i> Switch to {text}
    </div>
    """
    
    st.markdown(toggle_html, unsafe_allow_html=True)
    
    # Hidden button for the actual click handling
    if st.button("Toggle Theme", key="theme-toggle-button", help="Switch between light and dark mode", type="primary"):
        toggle_theme()
        st.rerun()

def display_hero_section(title, subtitle=None, bg_color=None):
    """
    Display a stylized hero section at the top of the page.
    
    Args:
        title: The main title text
        subtitle: Optional subtitle text
        bg_color: Optional background color override
    """
    bg_style = f"background: linear-gradient(135deg, {bg_color}, {bg_color}90);" if bg_color else ""
    
    hero_html = f"""
    <div class="hero-container" style="{bg_style}">
        <h1 class="hero-title">{title}</h1>
    """
    
    if subtitle:
        hero_html += f'<p class="hero-subtitle">{subtitle}</p>'
    
    hero_html += """
    </div>
    """
    
    st.markdown(hero_html, unsafe_allow_html=True)

def display_card(title, content, icon=None, accent_color=None):
    """
    Display content in a stylized card.
    
    Args:
        title: Card title
        content: HTML content for the card body
        icon: Optional icon name from Font Awesome
        accent_color: Optional accent color for the card
    """
    border_style = f"border-left-color: {accent_color};" if accent_color else ""
    
    icon_html = f'<i class="fas fa-{icon}" style="margin-right: 0.5rem;"></i>' if icon else ''
    
    card_html = f"""
    <div class="card-container" style="{border_style}">
        <h3 class="card-title">{icon_html}{title}</h3>
        <div class="card-content">
            {content}
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)

def setup_page(title=None, icon=None, layout="centered"):
    """
    Set up the page with consistent styling and title.
    
    Args:
        title: Page title
        icon: Page icon
        layout: Page layout
    """
    # Set up the page config
    if title:
        st.set_page_config(
            page_title=f"PrePersona - {title}",
            page_icon=icon or "🧠",
            layout=layout
        )
    
    # Apply custom styles
    apply_custom_styles()
    
    # Apply mood-based color scheme if user is logged in
    if "user_name" in st.session_state and st.session_state.user_name:
        set_color_scheme(st.session_state.user_name)

def display_profile_header(user_name=None, avatar_char=None):
    """
    Display a stylized profile header.
    
    Args:
        user_name: The user name to display
        avatar_char: Character(s) to use for the avatar
    """
    user = user_name or st.session_state.get("user_name", "Guest")
    avatar = avatar_char or (user[0].upper() if user and user != "Guest" else "?")
    
    profile_html = f"""
    <div class="profile-header">
        <div class="profile-avatar">
            {avatar}
        </div>
        <div class="profile-info">
            <h2 class="profile-name">{user}</h2>
            <div class="profile-meta">
                PrePersona User
            </div>
        </div>
    </div>
    """
    
    st.markdown(profile_html, unsafe_allow_html=True)

def inject_font_awesome():
    """Inject Font Awesome for icons."""
    st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    """, unsafe_allow_html=True)