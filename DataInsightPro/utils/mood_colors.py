"""
Mood-based color scheme utility for PrePersona.
This module handles the detection of user mood from text and conversation history,
and provides appropriate color schemes for the UI.
"""
import streamlit as st
import json
from typing import Dict, Tuple, List, Optional

# Define mood categories and their associated color schemes
# Format: (primary, secondary, background, text)
MOOD_COLORS = {
    "happy": ("#1E88E5", "#64B5F6", "#E3F2FD", "#212121"),  # Blue tones
    "excited": ("#F57C00", "#FFB74D", "#FFF3E0", "#212121"),  # Orange tones
    "calm": ("#26A69A", "#80CBC4", "#E0F2F1", "#212121"),  # Teal tones
    "thoughtful": ("#7E57C2", "#B39DDB", "#EDE7F6", "#212121"),  # Purple tones
    "sad": ("#78909C", "#B0BEC5", "#ECEFF1", "#212121"),  # Blue-grey tones
    "anxious": ("#FFD600", "#FFF176", "#FFFDE7", "#212121"),  # Yellow tones
    "neutral": ("#546E7A", "#90A4AE", "#ECEFF1", "#212121")  # Default blue-grey
}

# Words and phrases associated with different moods for basic detection
MOOD_KEYWORDS = {
    "happy": ["happy", "joy", "pleased", "delighted", "content", "satisfied", "cheerful", "glad"],
    "excited": ["excited", "thrilled", "enthusiastic", "eager", "energized", "animated", "pumped"],
    "calm": ["calm", "peaceful", "relaxed", "tranquil", "serene", "composed", "steady"],
    "thoughtful": ["thoughtful", "reflective", "contemplative", "pensive", "philosophical", "analytical"],
    "sad": ["sad", "unhappy", "disappointed", "down", "blue", "melancholy", "somber"],
    "anxious": ["anxious", "worried", "nervous", "uneasy", "apprehensive", "concerned", "stressed"],
    "neutral": ["neutral", "balanced", "moderate", "impartial", "even", "standard"]
}

def detect_mood_from_text(text: str) -> str:
    """
    Detect mood from text using keyword matching.
    This is a basic implementation that can be enhanced with AI later.
    
    Args:
        text: The text to analyze
        
    Returns:
        The detected mood category
    """
    # Convert to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # Count occurrences of mood keywords
    mood_scores = {mood: 0 for mood in MOOD_KEYWORDS.keys()}
    
    for mood, keywords in MOOD_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                mood_scores[mood] += 1
    
    # Find mood with highest score
    max_score = 0
    detected_mood = "neutral"
    
    for mood, score in mood_scores.items():
        if score > max_score:
            max_score = score
            detected_mood = mood
    
    return detected_mood

def detect_mood_from_profile(user_name: str) -> str:
    """
    Detect mood from the user's personality profile.
    
    Args:
        user_name: The name of the user
        
    Returns:
        The detected mood category
    """
    # Get emotional baseline from personality profile
    try:
        from utils.personality import get_user_personality_profile
        profile = get_user_personality_profile(user_name)
        
        if profile and 'emotional_baseline' in profile:
            emotional_baseline = profile['emotional_baseline'].lower()
            
            # Map emotional baseline to mood categories
            if emotional_baseline in ["positive", "optimistic", "cheerful"]:
                return "happy"
            elif emotional_baseline in ["energetic", "passionate", "enthusiastic"]:
                return "excited"
            elif emotional_baseline in ["calm", "relaxed", "peaceful"]:
                return "calm"
            elif emotional_baseline in ["analytical", "reflective", "thoughtful"]:
                return "thoughtful"
            elif emotional_baseline in ["melancholic", "sad", "gloomy"]:
                return "sad"
            elif emotional_baseline in ["worried", "anxious", "nervous"]:
                return "anxious"
            else:
                return "neutral"
    except Exception as e:
        st.warning(f"Could not detect mood from profile: {str(e)}")
    
    return "neutral"

