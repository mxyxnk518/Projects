import streamlit as st
import os
from utils.data_processor import get_upload_types, process_user_data
from utils.vector_store import initialize_vector_store
from utils.llm_handler import setup_llm_chain
from utils.db import init_db
from utils.ui_styles import setup_page, display_hero_section, inject_font_awesome
from utils.mood_colors import set_color_scheme, display_mood_selector, get_user_mood
from utils.card_display import simple_card

# Initialize database tables
db_initialized = init_db()

# Set up page with enhanced styling
setup_page(
    title="Your Digital Clone",
    icon="👤",
    layout="wide"
)

# Inject Font Awesome for icons
inject_font_awesome()

# Show database status
if not db_initialized:
    st.warning("Database connection issue. Your data might not be saved properly.")
else:
    # Set a default user if none exists
    if 'user_name' not in st.session_state or not st.session_state.user_name:
        from utils.db import get_or_create_user
        st.session_state.user_name = "DefaultUser"
        st.session_state.user_id = get_or_create_user("DefaultUser")

# Set up API key configuration in sidebar
st.sidebar.title("API KEY CONFIGURATION")

# Groq API key
if "GROQ_API_KEY" not in os.environ:
    groq_api_key = st.sidebar.text_input("Groq API Key", type="password", 
                                         help="Required for using Groq models")
    if groq_api_key:
        os.environ["GROQ_API_KEY"] = groq_api_key

# Initialize session state variables if they don't exist
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'llm_chain' not in st.session_state:
    st.session_state.llm_chain = None
if 'uploaded_files_count' not in st.session_state:
    st.session_state.uploaded_files_count = 0
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'processed_data_summary' not in st.session_state:
    st.session_state.processed_data_summary = {}
if 'is_ready' not in st.session_state:
    st.session_state.is_ready = False
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = "llama3-70b-8192"  # Default to Llama3 model from Groq

# Apply mood-based color scheme if user is logged in
if "user_name" in st.session_state and st.session_state.user_name:
    user_mood = get_user_mood(st.session_state.user_name)
    set_color_scheme(st.session_state.user_name, user_mood)
    # Add mood selector in sidebar
    with st.sidebar:
        st.markdown("### Mood Theme")
        display_mood_selector()

# Dark mode is now default and fixed
# Theme toggle removed as requested

# Hero Section
display_hero_section(
    title="PrePersona - Your Digital Clone",
    subtitle="An AI that learns how you think, talk, and decide"
)

# App introduction in a styled card
intro_content = """
<p style="font-size: 1.1rem; line-height: 1.6;">
PrePersona is an AI-powered digital clone that learns how you think, communicate, and make decisions.
You can use the AI immediately OR upload your personal data to create a personalized digital version of you 
that can predict how you would respond to new situations.
</p>
"""
simple_card("Your Personalized Digital Experience", intro_content, icon="brain")

# Two-column layout for features
col1, col2 = st.columns(2)

with col1:
    quick_start_content = """
<ul style="list-style-type: none; padding-left: 0;">
    <li><i class="fas fa-comments" style="color: #4f8bf9; margin-right: 8px;"></i> <strong>Chat with AI</strong> - Start chatting immediately</li>
    <li><i class="fas fa-question-circle" style="color: #4f8bf9; margin-right: 8px;"></i> <strong>Get assistance</strong> - Ask questions, explore capabilities</li>
    <li><i class="fas fa-bolt" style="color: #4f8bf9; margin-right: 8px;"></i> <strong>No setup required</strong> - Jump right in</li>
</ul>
"""
    simple_card("Quick Start - No Data Upload", quick_start_content, icon="rocket")

with col2:
    digital_clone_content = """
<ul style="list-style-type: none; padding-left: 0;">
    <li><i class="fas fa-upload" style="color: #4f8bf9; margin-right: 8px;"></i> <strong>Upload your data</strong> - journals, chat logs, notes</li>
    <li><i class="fas fa-brain" style="color: #4f8bf9; margin-right: 8px;"></i> <strong>Train your digital clone</strong> - Learn your patterns</li>
    <li><i class="fas fa-user-circle" style="color: #4f8bf9; margin-right: 8px;"></i> <strong>Get personalized responses</strong> - As if from you</li>
</ul>
"""
    simple_card("Create Your Personalized Digital Clone", digital_clone_content, icon="clone")

