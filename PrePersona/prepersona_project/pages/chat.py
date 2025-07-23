import streamlit as st
from utils.llm_handler import get_groq_client, get_selected_model
from utils.db import get_or_create_user, save_conversation
from utils.continuous_learner import initialize_continuous_learning, learn_from_conversation, toggle_continuous_learning
import time

st.set_page_config(
    page_title="PrePersona - Chat with AI",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize continuous learning
initialize_continuous_learning()

# Create or get user
if 'user_name' not in st.session_state:
    st.session_state.user_name = "DefaultUser"  # Default username
if 'user_id' not in st.session_state:
    user_id = get_or_create_user(st.session_state.user_name)
    st.session_state.user_id = user_id

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
if st.sidebar.button("Your Personality Profile"):
    st.switch_page("pages/profile.py")
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
    help="Select which Groq model powers your chat experience."
)

# Update the model selection in session state
if st.session_state.get("selected_model") != selected_model:
    st.session_state.selected_model = selected_model
    st.rerun()

# Continuous learning toggle
st.sidebar.title("Learning Settings")
continuous_learning_enabled = st.session_state.get("continuous_learning_enabled", True)
if st.sidebar.toggle("Enable Continuous Learning", value=continuous_learning_enabled, 
                   help="When enabled, the AI will learn from your conversations to build your digital clone"):
    if not continuous_learning_enabled:
        toggle_continuous_learning()
        st.sidebar.success("Continuous learning enabled!")
else:
    if continuous_learning_enabled:
        toggle_continuous_learning()
        st.sidebar.info("Continuous learning disabled.")

# Username input
current_name = st.session_state.get("user_name", "")
username = st.sidebar.text_input("Your Name", value=current_name)
if username != current_name and username.strip():
    st.session_state.user_name = username.strip()
    user_id = get_or_create_user(st.session_state.user_name)
    st.session_state.user_id = user_id
    st.sidebar.success(f"Welcome, {st.session_state.user_name}!")
    st.rerun()

# Initialize chat history
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# Main content
st.title("PrePersona Chat")
st.markdown("""
This chat interface serves two purposes:

1. **General assistance** - Get help with any question you have
2. **Building your digital clone** - As you chat, the AI learns about your communication style, preferences, and decision patterns

The more you chat, the better your digital clone will become. No need to manually upload data!
""")

# Learning progress indicator
if st.session_state.get("continuous_learning_enabled", True):
    conv_count = st.session_state.get("conversation_count", 0)
    profile_updates = st.session_state.get("profile_update_counter", 0)
    
    # Show a progress bar based on conversation count
    if conv_count > 0:
        progress = min(conv_count / 20.0, 1.0)  # Progress maxes out at 20 conversations
        st.progress(progress, text=f"Learning progress: {int(progress * 100)}%")
        
        if profile_updates > 0:
            st.success(f"Your digital clone has evolved {profile_updates} times based on your conversations!")
    else:
        st.info("Start chatting to build your digital clone!")
else:
    st.warning("Continuous learning is disabled. Enable it in the sidebar to build your digital clone through conversations.")

# Display chat messages
for message in st.session_state.chat_messages:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])

# Personality probing questions
personality_questions = [
    "What's your favorite way to spend a free weekend?",
    "How do you usually approach difficult decisions?",
    "What values are most important to you in life?",
    "How would your friends describe your communication style?",
    "What topics are you passionate about discussing?",
    "What's your typical reaction when faced with unexpected changes?",
    "What are some of your favorite books, movies, or shows?",
    "How do you prefer to learn new information?",
    "What motivates you most in your personal or professional life?",
    "How do you handle disagreements with others?"
]

# Chat input
if prompt := st.chat_input("Ask me anything or respond to my questions..."):
    # Add user message to chat history
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    
    # Display user message
    st.chat_message("user").write(prompt)
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            ai_response = ""
            if groq_client:
                # Add personality questions periodically if continuous learning is enabled
                system_message = "You are a helpful, friendly, and knowledgeable assistant."
                
                if st.session_state.get("continuous_learning_enabled", True):
                    # Every few messages, encourage learning about the user
                    if len(st.session_state.chat_messages) % 4 == 0:
                        question_idx = (len(st.session_state.chat_messages) // 4) % len(personality_questions)
                        system_message += f" After answering the user's question fully, ask the following question to learn more about them: '{personality_questions[question_idx]}'"
                
                try:
                    # Use Groq's API
                    # Convert our messages to Groq format
                    groq_messages = [
                        {"role": "system", "content": system_message},
                        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_messages]
                    ]
                    
                    response = groq_client.chat.completions.create(
                        model=selected_model,  # The selected Groq model
                        messages=groq_messages,
                        max_tokens=2000
                    )
                    ai_response = response.choices[0].message.content
                except Exception as e:
                    st.error(f"Error with Groq API: {str(e)}")
                    ai_response = "I'm sorry, but I encountered an error with the Groq API. Please check your API key."
            else:
                ai_response = "I'm sorry, but I don't have access to a Groq model right now. Please provide a Groq API key in the environment variables."
            
            # Display AI response
            st.write(ai_response)
            
            # Add AI response to chat history
            st.session_state.chat_messages.append({"role": "assistant", "content": ai_response})
            
            # Learn from the conversation if continuous learning is enabled
            if st.session_state.get("continuous_learning_enabled", True) and groq_client and ai_response:
                with st.spinner("Updating your digital clone..."):
                    # Ensure we have a valid user_id
                    user_id = st.session_state.get("user_id")
                    if not user_id and st.session_state.get("user_name"):
                        user_id = get_or_create_user(st.session_state.get("user_name"))
                        st.session_state.user_id = user_id
                        
                    if user_id:
                        learn_from_conversation(
                            user_id, 
                            prompt, 
                            ai_response, 
                            selected_model,
                            groq_client
                        )
                    else:
                        st.warning("Please enter your name in the sidebar to enable continuous learning.")

# Clear chat button and tutorial
col1, col2 = st.columns([1, 6])
with col1:
    if st.button("Clear Chat"):
        st.session_state.chat_messages = []
        st.rerun()
with col2:
    with st.expander("How continuous learning works"):
        st.markdown("""
        ### Building Your Digital Clone Through Chat
        
        With continuous learning enabled, PrePersona analyzes your conversations to:
        
        1. **Understand your communication style** - formal, casual, technical, etc.
        2. **Learn your decision patterns** - analytical, intuitive, cautious, etc. 
        3. **Identify preferences** - topics you care about, things you like/dislike
        4. **Extract core values** - what matters most to you based on how you communicate
        
        The more you chat, the more accurate your digital clone becomes. After several conversations, 
        visit your Profile page to see what the AI has learned about you.
        
        Your digital clone improves with:
        - Longer, more detailed responses from you
        - Personal stories and examples
        - Discussions about your preferences and opinions
        - Responses to the AI's personality-probing questions
        """)

# Footer
st.markdown("---")
st.markdown("**PrePersona** - Your future self, available today.")