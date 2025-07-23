import streamlit as st
from utils.dark_mode_styles import apply_dark_mode, create_navigation_sidebar

st.set_page_config(
    page_title="PrePersona - HOME",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply dark mode styling
apply_dark_mode()

# Main app title and description
st.title("PrePersona - Your Digital Clone")
st.subheader("An AI that learns how you think, talk, and decide")

# App introduction
st.markdown("""
**PrePersona** is an AI-powered digital clone that learns how you think, communicate, and make decisions.
You can use the AI immediately OR upload your personal data to create a personalized digital version of you 
that can predict how you would respond to new situations.

### Two Ways to Use PrePersona:

#### 1. Quick Start - No Data Upload Required:
- **Chat with AI** - Start chatting immediately without uploading any data
- **Get general assistance** - Ask questions, get help, explore the capabilities

#### 2. Create Your Personalized Digital Clone:
- **Upload your data** - journals, chat logs, notes, calendar entries
- **Train your digital clone** - PrePersona learns your communication style and decision patterns
- **Ask personalized questions** - Find out how you would likely respond to new situations

### Example Questions for Your Digital Clone:
- "What would I likely do if offered a remote internship in July?"
- "Draft a birthday message I would write to my best friend."
- "How would I approach resolving this conflict at work?"
""")

# App navigation
st.markdown("### Get Started")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Chat with AI", use_container_width=True):
        st.switch_page("pages/chat.py")

with col2:
    if st.button("Upload Your Data", use_container_width=True):
        st.switch_page("pages/upload.py")

with col3:
    if st.button("Ask Your Digital Clone", use_container_width=True):
        st.switch_page("pages/query.py")

with col4:
    if st.button("Your Profile", use_container_width=True):
        st.switch_page("pages/profile.py")

# Status message at the bottom
if 'is_ready' in st.session_state and st.session_state.is_ready:
    st.success(f"Your Digital Clone is ready! You've uploaded {st.session_state.uploaded_files_count} files.")
else:
    st.info("You can chat with the AI right away or upload your data to create a personalized Digital Clone.")

# Footer
st.markdown("---")
st.markdown("**PrePersona** - Your future self, available today.")