def detect_mood_from_conversations(user_name: str, limit: int = 5) -> str:
    """
    Detect mood from recent conversations.
    
    Args:
        user_name: The name of the user
        limit: Number of recent conversations to analyze
        
    Returns:
        The detected mood category
    """
    try:
        from utils.db import get_or_create_user, get_conversations
        
        user_id = get_or_create_user(user_name)
        if not user_id:
            return "neutral"
            
        conversations = get_conversations(user_id, limit=limit)
        if not conversations:
            return "neutral"
        
        # Concatenate all conversation text
        all_text = " ".join([q + " " + r for q, r, _ in conversations])
        
        # Detect mood from text
        return detect_mood_from_text(all_text)
    
    except Exception as e:
        st.warning(f"Could not detect mood from conversations: {str(e)}")
        return "neutral"

def get_user_mood(user_name: str = None) -> str:
    """
    Get the current mood for a user, using multiple detection methods.
    
    Args:
        user_name: The name of the user
        
    Returns:
        The detected mood category
    """
    # Skip if no user name
    if not user_name:
        return "neutral"
    
    # Try to get from session state first (for consistency)
    if "user_mood" in st.session_state:
        return st.session_state.user_mood
    
    # Use profile-based detection as primary method
    profile_mood = detect_mood_from_profile(user_name)
    
    # Use conversation-based detection as backup
    conversation_mood = detect_mood_from_conversations(user_name)
    
    # Determine final mood (prioritize profile mood if available)
    if profile_mood != "neutral":
        final_mood = profile_mood
    else:
        final_mood = conversation_mood
    
    # Store in session state for consistency
    st.session_state.user_mood = final_mood
    
    return final_mood

def set_color_scheme(user_name: str = None, mood: str = None):
    """
    Set the app's color scheme based on user mood.
    
    Args:
        user_name: The name of the user
        mood: Override the mood detection with a specific mood
    """
    # Get mood if not provided
    if not mood:
        mood = get_user_mood(user_name)
    
    # Get color scheme for the mood
    colors = MOOD_COLORS.get(mood, MOOD_COLORS["neutral"])
    primary, secondary, background, text = colors
    
    # Apply the color scheme using Streamlit config options
    st.markdown(f"""
    <style>
    .stApp {{
        background-color: {background};
    }}
    .stButton>button, .stDownloadButton>button {{
        background-color: {primary};
        color: white;
    }}
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {{
        border-color: {secondary};
    }}
    .stSelectbox>div>div>div {{
        border-color: {secondary};
    }}
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {{
        color: {primary};
    }}
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: auto;
        white-space: pre-wrap;
        background-color: {background};
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        border-right: 1px solid {secondary};
        border-left: 1px solid {secondary};
        border-top: 1px solid {secondary};
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {secondary};
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Store current mood in session state
    st.session_state.user_mood = mood

def get_mood_emoji(mood: str) -> str:
    """
    Get an emoji representing the given mood.
    
    Args:
        mood: The mood category
        
    Returns:
        An appropriate emoji string
    """
    mood_emojis = {
        "happy": "😊",
        "excited": "🎉",
        "calm": "😌",
        "thoughtful": "🤔",
        "sad": "😔",
        "anxious": "😰",
        "neutral": "😐"
    }
    
    return mood_emojis.get(mood, "😐")

def display_mood_selector():
    """
    Display a mood selector widget for manual mood selection.
    """
    # Only show if user is logged in
    if "user_name" not in st.session_state or not st.session_state.user_name:
        return
    
    user_name = st.session_state.user_name
    current_mood = get_user_mood(user_name)
    
    # Create columns for mood display and selector
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.write(f"Mood: {get_mood_emoji(current_mood)}")
    
    with col2:
        moods = list(MOOD_COLORS.keys())
        selected_mood = st.selectbox(
            "Change mood theme",
            moods,
            index=moods.index(current_mood),
            key="mood_selector",
            label_visibility="collapsed"
        )
        
        if selected_mood != current_mood:
            st.session_state.user_mood = selected_mood
            set_color_scheme(mood=selected_mood)
            st.rerun()