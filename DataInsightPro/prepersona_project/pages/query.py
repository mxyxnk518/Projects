import streamlit as st
from utils.llm_handler import query_digital_clone, get_groq_client, get_selected_model, setup_llm_chain
from utils.db import get_or_create_user
from utils.continuous_learner import initialize_continuous_learning, learn_from_conversation
from utils.personality import enhance_llm_chain_with_personality
import time

st.set_page_config(
    page_title="PrePersona - Talk to Your Future Self",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize continuous learning
initialize_continuous_learning()

# Model selection
selected_model = get_selected_model()

# Initialize Groq client
groq_client = get_groq_client()

# If no client is available, use a warning
if not groq_client:
    st.warning("No Groq API key available. Please provide a Groq API key to use the app.")
    
# Initialize user if needed
user_name = st.session_state.get("user_name", "")
if not user_name:
    user_name_input = st.text_input("What should I call you?", placeholder="Enter your name")
    if user_name_input:
        st.session_state.user_name = user_name_input
        user_name = user_name_input
        # Get or create user in DB
        user_id = get_or_create_user(user_name)
        st.session_state.user_id = user_id
        st.rerun()
else:
    # Ensure user_id is in session state
    if "user_id" not in st.session_state:
        user_id = get_or_create_user(user_name)
        st.session_state.user_id = user_id

# Make sure vector store exists (can be empty for new users)
if "vector_store" not in st.session_state or not st.session_state.vector_store:
    from utils.vector_store import initialize_vector_store
    st.session_state.vector_store = initialize_vector_store()
    
# Make sure LLM chain exists
if "llm_chain" not in st.session_state or not st.session_state.llm_chain:
    st.session_state.llm_chain = setup_llm_chain()
    
# Mark as ready since we can now start conversations without uploading data
if "is_ready" not in st.session_state:
    st.session_state.is_ready = True

# Sidebar with navigation
st.sidebar.title("Navigation")
if st.sidebar.button("Home"):
    st.switch_page("pages/home.py")
if st.sidebar.button("Upload Your Data"):
    st.switch_page("pages/upload.py")
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
    # Reset the LLM chain to use the new model
    st.session_state.llm_chain = None
    st.rerun()

# Main content
st.title("Ask Your Digital Clone")

# Check if digital clone is ready
if not st.session_state.get("is_ready", False):
    st.warning("Your digital clone is not ready yet. Please upload your data first.")
    if st.button("Go to Upload Page"):
        st.switch_page("pages/upload.py")
else:
    user_name = st.session_state.get("user_name", "User")
    st.markdown(f"""
    Your digital clone for **{user_name}** is ready! Ask any question to find out how you would 
    likely respond in various situations. The more data you've uploaded, the more accurate the responses will be.
    
    ### Example Questions:
    - "What would I likely do if offered a remote internship in July?"
    - "Draft a birthday message I would write to my best friend."
    - "How would I approach resolving this conflict at work?"
    - "What kind of restaurant would I enjoy for a special occasion?"
    - "How would I prioritize tasks if I had too many deadlines?"
    """)
    
    # Query input
    query = st.text_area("Ask a question to your digital clone:", height=100, 
                         placeholder="Enter your question here...")
    
    # Process query
    if st.button("Generate Response"):
        if query:
            vector_store = st.session_state.get("vector_store")
            llm_chain = st.session_state.get("llm_chain")
            user_name = st.session_state.get("user_name", "")
            
            try:
                # Set up LLM chain if not available
                if not llm_chain:
                    llm_chain = setup_llm_chain()
                    st.session_state.llm_chain = llm_chain
                
                # Enhance LLM chain with personality profile if available
                from utils.personality import enhance_llm_chain_with_personality
                enhanced_llm_chain = enhance_llm_chain_with_personality(llm_chain, user_name)
                
                # Save enhanced chain back to session state
                st.session_state.llm_chain = enhanced_llm_chain
                
                # Use the Groq client to generate response
                response = query_digital_clone(query, user_name, vector_store, enhanced_llm_chain, groq_client)
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
                response = "I'm sorry, I encountered an error while trying to generate a response. Please check the error message above for details."
            
            # Save conversation to database
            from utils.db import get_or_create_user, save_conversation
            try:
                user_id = get_or_create_user(user_name)
                save_conversation(
                    user_id, 
                    query, 
                    response, 
                    model_used=st.session_state.selected_model
                )
            except Exception as e:
                st.warning(f"Could not save conversation to database: {str(e)}")
            
            # Display response
            st.subheader("Your Digital Clone's Response:")
            display_name = st.session_state.get("user_name", "You")
            st.markdown(f"***{display_name}** would likely respond:*")
            st.markdown(response)
            
            # Add to conversation history if it doesn't exist
            if "conversation_history" not in st.session_state:
                st.session_state.conversation_history = []
            
            # Add the current Q&A to history
            st.session_state.conversation_history.append({
                "question": query,
                "response": response
            })
        else:
            st.error("Please enter a question to get a response.")
    
    # Display conversation history
    if "conversation_history" in st.session_state and st.session_state.conversation_history:
        st.subheader("Previous Questions & Responses")
        
        for i, qa in enumerate(reversed(st.session_state.conversation_history)):
            with st.expander(f"Q: {qa['question'][:50]}{'...' if len(qa['question']) > 50 else ''}"):
                st.markdown(f"**Question:** {qa['question']}")
                st.markdown(f"**Response:** {qa['response']}")

# Data summary if available
if st.session_state.get("processed_data_summary"):
    with st.sidebar:
        st.subheader("Your Digital Clone Data")
        summary = st.session_state.processed_data_summary
        st.write(f"Total entries: {summary['total_entries']}")
        st.write(f"Total words: {summary['total_words']}")
        
        if summary['date_range']['start'] and summary['date_range']['end']:
            st.write(f"Date range: {summary['date_range']['start'].strftime('%Y-%m-%d')} to {summary['date_range']['end'].strftime('%Y-%m-%d')}")
        
        st.write("File types:")
        for file_type, count in summary['file_types_processed'].items():
            st.write(f"- {file_type}: {count} files")

# Footer
st.markdown("---")
st.markdown("**PrePersona** - Your future self, available today.")
