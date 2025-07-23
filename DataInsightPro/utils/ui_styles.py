"""
UI Styling utilities for PrePersona.
This module handles custom CSS and styling for the application.
"""
import streamlit as st
from utils.mood_colors import get_user_mood, set_color_scheme

# Theme settings store - this must be initialized before it's used elsewhere
def init_theme():
    """Initialize theme settings in session state - Force light theme."""
    st.session_state['theme_mode'] = 'light'  # Force light theme always

# DO NOT call init_theme() here - it will be called after set_page_config in setup_page

def toggle_theme():
    """Toggle between dark and light mode."""
    if st.session_state['theme_mode'] == 'light':
        st.session_state['theme_mode'] = 'dark'
    else:
        st.session_state['theme_mode'] = 'light'

def get_theme_colors():
    """Get colors based on current theme."""
    if st.session_state['theme_mode'] == 'dark':
        return {
            'bg_primary': '#0f1117',  # Deeper blue-black background
            'bg_secondary': '#161a24', # Slightly lighter blue-black
            'bg_card': '#1c2333',     # Card background with blue tint
            'text_primary': '#e0e1e6', # Softer white for text
            'text_secondary': '#9ca0b0', # Soft blue-gray for secondary text
            'accent': '#4d7cfe',      # Brighter blue accent color
            'border': 'rgba(255,255,255,0.07)', # Subtle borders
            'user_message_bg': '#263242', # Blue tinted message background
            'ai_message_bg': '#1a1f2c',  # Darker message background
            'button_bg': '#3d5173',    # More saturated button background
            'card_border': '#2c3347',  # Subtle card border
            'card_shadow': 'rgba(0,0,0,0.6)', # Deeper shadow
            'input_bg': '#212736',     # Input fields with blue tint
            'sidebar_bg': '#0b0f18',   # Darker sidebar
            'sidebar_item': '#e0e1e6', # Match primary text color
            'header_bg': '#161a24',    # Match secondary background
            'footer_bg': '#0b0f18'     # Match sidebar background
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
            'card_shadow': 'rgba(0,0,0,0.05)',
            'input_bg': '#ffffff',
            'sidebar_bg': '#f5f5f5',
            'sidebar_item': '#212529',
            'header_bg': '#ffffff',
            'footer_bg': '#f5f5f5'
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
        --input-bg: {colors['input_bg']};
        --sidebar-bg: {colors['sidebar_bg']};
        --sidebar-item: {colors['sidebar_item']};
        --header-bg: {colors['header_bg']};
        --footer-bg: {colors['footer_bg']};
        --button-bg: {colors['button_bg']};
        --card-shadow: {colors['card_shadow']};
        --card-border: {colors['card_border']};
    }}
    
    /* Global overrides for theme */
    .reportview-container .main .block-container,
    .main .block-container,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    .stApp {{
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }}
    
    /* This targets the main content area */
    .st-emotion-cache-z5fcl4,
    .st-emotion-cache-1kyxreq,
    .st-emotion-cache-r421ms,
    .st-emotion-cache-10oheav,
    .st-emotion-cache-ue6h4q,
    [data-testid="stAppViewBlockContainer"],
    .st-emotion-cache-uf99v8,
    .st-emotion-cache-16txtl3,
    .st-emotion-cache-18ni7ap,
    [data-testid="block-container"] {{
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }}
    
    /* Target header and sidebar */
    [data-testid="stSidebar"] > div:first-child,
    .st-emotion-cache-1cypcdb,
    .st-emotion-cache-1wrcr25,
    div[class*="st-emotion-cache"] > div {{
        background-color: var(--sidebar-bg) !important;
    }}
    
    /* Target Streamlit's base elements */
    html, body {{
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }}
    
    /* Main heading styles */
    h1, h2, h3, h4, h5, h6 {{
        font-weight: 600 !important;
        letter-spacing: -0.3px;
        color: var(--text-primary);
    }}
    
    /* Paragraph text */
    p, div, span {{
        color: var(--text-primary);
    }}
    
    /* Navigation menu styling */
    .css-1q8dd3e, .css-wjbhl0, .st-emotion-cache-1q8dd3e, .st-emotion-cache-wjbhl0 {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        background-color: var(--sidebar-bg);
    }}
    
    /* Capitalize navigation menu items */
    section[data-testid="stSidebar"] .css-pkbazv, 
    section[data-testid="stSidebar"] .st-emotion-cache-pkbazv,
    section[data-testid="stSidebar"] .st-emotion-cache-16txtl3,
    section[data-testid="stSidebar"] .css-16txtl3 {{
        text-transform: capitalize !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        color: var(--sidebar-item) !important;
    }}
    
    /* Enhance buttons */
    .stButton > button {{
        border-radius: 6px !important;
        font-weight: 500 !important;
        padding: 0.5rem 1rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
        color: var(--text-primary) !important;
        background-color: var(--bg-secondary) !important;
        border-color: var(--border) !important;
    }}
    
    /* Primary buttons */
    .stButton > button[data-baseweb="button"][kind="primary"] {{
        background-color: var(--accent) !important;
        color: white !important;
    }}
    
    /* Enhance input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {{
        border-radius: 6px !important;
        padding: 0.75rem !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
        background-color: var(--input-bg) !important;
        color: var(--text-primary) !important;
        border-color: var(--border) !important;
    }}
    
    /* Style expanders */
    .streamlit-expanderHeader {{
        font-weight: 500 !important;
        font-size: 1.05rem !important;
        color: var(--text-primary) !important;
        background-color: var(--bg-secondary) !important;
    }}
    
    /* Style dividers */
    hr {{
        margin-top: 2rem !important;
        margin-bottom: 2rem !important;
        border-color: var(--border) !important;
    }}
    
    /* Add shadow to cards/containers */
    div.css-12w0qpk, div.st-emotion-cache-12w0qpk {{
        border-radius: 10px !important;
        box-shadow: 0 2px 10px var(--card-shadow) !important;
        background-color: var(--bg-card) !important;
        border: 1px solid var(--card-border) !important;
    }}
    
    /* Enhance sidebar */
    section[data-testid="stSidebar"], 
    [data-testid="stSidebar"] > div:first-child {{
        background-color: var(--sidebar-bg) !important;
        box-shadow: 0 0 10px var(--card-shadow) !important;
    }}
    
    [data-testid="stSidebar"] .st-emotion-cache-16txtl3 {{
        color: var(--sidebar-item) !important;
    }}
    
    /* Apply theme to inputs */
    .stTextInput input, .stTextArea textarea, .stSelectbox, [data-baseweb="select"] {{
        background-color: var(--input-bg) !important;
        color: var(--text-primary) !important;
        border-color: var(--border) !important;
    }}
    
    /* Style dropdowns */
    [data-baseweb="select"] > div {{
        background-color: var(--input-bg) !important;
        color: var(--text-primary) !important;
    }}
    
    /* Style sliders */
    .stSlider [data-baseweb="slider"] {{
        background-color: var(--bg-secondary) !important;
    }}
    
    /* Style checkboxes */
    .stCheckbox label {{
        color: var(--text-primary) !important;
    }}
    
    /* Style radio buttons */
    .stRadio label {{
        color: var(--text-primary) !important;
    }}
    
    /* Style data frames */
    .dataframe {{
        color: var(--text-primary) !important;
        background-color: var(--bg-card) !important;
    }}
    
    .stDataFrame div[data-testid="stTable"] {{
        color: var(--text-primary) !important;
        background-color: var(--bg-card) !important;
    }}
    
    /* Fix for markdown background */
    div[data-testid="stMarkdownContainer"] {{
        color: var(--text-primary) !important;
    }}
    
    /* Style footer */
    footer {{
        font-size: 0.8rem !important;
        font-weight: 400 !important;
        border-top: 1px solid var(--border) !important;
        padding-top: 1rem !important;
        color: var(--text-secondary) !important;
        background-color: var(--footer-bg) !important;
    }}
    
    /* Hero section styling */
    .hero-container {{
        padding: 2rem;
        border-radius: 10px;
        background: linear-gradient(135deg, var(--accent), #3a7bd5);
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px var(--card-shadow);
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
        background-color: var(--bg-card);
        border-radius: 12px;
        padding: 1.75rem;
        box-shadow: 0 8px 16px var(--card-shadow);
        margin-bottom: 1.75rem;
        border-left: 4px solid var(--accent);
        color: var(--text-primary);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .card-container::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--accent), transparent);
        opacity: 0.7;
    }}
    
    .card-container:hover {{
        transform: translateY(-2px);
        box-shadow: 0 12px 20px var(--card-shadow);
    }}
    
    .card-title {{
        font-weight: 600 !important;
        margin-bottom: 1rem;
        font-size: 1.35rem !important;
        color: var(--text-primary);
        display: flex;
        align-items: center;
        letter-spacing: -0.3px;
    }}
    
    .card-title i {{
        margin-right: 0.75rem;
        color: var(--accent);
        font-size: 1.2em;
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
        background-color: var(--accent);
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
        color: var(--text-primary);
    }}
    
    .profile-meta {{
        color: var(--text-secondary);
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
        background-color: var(--button-bg);
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
    current_theme = st.session_state['theme_mode']
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
    
    # Remove any closing div tags that might be in the content to prevent them from showing
    cleaned_content = content.replace("</div>", "")
    
    card_html = f"""
    <div class="card-container" style="{border_style}">
        <h3 class="card-title">{icon_html}{title}</h3>
        {cleaned_content}
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
    # Set up the page config first (must be the first streamlit command)
    if title:
        st.set_page_config(
            page_title=f"PrePersona - {title}",
            page_icon=icon or "🧠",
            layout=layout
        )
    
    # Initialize theme settings right after page config
    init_theme()
    
    # Apply custom styles
    apply_custom_styles()
    
    # Apply mood-based color scheme if user is logged in
    if "user_name" in st.session_state and st.session_state.get("user_name"):
        set_color_scheme(st.session_state.get("user_name"))

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