# Example Questions
example_content = """
<p style="font-style: italic; color: var(--text-secondary); border-left: 3px solid var(--accent); padding-left: 15px; margin: 10px 0;">
"What would I likely do if offered a remote internship in July?"<br>
"Draft a birthday message I would write to my best friend."<br>
"How would I approach resolving this conflict at work?"
</p>
"""
simple_card("Example Questions for Your Digital Clone", example_content, icon="lightbulb")

# App navigation with styled buttons
st.markdown('<h3 style="margin-top: 2rem; margin-bottom: 1.5rem;">Get Started</h3>', unsafe_allow_html=True)

# Create three rows of buttons with icons
nav_col1, nav_col2, nav_col3 = st.columns(3)

# Define interactive navigation button styles with hover effects
st.markdown("""
<style>
/* Base navigation button styles */
.nav-button {
    text-align: center;
    padding: 1.2rem;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    cursor: pointer;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

/* Hover effect for all nav buttons */
.nav-button:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 10px 20px rgba(0,0,0,0.3);
}

/* Pulse animation for icons */
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.15); }
    100% { transform: scale(1); }
}

/* Icon base styles */
.nav-button i {
    font-size: 2.2rem;
    color: white;
    margin-bottom: 0.7rem;
    display: inline-block;
    transition: transform 0.3s ease;
}

/* Icon hover animation */
.nav-button:hover i {
    animation: pulse 1s infinite ease-in-out;
}

/* Title styles */
.nav-button h4 {
    color: white;
    margin-bottom: 0.5rem;
    transition: transform 0.3s ease, color 0.3s ease;
}

/* Description text styles */
.nav-button p {
    color: rgba(255,255,255,0.9);
    font-size: 0.9rem;
    transition: opacity 0.3s ease;
}

/* Enhance text on hover */
.nav-button:hover h4 {
    transform: scale(1.05);
}

.nav-button:hover p {
    opacity: 1;
}

/* Glow effect on hover */
.nav-button::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 70%);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.nav-button:hover::after {
    opacity: 1;
}

/* Specific color themes for each button */
.nav-blue {
    background: linear-gradient(135deg, #4f8bf9, #3370e8);
}
.nav-blue:hover {
    background: linear-gradient(135deg, #5a94fd, #4a81f1);
}

.nav-green {
    background: linear-gradient(135deg, #26A69A, #1E8C7E);
}
.nav-green:hover {
    background: linear-gradient(135deg, #2dbeaf, #25a193);
}

.nav-purple {
    background: linear-gradient(135deg, #7E57C2, #6A48B0);
}
.nav-purple:hover {
    background: linear-gradient(135deg, #8c67cd, #7955c4);
}
</style>
""", unsafe_allow_html=True)

with nav_col1:
    st.markdown("""
    <div class="nav-button nav-blue" onclick="window.open('pages/chat.py', '_self')">
        <i class="fas fa-comments"></i>
        <h4>Chat with AI</h4>
        <p>Start a conversation with the AI assistant</p>
    </div>
    """, unsafe_allow_html=True)

with nav_col2:
    st.markdown("""
    <div class="nav-button nav-green" onclick="window.open('pages/upload.py', '_self')">
        <i class="fas fa-upload"></i>
        <h4>Upload Your Data</h4>
        <p>Add personal data to train your digital clone</p>
    </div>
    """, unsafe_allow_html=True)

with nav_col3:
    st.markdown("""
    <div class="nav-button nav-purple" onclick="window.open('pages/query.py', '_self')">
        <i class="fas fa-question-circle"></i>
        <h4>Ask Your Digital Clone</h4>
        <p>Get personalized responses based on your data</p>
    </div>
    """, unsafe_allow_html=True)

# Second row
nav_col4, nav_col5, nav_col6 = st.columns(3)

