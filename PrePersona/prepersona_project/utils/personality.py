import os
import streamlit as st
from utils.db import update_personality_profile, get_personality_profile
from utils.llm_handler import get_groq_client, get_selected_model
import re
from datetime import datetime

def extract_personality_profile(user_id, processed_data):
    """
    Extract a personality profile from the user's processed data.
    
    Args:
        user_id: The ID of the user
        processed_data: List of dictionaries with 'text' and 'metadata' fields
    """
    # Get all text combined
    all_text = "\n\n".join([item["text"] for item in processed_data])
    
    # Initialize Groq client
    selected_model = get_selected_model()
    groq_client = get_groq_client()
    
    if not groq_client:
        st.warning("No Groq client available for personality extraction. Using basic profile.")
        # Create a basic profile
        profile_data = {
            "decision_style": "unknown",
            "emotional_baseline": "neutral",
            "language_tone": "casual",
            "core_values": ["unknown"],
            "behavior_patterns": {
                "conflict_handling": "unknown",
                "communication_preference": "unknown"
            },
            "preferences": {
                "general": []
            }
        }
    else:
        with st.spinner("Analyzing your data to extract personality profile..."):
            try:
                profile_data = extract_profile_with_ai(all_text, groq_client, selected_model)
                st.success("Personality profile created based on your data")
            except Exception as e:
                st.warning(f"Could not extract personality profile with AI: {str(e)}")
                # Use basic extraction as fallback
                profile_data = extract_basic_profile(all_text)
    
    # Save the profile to the database
    update_personality_profile(user_id, profile_data)

def extract_profile_with_ai(text, client, model_name):
    """
    Extract personality profile using Groq AI.
    
    Args:
        text: Text to analyze
        client: Groq client 
        model_name: Name of the Groq model
        
    Returns:
        Dictionary with personality profile data
    """
    # Sample size to avoid token limits
    max_chars = 10000  # Adjust based on model limits
    text_sample = text[:max_chars] if len(text) > max_chars else text
    
    # Profile extraction prompt
    prompt = f"""
    Analyze the following text which contains writings from a person. 
    Extract their personality traits, values, and communication style.
    
    Text to analyze:
    {text_sample}
    
    Based on this text, create a personality profile with the following attributes:
    
    1. Decision making style (analytical, intuitive, deliberate, spontaneous, etc.)
    2. Emotional baseline (optimistic, cautious, neutral, anxious, etc.)
    3. Language tone (formal, casual, technical, poetic, etc.)
    4. Core values (list 3-5 values that seem important to this person)
    5. Behavior patterns (how they handle conflict, communication preferences)
    6. General preferences (things they like/dislike based on the text)
    
    Return the profile as a structured JSON object with these fields:
    decision_style, emotional_baseline, language_tone, core_values (array), 
    behavior_patterns (object), preferences (object).
    
    Respond only with the JSON, no explanations or other text.
    """
    
    # Use Groq to extract profile
    try:
        response = client.chat.completions.create(
            model=model_name,  # Use the selected Groq model
            messages=[
                {"role": "system", "content": "You are a personality analysis expert."},
                {"role": "user", "content": prompt}
            ],
        )
        profile_json = response.choices[0].message.content
        
        # Extract JSON from the text in case it contains other content
        profile_json = extract_json_from_text(profile_json)
        
        # Parse the JSON
        import json
        profile_data = json.loads(profile_json)
        
        return profile_data
    except Exception as e:
        st.error(f"Error extracting personality profile with Groq: {str(e)}")
        # Return a basic profile on error
        return {
            "decision_style": "unknown",
            "emotional_baseline": "neutral",
            "language_tone": "casual",
            "core_values": ["growth"],
            "behavior_patterns": {
                "conflict_handling": "accommodating",
                "communication_preference": "concise"
            },
            "preferences": {
                "general": []
            }
        }

