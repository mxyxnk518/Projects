import streamlit as st
import os
from utils.data_processor import get_upload_types, process_user_data
from utils.vector_store import initialize_vector_store
from utils.llm_handler import setup_llm_chain
from utils.db import init_db
from utils.ui_styles import setup_page, display_hero_section, display_card, inject_font_awesome
from utils.mood_colors import set_color_scheme, display_mood_selector, get_user_mood

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
    st.warning("Database connection issue: Using a temporary in-memory database for testing. Your data won't be saved permanently.")

# Set up API key configuration in sidebar
st.sidebar.title("API Key Configuration")

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
display_card("Your Personalized Digital Experience", intro_content, icon="brain")

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
    display_card("Quick Start - No Data Upload", quick_start_content, icon="rocket")

with col2:
    digital_clone_content = """
    <ul style="list-style-type: none; padding-left: 0;">
        <li><i class="fas fa-upload" style="color: #4f8bf9; margin-right: 8px;"></i> <strong>Upload your data</strong> - journals, chat logs, notes</li>
        <li><i class="fas fa-brain" style="color: #4f8bf9; margin-right: 8px;"></i> <strong>Train your digital clone</strong> - Learn your patterns</li>
        <li><i class="fas fa-user-circle" style="color: #4f8bf9; margin-right: 8px;"></i> <strong>Get personalized responses</strong> - As if from you</li>
    </ul>
    """
    display_card("Create Your Personalized Digital Clone", digital_clone_content, icon="clone")

# Example Questions
example_content = """
<p style="font-style: italic; color: #555;">
"What would I likely do if offered a remote internship in July?"<br>
"Draft a birthday message I would write to my best friend."<br>
"How would I approach resolving this conflict at work?"
</p>
"""
display_card("Example Questions for Your Digital Clone", example_content, icon="lightbulb")

# App navigation with styled buttons
st.markdown('<h3 style="margin-top: 2rem; margin-bottom: 1.5rem;">Get Started</h3>', unsafe_allow_html=True)

# Create three rows of buttons with icons
nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; border-radius: 10px; background: linear-gradient(135deg, #4f8bf9, #3f7df7); 
                box-shadow: 0 4px 6px rgba(0,0,0,0.1); cursor: pointer; margin-bottom: 1rem;"
         onclick="window.open('pages/chat.py', '_self')">
        <i class="fas fa-comments" style="font-size: 2rem; color: white; margin-bottom: 0.5rem;"></i>
        <h4 style="color: white; margin-bottom: 0.5rem;">Chat with AI</h4>
        <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Start a conversation with the AI assistant</p>
    </div>
    """, unsafe_allow_html=True)

with nav_col2:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; border-radius: 10px; background: linear-gradient(135deg, #26A69A, #1E8C7E); 
                box-shadow: 0 4px 6px rgba(0,0,0,0.1); cursor: pointer; margin-bottom: 1rem;"
         onclick="window.open('pages/upload.py', '_self')">
        <i class="fas fa-upload" style="font-size: 2rem; color: white; margin-bottom: 0.5rem;"></i>
        <h4 style="color: white; margin-bottom: 0.5rem;">Upload Your Data</h4>
        <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Add personal data to train your digital clone</p>
    </div>
    """, unsafe_allow_html=True)

with nav_col3:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; border-radius: 10px; background: linear-gradient(135deg, #7E57C2, #6A48B0); 
                box-shadow: 0 4px 6px rgba(0,0,0,0.1); cursor: pointer; margin-bottom: 1rem;"
         onclick="window.open('pages/query.py', '_self')">
        <i class="fas fa-question-circle" style="font-size: 2rem; color: white; margin-bottom: 0.5rem;"></i>
        <h4 style="color: white; margin-bottom: 0.5rem;">Ask Your Digital Clone</h4>
        <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Get personalized responses based on your data</p>
    </div>
    """, unsafe_allow_html=True)

# Second row
nav_col4, nav_col5, nav_col6 = st.columns(3)

with nav_col4:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; border-radius: 10px; background: linear-gradient(135deg, #F57C00, #E56A00); 
                box-shadow: 0 4px 6px rgba(0,0,0,0.1); cursor: pointer; margin-bottom: 1rem;"
         onclick="window.open('pages/profile.py', '_self')">
        <i class="fas fa-user-circle" style="font-size: 2rem; color: white; margin-bottom: 0.5rem;"></i>
        <h4 style="color: white; margin-bottom: 0.5rem;">Your Profile</h4>
        <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">View and manage your personality profile</p>
    </div>
    """, unsafe_allow_html=True)

with nav_col5:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; border-radius: 10px; background: linear-gradient(135deg, #546E7A, #455A64); 
                box-shadow: 0 4px 6px rgba(0,0,0,0.1); cursor: pointer; margin-bottom: 1rem;"
         onclick="window.open('pages/about.py', '_self')">
        <i class="fas fa-info-circle" style="font-size: 2rem; color: white; margin-bottom: 0.5rem;"></i>
        <h4 style="color: white; margin-bottom: 0.5rem;">About PrePersona</h4>
        <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Learn more about how the technology works</p>
    </div>
    """, unsafe_allow_html=True)

# Status message with better styling
if st.session_state.is_ready:
    st.success(f"Your Digital Clone is ready! You've uploaded {st.session_state.uploaded_files_count} files.")
else:
    st.info("You can chat with the AI right away or upload your data to create a personalized Digital Clone.")

# Enhanced footer
st.markdown("""
<div style="margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid rgba(0,0,0,0.1); text-align: center;">
    <p style="font-size: 1.2rem; font-weight: 500; color: #555;">
        <span style="color: #4f8bf9; font-weight: 600;">PrePersona</span> - Your future self, available today.
    </p>
    <div style="font-size: 0.8rem; color: #777; margin-top: 0.5rem;">
        © 2025 PrePersona AI | Your Digital Clone Technology
    </div>
</div>
""", unsafe_allow_html=True)