# Add more color themes for the second row
st.markdown("""
<style>
.nav-orange {
    background: linear-gradient(135deg, #F57C00, #E56A00);
}
.nav-orange:hover {
    background: linear-gradient(135deg, #ff8c1a, #f57c00);
}

.nav-gray {
    background: linear-gradient(135deg, #546E7A, #455A64);
}
.nav-gray:hover {
    background: linear-gradient(135deg, #607d8b, #546e7a);
}

.nav-magenta {
    background: linear-gradient(135deg, #9C27B0, #7B1FA2);
}
.nav-magenta:hover {
    background: linear-gradient(135deg, #ab47bc, #9c27b0);
}
</style>
""", unsafe_allow_html=True)

with nav_col4:
    st.markdown("""
    <div class="nav-button nav-orange" onclick="window.open('pages/profile.py', '_self')">
        <i class="fas fa-user-circle"></i>
        <h4>Your Profile</h4>
        <p>View and manage your personality profile</p>
    </div>
    """, unsafe_allow_html=True)

with nav_col5:
    st.markdown("""
    <div class="nav-button nav-gray" onclick="window.open('pages/about.py', '_self')">
        <i class="fas fa-info-circle"></i>
        <h4>About PrePersona</h4>
        <p>Learn more about how the technology works</p>
    </div>
    """, unsafe_allow_html=True)

with nav_col6:
    st.markdown("""
    <div class="nav-button nav-magenta" onclick="window.open('pages/debug.py', '_self')">
        <i class="fas fa-database"></i>
        <h4>Database Debug</h4>
        <p>View and explore stored data</p>
    </div>
    """, unsafe_allow_html=True)

# Status message with better styling
if st.session_state.is_ready:
    st.success(f"Your Digital Clone is ready! You've uploaded {st.session_state.uploaded_files_count} files.")
else:
    st.info("You can chat with the AI right away or upload your data to create a personalized Digital Clone.")

# Enhanced footer with micro-interaction animations
st.markdown("""
<style>
/* Enhanced footer styling */
.interactive-footer {
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
    text-align: center;
    position: relative;
}

/* Gradient line effect */
.interactive-footer::before {
    content: '';
    position: absolute;
    top: -1px;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 3px;
    background: linear-gradient(90deg, #4d7cfe, #9c27b0);
    transition: width 0.8s ease;
}

/* Expand gradient line on hover */
.interactive-footer:hover::before {
    width: 100%;
}

/* Main slogan styling */
.footer-slogan {
    font-size: 1.2rem; 
    font-weight: 500; 
    color: var(--text-primary);
    margin-bottom: 0.6rem;
    transition: transform 0.3s ease;
}

/* Slogan slight float on hover */
.interactive-footer:hover .footer-slogan {
    transform: translateY(-3px);
}

/* Brand name styling with glow effect */
.brand-name {
    color: var(--accent); 
    font-weight: 600;
    position: relative;
    transition: color 0.3s ease;
}

/* Brand name color shift on hover */
.interactive-footer:hover .brand-name {
    color: #5d8fff;
}

/* Subtle glow effect for brand name */
.brand-name::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    box-shadow: 0 0 8px var(--accent);
    opacity: 0;
    transition: opacity 0.5s ease;
    border-radius: 4px;
    z-index: -1;
}

/* Show glow on hover */
.interactive-footer:hover .brand-name::after {
    opacity: 0.6;
}

/* Copyright text styling */
.copyright-text {
    font-size: 0.8rem; 
    color: var(--text-secondary); 
    margin-top: 0.5rem;
    opacity: 0.8;
    transition: opacity 0.3s ease;
}

/* Brighten copyright text on hover */
.interactive-footer:hover .copyright-text {
    opacity: 1;
}
</style>

<div class="interactive-footer">
    <p class="footer-slogan">
        <span class="brand-name">PrePersona</span> - Your future self, available today.
    </p>
    <div class="copyright-text">
        © 2025 PrePersona AI | Your Digital Clone Technology
    </div>
</div>
""", unsafe_allow_html=True)
