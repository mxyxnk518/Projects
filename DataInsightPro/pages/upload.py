import streamlit as st
import os
import time
from utils.data_processor import get_upload_types, process_user_data
from utils.vector_store import initialize_vector_store, create_embeddings
from utils.llm_handler import get_groq_client, setup_llm_chain, get_selected_model
from utils.dark_mode_styles import apply_dark_mode, create_navigation_sidebar

st.set_page_config(
    page_title="PrePersona - UPLOAD",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply dark mode styling
apply_dark_mode()

# Model selection
selected_model = get_selected_model()

# Initialize Groq client
groq_client = get_groq_client()

# If no client is available, show a warning
if not groq_client:
    st.warning("No Groq API key available. Please provide a Groq API key to use the app.")

# Sidebar with navigation
st.sidebar.title("Navigation")
if st.sidebar.button("Home"):
    st.switch_page("pages/home.py")
if st.sidebar.button("Ask Your Digital Clone"):
    st.switch_page("pages/query.py")
if st.sidebar.button("About"):
    st.switch_page("pages/about.py")

# Initialize Groq client
groq_client = get_groq_client()

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
st.title("Upload Your Data")
st.markdown("""
Upload personal data to train your digital clone. PrePersona learns from your writing style, 
decision patterns, and communication habits to create a digital representation of you.

**Privacy Note:** All your data is processed locally and not stored permanently. 
Your information is only used to create your digital clone and is not shared with any third parties.
""")

# Name input field with current value if available
st.subheader("Your Identity")
current_name = st.session_state.get("user_name", "")
user_name = st.text_input(
    "Enter your name (how your digital clone should refer to you):", 
    value=current_name,
    help="This name will be used throughout your experience with PrePersona"
)

# Update the name in session state if changed
if user_name and user_name != current_name:
    st.session_state.user_name = user_name
    st.success(f"Name updated to: {user_name}")
elif not user_name and current_name:
    st.warning("Please enter your name to continue")

# Show upload interface if user has provided their name
if "user_name" in st.session_state and st.session_state.user_name:
    st.subheader(f"Upload Data for {st.session_state.user_name}'s Digital Clone")
    
    # Get upload types
    upload_types = get_upload_types()
    
    # Create tabs for different upload types
    tabs = st.tabs(list(upload_types.keys()))
    
    upload_instructions = {
        "Text/Journal": "Upload text files containing your journal entries, notes, or any written content.",
        "Chat Export": "Upload chat exports from messaging platforms (WhatsApp, Telegram, Discord, etc.).",
        "Calendar": "Upload calendar exports (.ics files or CSV exports) to include your scheduling patterns.",
        "Email": "Upload email exports to include your communication style.",
        "Social Media Export": "Upload social media data exports (Twitter, Facebook, etc.)."
    }
    
    uploaded_files = []
    
    for i, (data_type, extensions) in enumerate(upload_types.items()):
        with tabs[i]:
            st.markdown(upload_instructions[data_type])
            st.markdown(f"Supported formats: {', '.join(extensions)}")
            
            # File uploader
            files = st.file_uploader(
                f"Upload {data_type} files",
                accept_multiple_files=True,
                type=extensions,
                key=f"uploader_{data_type}"
            )
            
            if files:
                uploaded_files.extend(files)
                st.success(f"Uploaded {len(files)} {data_type} files")
    
    # Process button
    if uploaded_files:
        st.subheader("Process Uploaded Data")
        st.write(f"Total files uploaded: {len(uploaded_files)}")
        
        if st.button("Process Data and Create Digital Clone"):
            with st.spinner("Processing your data..."):
                # Process the uploaded files
                processed_data, summary = process_user_data(uploaded_files, st.session_state.user_name)
                
                if processed_data:
                    st.session_state.processed_data_summary = summary
                    st.session_state.uploaded_files_count = len(uploaded_files)
                    
                    # Create vector store
                    vector_store = initialize_vector_store()
                    
                    # Generate embeddings for the processed data
                    texts, embeddings, metadata_list = create_embeddings(processed_data, groq_client)
                    
                    if texts and embeddings and metadata_list:
                        # Add documents to vector store
                        vector_store.add_documents(texts, embeddings, metadata_list)
                        
                        # Store vector store in session state
                        st.session_state.vector_store = vector_store
                        
                        # Set up LLM chain
                        llm_chain = setup_llm_chain()
                        st.session_state.llm_chain = llm_chain
                        
                        # Mark as ready
                        st.session_state.is_ready = True
                        
                        # Save data to database
                        from utils.db import get_or_create_user, store_user_data, save_vector_store_db
                        
                        with st.spinner("Saving data to database..."):
                            try:
                                # Get or create user
                                user_id = get_or_create_user(st.session_state.user_name)
                                
                                # Store processed data with embeddings
                                store_user_data(user_id, processed_data, embeddings)
                                
                                # Save vector store
                                save_vector_store_db(user_id, vector_store)
                                
                                st.success("Data successfully saved to database")
                                
                                # Generate initial personality profile
                                from utils.personality import extract_personality_profile
                                extract_personality_profile(user_id, processed_data)
                                
                            except Exception as e:
                                st.warning(f"Could not save data to database: {str(e)}")
                                st.info("Your data is still available for this session, but may not persist after closing the app.")
                        
                        # Show success message
                        st.success("Your digital clone has been created successfully!")
                        
                        # Summary information
                        st.subheader("Data Processing Summary")
                        st.write(f"Total entries processed: {summary['total_entries']}")
                        st.write(f"Total words processed: {summary['total_words']}")
                        
                        if summary['date_range']['start'] and summary['date_range']['end']:
                            st.write(f"Date range: {summary['date_range']['start'].strftime('%Y-%m-%d')} to {summary['date_range']['end'].strftime('%Y-%m-%d')}")
                        
                        st.write("File types processed:")
                        for file_type, count in summary['file_types_processed'].items():
                            st.write(f"- {file_type}: {count} files")
                        
                        # Redirect to query page after a short delay
                        st.markdown("Redirecting to the query page in 5 seconds...")
                        time.sleep(5)
                        st.switch_page("pages/query.py")
                else:
                    st.error("No data could be processed from the uploaded files. Please try different files.")
    else:
        st.info("Please upload at least one file to create your digital clone.")
else:
    st.info("Please enter your name to get started.")

# Footer
st.markdown("---")
st.markdown("**PrePersona** - Your future self, available today.")
