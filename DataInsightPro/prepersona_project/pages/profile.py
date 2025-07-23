import streamlit as st
from utils.personality import get_user_personality_profile
from utils.llm_handler import get_groq_client, get_selected_model
from utils.db import get_or_create_user, get_conversations

st.set_page_config(
    page_title="PrePersona - Personality Profile",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Model selection
selected_model = get_selected_model()

# Initialize Groq client
groq_client = get_groq_client()

# If no client is available, show a warning
if not groq_client:
    st.warning("Groq API key not found. Please provide your Groq API key to use the app.")

# Sidebar with navigation
st.sidebar.title("Navigation")
if st.sidebar.button("Home"):
    st.switch_page("pages/home.py")
if st.sidebar.button("Upload Your Data"):
    st.switch_page("pages/upload.py")
if st.sidebar.button("Ask Your Digital Clone"):
    st.switch_page("pages/query.py")
if st.sidebar.button("About"):
    st.switch_page("pages/about.py")

# Model selection in sidebar
st.sidebar.title("AI Model Settings")
model_options = ["llama3-70b-8192", "mixtral-8x7b-32768", "gemma-7b-it"]
model_index = model_options.index(st.session_state.get("selected_model", "llama3-70b-8192")) if st.session_state.get("selected_model") in model_options else 0
selected_model = st.sidebar.selectbox(
    "Choose Groq Model",
    options=model_options,
    index=model_index,
    help="Select which Groq model powers your digital clone."
)

# Update the model selection in session state
if st.session_state.get("selected_model") != selected_model:
    st.session_state.selected_model = selected_model
    st.rerun()

# Main content
st.title("Your Personality Profile")

# Check if digital clone is ready
if not st.session_state.get("is_ready", False):
    st.warning("Your digital clone is not ready yet. Please upload your data first.")
    if st.button("Go to Upload Page"):
        st.switch_page("pages/upload.py")
else:
    user_name = st.session_state.get("user_name")
    
    # Get personality profile
    profile = get_user_personality_profile(user_name)
    
    if not profile:
        st.info("No personality profile found. This will be generated when you upload data.")
    else:
        st.markdown(f"""
        # {user_name}'s Personality Profile
        
        This profile is automatically generated from your data and used to make your digital clone's responses more authentic.
        The more data you provide, the more accurate this profile will become.
        """)
        
        # Core profile information in cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Decision Style")
            decision_style = profile.get('decision_style', 'Unknown')
            st.info(f"**{decision_style.title()}**")
            
            if decision_style == "analytical":
                st.markdown("You tend to make decisions based on logic and careful consideration of facts.")
            elif decision_style == "intuitive":
                st.markdown("You often rely on gut feelings and intuition when making decisions.")
            elif decision_style == "deliberate":
                st.markdown("You take your time with decisions, carefully weighing all options.")
            elif decision_style == "spontaneous":
                st.markdown("You're comfortable making quick decisions and adapting on the fly.")
        
        with col2:
            st.markdown("### Emotional Baseline")
            emotional_baseline = profile.get('emotional_baseline', 'Neutral')
            st.info(f"**{emotional_baseline.title()}**")
            
            if emotional_baseline == "optimistic":
                st.markdown("You generally maintain a positive outlook on situations.")
            elif emotional_baseline == "cautious":
                st.markdown("You tend to carefully consider potential risks and downsides.")
            elif emotional_baseline == "neutral":
                st.markdown("You maintain a balanced emotional approach to situations.")
            elif emotional_baseline == "anxious":
                st.markdown("You sometimes worry about outcomes and consider safeguards.")
        
        with col3:
            st.markdown("### Communication Style")
            language_tone = profile.get('language_tone', 'Casual')
            st.info(f"**{language_tone.title()}**")
            
            if language_tone == "formal":
                st.markdown("Your communication tends to be structured and proper.")
            elif language_tone == "casual":
                st.markdown("You communicate in a relaxed, conversational manner.")
            elif language_tone == "technical":
                st.markdown("You often use precise, specialized terminology.")
            elif language_tone == "poetic":
                st.markdown("Your expression is creative and uses vivid imagery.")
        
        # Core values
        st.markdown("### Core Values")
        core_values = profile.get('core_values', [])
        if core_values:
            values_cols = st.columns(len(core_values))
            for i, value in enumerate(core_values):
                with values_cols[i]:
                    st.success(f"**{value.title()}**")
        else:
            st.info("No core values identified yet.")
        
        # Behavior patterns
        st.markdown("### Behavior Patterns")
        behavior_patterns = profile.get('behavior_patterns', {})
        
        if behavior_patterns:
            col1, col2 = st.columns(2)
            
            with col1:
                conflict_style = behavior_patterns.get('conflict_handling', 'Unknown')
                st.markdown(f"**Conflict Handling:** {conflict_style.title()}")
            
            with col2:
                comm_pref = behavior_patterns.get('communication_preference', 'Unknown')
                st.markdown(f"**Communication Preference:** {comm_pref.title()}")
        else:
            st.info("Behavior patterns not yet identified.")
        
        # Preferences section
        st.markdown("### Preferences")
        preferences = profile.get('preferences', {})
        general_prefs = preferences.get('general', [])
        
        if general_prefs:
            st.write(", ".join(general_prefs))
        else:
            st.info("Specific preferences not yet identified.")
        
        # Last updated
        st.caption(f"Profile last updated: {profile.get('updated_at', 'Unknown')}")
    
    # Recent conversations
    st.markdown("## Recent Conversations")
    
    try:
        user_id = get_or_create_user(user_name)
        conversations = get_conversations(user_id, limit=5)
        
        if conversations:
            for question, response, timestamp in conversations:
                with st.expander(f"Q: {question[:50]}{'...' if len(question) > 50 else ''} ({timestamp.strftime('%Y-%m-%d %H:%M')})"):
                    st.markdown(f"**Question:** {question}")
                    st.markdown(f"**Response:** {response}")
        else:
            st.info("No conversation history found.")
    except Exception as e:
        st.warning(f"Could not load conversation history: {str(e)}")

# Footer
st.markdown("---")
st.markdown("**PrePersona** - Your future self, available today.")