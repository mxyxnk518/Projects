import streamlit as st
from utils.db import save_conversation, update_personality_profile, get_conversations, get_personality_profile
from utils.personality import extract_profile_with_ai
import os
import json
from datetime import datetime, timedelta

def initialize_continuous_learning():
    """Initialize continuous learning for first-time users"""
    if 'continuous_learning_enabled' not in st.session_state:
        st.session_state.continuous_learning_enabled = True
    
    if 'conversation_count' not in st.session_state:
        st.session_state.conversation_count = 0
    
    if 'profile_update_counter' not in st.session_state:
        st.session_state.profile_update_counter = 0
    
    if 'last_profile_update' not in st.session_state:
        st.session_state.last_profile_update = datetime.now() - timedelta(days=1)

def learn_from_conversation(user_id, question, response, model_used, client):
    """
    Learn from the current conversation to continuously update the user's profile.
    
    Args:
        user_id: The ID of the user
        question: The user's question
        response: The AI's response
        model_used: The model used for the response
        client: The AI client (Groq)
    """
    # Save conversation to database
    try:
        save_conversation(user_id, question, response, model_used)
        
        # Increment conversation counter
        if 'conversation_count' not in st.session_state:
            st.session_state.conversation_count = 0
        st.session_state.conversation_count += 1
        
        # Check if we should update the personality profile
        should_update_profile = False
        
        # Update after every few conversations
        if st.session_state.conversation_count % 3 == 0:
            should_update_profile = True
        
        # Or if it's been a while since the last update
        time_since_update = datetime.now() - st.session_state.get('last_profile_update', datetime.now() - timedelta(days=1))
        if time_since_update > timedelta(hours=1):
            should_update_profile = True
        
        if should_update_profile:
            # Update the personality profile based on conversations
            update_profile_from_conversations(user_id, client, model_used)
            
            # Reset counter and update timestamp
            st.session_state.profile_update_counter += 1
            st.session_state.last_profile_update = datetime.now()
            
            if st.session_state.profile_update_counter % 5 == 0:
                st.success("Your digital clone has evolved based on your conversations!", icon="🔄")
    
    except Exception as e:
        st.warning(f"Could not save conversation for learning: {str(e)}")

def update_profile_from_conversations(user_id, client, model_type):
    """
    Update the user's personality profile based on recent conversations.
    
    Args:
        user_id: The ID of the user
        client: The AI client (Groq)
        model_type: The type of model (Groq model name)
    """
    try:
        # Get recent conversations
        recent_convs = get_conversations(user_id, limit=10)
        
        if not recent_convs or len(recent_convs) < 2:
            return  # Not enough conversations to learn from
        
        # Format conversations for analysis
        conv_text = ""
        for conv in recent_convs:
            # Handle different return formats depending on the implementation of get_conversations
            if isinstance(conv, tuple) and len(conv) >= 2:
                # Unpacking the tuple format (question, response, timestamp)
                question, response = conv[0], conv[1]
                conv_text += f"User: {question}\n"
                conv_text += f"Response: {response}\n\n"
            elif hasattr(conv, 'question') and hasattr(conv, 'response'):
                # Object format with attributes
                conv_text += f"User: {conv.question}\n"
                conv_text += f"Response: {conv.response}\n\n"
            elif isinstance(conv, dict) and 'question' in conv and 'response' in conv:
                # Dictionary format
                conv_text += f"User: {conv['question']}\n"
                conv_text += f"Response: {conv['response']}\n\n"
        
        # Get current profile if it exists
        current_profile = get_personality_profile(user_id)
        
        # Process conversations with AI to extract/update personality
        profile_prompt = f"""
        Analyze the following conversation snippets from a user.
        Extract or update their personality traits, values, and communication style.
        
        Conversations to analyze:
        {conv_text}
        
        Based on these conversations, create or update the personality profile with the following attributes:
        
        1. Decision making style (analytical, intuitive, deliberate, spontaneous, etc.)
        2. Emotional baseline (optimistic, cautious, neutral, anxious, etc.)
        3. Language tone (formal, casual, technical, poetic, etc.)
        4. Core values (list 3-5 values that seem important to this person)
        5. Behavior patterns (how they handle conflict, communication preferences)
        6. General preferences (things they like/dislike based on the conversations)
        
        Return the profile as a structured JSON object with these fields:
        decision_style, emotional_baseline, language_tone, core_values (array), 
        behavior_patterns (object with conflict_handling and communication_preference), preferences (object with general array).
        
        Respond only with the JSON, no explanations or other text.
        """
        
        new_insights = extract_profile_with_ai(conv_text, client, model_type)
        
        # If we have a current profile, merge the new insights with the current profile
        if current_profile:
            # For basic fields, prefer new insights if they have high confidence
            if 'decision_style' in new_insights and new_insights['decision_style'] != 'unknown':
                current_profile['decision_style'] = new_insights['decision_style']
            
            if 'emotional_baseline' in new_insights and new_insights['emotional_baseline'] != 'neutral':
                current_profile['emotional_baseline'] = new_insights['emotional_baseline']
            
            if 'language_tone' in new_insights and new_insights['language_tone'] != 'casual':
                current_profile['language_tone'] = new_insights['language_tone']
            
            # For arrays and objects, merge them
            if 'core_values' in new_insights and new_insights['core_values']:
                # Add new values while keeping old ones, remove duplicates
                combined_values = list(set(current_profile.get('core_values', []) + new_insights['core_values']))
                current_profile['core_values'] = combined_values[:5]  # Limit to 5 values
            
            if 'behavior_patterns' in new_insights and new_insights['behavior_patterns']:
                if 'behavior_patterns' not in current_profile:
                    current_profile['behavior_patterns'] = {}
                
                # Update behavior patterns with new insights
                for key, value in new_insights['behavior_patterns'].items():
                    if value != 'unknown':
                        current_profile['behavior_patterns'][key] = value
            
            if 'preferences' in new_insights and new_insights['preferences']:
                if 'preferences' not in current_profile:
                    current_profile['preferences'] = {}
                
                # Merge preferences
                for key, value in new_insights['preferences'].items():
                    if key not in current_profile['preferences']:
                        current_profile['preferences'][key] = value
                    else:
                        # For arrays like 'general', combine them
                        if isinstance(value, list) and isinstance(current_profile['preferences'][key], list):
                            current_profile['preferences'][key] = list(set(current_profile['preferences'][key] + value))
            
            # Update the profile in the database
            update_personality_profile(user_id, current_profile)
        else:
            # If no current profile, use the new insights as is
            update_personality_profile(user_id, new_insights)
    
    except Exception as e:
        st.warning(f"Could not update personality profile from conversations: {str(e)}")

