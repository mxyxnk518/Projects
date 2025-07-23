import streamlit as st
from utils.dark_mode_styles import apply_dark_mode, create_navigation_sidebar

st.set_page_config(
    page_title="PrePersona - ABOUT",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply dark mode styling
apply_dark_mode()

# Sidebar with navigation
st.sidebar.title("NAVIGATION")
if st.sidebar.button("Home"):
    st.switch_page("pages/home.py")
if st.sidebar.button("Upload Your Data"):
    st.switch_page("pages/upload.py")
if st.sidebar.button("Ask Your Digital Clone"):
    st.switch_page("pages/query.py")
if st.sidebar.button("Your Personality Profile"):
    st.switch_page("pages/profile.py")

# Main content
st.title("About PrePersona")

st.markdown("""
## What is PrePersona?

**PrePersona** is an AI-powered digital clone that learns how you think, communicate, and make decisions. 
It creates a personalized AI model based on your data that can predict how you would respond to new situations.

Unlike general AI chatbots, PrePersona doesn't give generic answers - it gives YOUR answers, 
based on your unique communication style, preferences, and decision-making patterns.

## How It Works

PrePersona uses advanced AI technology to process and learn from your personal data:

1. **Data Processing**: Your uploaded data (chats, journals, notes, calendar entries) is processed to extract your 
communication patterns, preferences, and decision-making style.

2. **Vector Embedding**: The processed data is converted into numerical representations (embeddings) that capture 
the semantic meaning of your writing and decisions.

3. **Contextual Retrieval**: When you ask a question, PrePersona finds the most relevant pieces of your data 
that would inform your response.

4. **Personalized Generation**: Using the retrieved context, PrePersona generates a response that mimics how 
you would likely respond, matching your tone, style, and decision patterns.

## Technology Behind PrePersona

PrePersona is built using cutting-edge AI technologies:

- **LangChain**: Orchestrates the workflow of retrieving relevant context and generating personalized responses
- **FAISS**: Provides efficient similarity search for finding the most relevant pieces of your data
- **AI Models**: Uses Anthropic Claude and/or OpenAI GPT-4 for understanding and generating natural language
- **PostgreSQL Database**: Securely stores your personality profile and conversation history
- **Vector Embeddings**: Converts text into numerical representations that capture semantic meaning

## Privacy & Security

PrePersona takes your privacy seriously:

- All data processing happens within your personal environment
- Your information is stored securely in your own PostgreSQL database
- Your data is only used to create your digital clone and is not shared with third parties
- Your API keys for AI providers are stored securely as environment variables

## Use Cases

PrePersona can help you in various ways:

- **Personal Decision Assistant**: Get insights into how you would likely approach different situations
- **Communication Helper**: Draft messages in your own style for different contexts
- **Reflection Tool**: Understand your own patterns and preferences better
- **Memory Extension**: Recall how you've handled similar situations in the past
- **Digital Legacy**: Create a digital version of yourself that captures your essence

## Limitations

While PrePersona aims to accurately represent you, it has some limitations:

- It can only learn from the data you provide - more data means better accuracy
- It may not capture nuanced emotional states or context-specific reasoning perfectly
- It represents your past self based on historical data, not necessarily your current or future self
- It is not a substitute for your actual thoughts and decisions, but rather a simulation

## Future Developments

PrePersona is continuously evolving. Future updates may include:

- Support for more data sources and formats
- Improved personalization and accuracy
- Real-time synchronization with your digital activities
- Integration with productivity tools and communication platforms
""")

# FAQ Section
st.subheader("Frequently Asked Questions")

faq = {
    "Is my data secure?": "Yes, your data is processed and stored within your own personal environment using a secure PostgreSQL database. We don't share your information with third parties.",
    
    "How much data do I need to upload?": "The more data you provide, the more accurate your digital clone will be. We recommend uploading at least several text files or chat exports to start seeing personalized results.",
    
    "What types of files can I upload?": "PrePersona supports various file formats including text files (.txt), chat exports (.txt, .json), calendar data (.ics, .csv), and more. Check the upload page for the full list of supported formats.",
    
    "How accurate is PrePersona?": "The accuracy depends on the amount and quality of data you provide. With sufficient data, PrePersona can capture your communication style and common decision patterns quite well, but it cannot perfectly predict complex decisions or emotional responses.",
    
    "Which AI models does PrePersona use?": "PrePersona supports both Anthropic Claude and OpenAI GPT models. You can choose which model to use in the settings, with Anthropic Claude set as the default.",
    
    "Is this different from ChatGPT?": "Yes, while ChatGPT gives general responses based on its training, PrePersona gives personalized responses based specifically on YOUR data, mimicking how YOU would respond."
}

for question, answer in faq.items():
    with st.expander(question):
        st.write(answer)

# Footer
st.markdown("---")
st.markdown("**PrePersona** - Your future self, available today.")