def extract_basic_profile(text):
    """
    Extract a basic personality profile using simple pattern matching.
    
    Args:
        text: Text to analyze
        
    Returns:
        Dictionary with basic personality profile data
    """
    # Simple regex-based analysis
    decision_style = "analytical" if re.search(r'\b(analyze|consider|think|weigh|evidence|logic|rational)\b', text, re.I) else "intuitive"
    
    # Sentiment analysis
    positive_words = ["happy", "excited", "good", "great", "love", "enjoy", "positive", "hope"]
    negative_words = ["sad", "upset", "bad", "terrible", "hate", "dislike", "negative", "worry", "anxiety"]
    
    positive_count = sum(1 for word in positive_words if re.search(rf'\b{word}\b', text, re.I))
    negative_count = sum(1 for word in negative_words if re.search(rf'\b{word}\b', text, re.I))
    
    if positive_count > negative_count:
        emotional_baseline = "optimistic"
    elif negative_count > positive_count:
        emotional_baseline = "cautious"
    else:
        emotional_baseline = "neutral"
    
    # Language tone
    formal_indicators = ["therefore", "moreover", "thus", "consequently", "subsequently", "furthermore"]
    technical_indicators = ["system", "process", "technical", "methodology", "implement", "framework"]
    
    formal_count = sum(1 for word in formal_indicators if re.search(rf'\b{word}\b', text, re.I))
    technical_count = sum(1 for word in technical_indicators if re.search(rf'\b{word}\b', text, re.I))
    
    if formal_count > 3:
        language_tone = "formal"
    elif technical_count > 3:
        language_tone = "technical"
    else:
        language_tone = "casual"
    
    # Extract potential values
    value_patterns = {
        "freedom": r'\b(freedom|liberty|independence|choice|options)\b',
        "growth": r'\b(growth|development|improvement|progress|learning)\b',
        "security": r'\b(security|safety|stability|reliability|dependable)\b',
        "family": r'\b(family|parents|children|kids|relationship|partner)\b',
        "achievement": r'\b(achieve|accomplish|success|goal|ambition)\b',
        "creativity": r'\b(creative|create|original|innovative|design)\b',
        "balance": r'\b(balance|harmony|equilibrium|stability)\b',
        "truth": r'\b(truth|honest|authentic|integrity|genuine)\b'
    }
    
    core_values = []
    for value, pattern in value_patterns.items():
        if re.search(pattern, text, re.I) and len(core_values) < 5:
            core_values.append(value)
    
    # Add at least one value if none were detected
    if not core_values:
        core_values = ["growth"]
    
    # Basic profile
    return {
        "decision_style": decision_style,
        "emotional_baseline": emotional_baseline,
        "language_tone": language_tone,
        "core_values": core_values,
        "behavior_patterns": {
            "conflict_handling": "direct" if re.search(r'\b(confront|address|direct|honest|speak up)\b', text, re.I) else "accommodating",
            "communication_preference": "detailed" if re.search(r'\b(detail|thorough|specific|precise)\b', text, re.I) else "concise"
        },
        "preferences": {
            "general": []
        }
    }

def extract_json_from_text(text):
    """Extract JSON from text that might contain other content."""
    # Try to find JSON block in text
    json_match = re.search(r'({.*})', text, re.DOTALL)
    if json_match:
        return json_match.group(1)
    
    # If no JSON block found, look for content between ```json and ```
    code_block_match = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
    if code_block_match:
        return code_block_match.group(1)
    
    # If still not found, return the original text
    return text

def get_user_personality_profile(user_name):
    """
    Get a user's personality profile from the database.
    
    Args:
        user_name: The name of the user
        
    Returns:
        Dictionary with personality profile data or None if not found
    """
    from utils.db import get_or_create_user, get_personality_profile
    
    # Skip database queries if no valid user_name
    if not user_name:
        return None
    
    try:
        # Get user ID
        user_id = get_or_create_user(user_name)
        
        # Get personality profile
        return get_personality_profile(user_id)
    except Exception as e:
        import streamlit as st
        st.error(f"Error retrieving personality profile: {str(e)}")
        return None

def enhance_llm_chain_with_personality(llm_chain, user_name):
    """
    Enhance the LLM chain prompt with the user's personality profile.
    
    Args:
        llm_chain: The LangChain chain
        user_name: The name of the user
        
    Returns:
        Enhanced LLM chain or the original if no profile is found
    """
    # If chain is None or user_name is empty, return the original chain
    if not llm_chain or not user_name:
        return llm_chain
        
    try:
        profile = get_user_personality_profile(user_name)
        
        if not profile:
            return llm_chain
    except Exception as e:
        import streamlit as st
        st.error(f"Error enhancing LLM chain: {str(e)}")
        return llm_chain
    
    # Enhance the prompt with personality details
    try:
        # Extract core profile information
        decision_style = profile.get('decision_style', 'unknown')
        emotional_baseline = profile.get('emotional_baseline', 'neutral')
        language_tone = profile.get('language_tone', 'casual')
        core_values = profile.get('core_values', [])
        core_values_str = ", ".join(core_values) if core_values else "unknown"
        
        # Get behavior patterns
        behavior_patterns = profile.get('behavior_patterns', {})
        conflict_handling = behavior_patterns.get('conflict_handling', 'unknown')
        communication_preference = behavior_patterns.get('communication_preference', 'unknown')
        
        # Modify the prompt template
        current_prompt = llm_chain.prompt.template
        
        personality_info = f"""
        Additional personality information for {user_name}:
        - Decision-making style: {decision_style}
        - Emotional baseline: {emotional_baseline}
        - Typical communication tone: {language_tone}
        - Core values: {core_values_str}
        - Conflict handling style: {conflict_handling}
        - Communication preference: {communication_preference}
        
        Make sure your response reflects these personality traits accurately.
        """
        
        # Insert the personality info before the last paragraph
        sections = current_prompt.split("\n\n")
        if len(sections) >= 2:
            sections.insert(-1, personality_info)
            enhanced_prompt = "\n\n".join(sections)
            
            # Update the prompt
            llm_chain.prompt.template = enhanced_prompt
            
            st.success("Enhanced response generation with personality profile")
        
        return llm_chain
        
    except Exception as e:
        st.warning(f"Could not enhance prompt with personality: {str(e)}")
        return llm_chain