def get_conversation_insights(user_id, client, model_type):
    """
    Get insights into the user's recent conversations.
    
    Args:
        user_id: The ID of the user
        client: The AI client (Groq)
        model_type: The type of model (Groq model name)
        
    Returns:
        A dictionary with insights about the user's conversations
    """
    try:
        # Get recent conversations
        recent_convs = get_conversations(user_id, limit=20)
        
        if not recent_convs or len(recent_convs) < 5:
            return {"status": "not_enough_data", "message": "Not enough conversations to generate insights"}
        
        # Format conversations for analysis
        conv_text = ""
        for conv in recent_convs:
            # Handle different return formats depending on the implementation of get_conversations
            if isinstance(conv, tuple) and len(conv) >= 2:
                # Unpacking the tuple format (question, response, timestamp)
                question, response = conv[0], conv[1]
                conv_text += f"User: {question}\n"
                conv_text += f"Response: {response}\n\n"
            elif hasattr(conv, 'question') and hasattr(conv, 'response'):
                # Object format with attributes
                conv_text += f"User: {conv.question}\n"
                conv_text += f"Response: {conv.response}\n\n"
            elif isinstance(conv, dict) and 'question' in conv and 'response' in conv:
                # Dictionary format
                conv_text += f"User: {conv['question']}\n"
                conv_text += f"Response: {conv['response']}\n\n"
        
        # Generate insights with AI
        insights_prompt = f"""
        Analyze the following conversation snippets from a user.
        Extract insights about their communication patterns and interests.
        
        Conversations to analyze:
        {conv_text}
        
        Based on these conversations, provide the following insights:
        
        1. Common topics (list 3-5 topics the user discusses frequently)
        2. Question patterns (how does the user tend to ask questions?)
        3. Decision scenarios (types of decisions the user seeks advice on)
        4. Growth observations (how has the user's communication evolved?)
        5. Interesting insights (what unique patterns do you notice?)
        
        Return the insights as a structured JSON object with these fields:
        common_topics (array), question_patterns (object), decision_scenarios (array),
        growth_observations (string), interesting_insights (array).
        
        Respond only with the JSON, no explanations or other text.
        """
        
        # Use Groq to extract insights
        response = client.chat.completions.create(
            model=model_type,  # Use the specified Groq model
            messages=[
                {"role": "system", "content": "You are a conversation analysis expert."},
                {"role": "user", "content": insights_prompt}
            ]
        )
        insights_json = response.choices[0].message.content
        
        # Extract JSON from text
        import re
        json_match = re.search(r'({.*})', insights_json, re.DOTALL)
        if json_match:
            insights_json = json_match.group(1)
        
        # Parse JSON
        insights = json.loads(insights_json)
        
        return {"status": "success", "insights": insights}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

def toggle_continuous_learning():
    """Toggle the continuous learning feature."""
    if 'continuous_learning_enabled' not in st.session_state:
        st.session_state.continuous_learning_enabled = True
    
    st.session_state.continuous_learning_enabled = not st.session_state.continuous_learning_enabled
    
    return st.session_state.continuous_learning_enabled