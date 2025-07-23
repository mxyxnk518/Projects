import os
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import groq
import numpy as np

def get_groq_client():
    """Initialize the Groq client."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        st.warning("Groq API key not found. Please provide your Groq API key to use the app.")
        return None
    
    return groq.Groq(api_key=api_key)

def get_selected_model():
    """Get the user-selected Groq model from session state."""
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = "llama3-70b-8192"  # Default Groq model
    return st.session_state.selected_model

def setup_llm_chain():
    """Set up LangChain components for generating responses based on selected model."""
    # Get the selected model
    selected_model = get_selected_model()
    
    # Initialize the Groq LLM
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        st.error("Groq API key not found in environment variables.")
        st.info("Please provide your Groq API key to use the app.")
        return None
    
    # Groq supports several models, selected_model should be one of these
    llm = ChatGroq(
        model=selected_model,  # e.g., "llama3-70b-8192", "mixtral-8x7b-32768", etc.
        temperature=0.7,
        groq_api_key=api_key
    )
    
    # Create prompt template for generating responses as if from the user
    user_response_template = PromptTemplate(
        input_variables=["context", "question", "user_name"],
        template="""
        You are an AI that predicts how {user_name} would respond to situations based on their past data.
        
        Here's the relevant context from {user_name}'s data:
        {context}
        
        Given the question: {question}
        
        Generate a detailed response AS IF YOU WERE {user_name}, using their typical tone, style, and decision-making patterns.
        The response should be written in first person (I, me, my) as if {user_name} is directly responding.
        
        Important: Do not mention that you are an AI or that this is a prediction. Respond exactly as {user_name} would respond.
        """
    )
    
    # Create the chain
    chain = LLMChain(
        llm=llm,
        prompt=user_response_template,
        output_parser=StrOutputParser(),
        verbose=False
    )
    
    return chain

def generate_embedding(text, client):
    """
    Generate an embedding for a single text using Groq or a fallback method.
    
    Args:
        text (str): The text to embed
        client: The Groq client
    """
    if not client:
        st.error("No embedding client available. Please provide a Groq API key.")
        return None
    
    # Groq doesn't have a dedicated embeddings endpoint yet, so we'll use a fallback method
    # In the future, this can be updated when Groq provides an embeddings API
    
    try:
        # As a fallback, we'll create a simple bag-of-words embedding
        st.info("Using lightweight embedding method.")
        words = text.lower().split()
        # Create a simple bag of words embedding
        embedding = np.zeros(1536)  # Standard embedding dimension
        for i, word in enumerate(words[:1536]):  # Limit to embedding dimension
            # Simple hash of word to position in embedding
            embedding[i % 1536] = hash(word) % 1000 / 1000
        return embedding / (np.linalg.norm(embedding) + 1e-5)  # Normalize
    except Exception as e:
        st.error(f"Error generating embedding: {str(e)}")
        return None

def query_digital_clone(question, user_name, vector_store, llm_chain, client):
    """
    Query the digital clone based on the user's question.
    
    Args:
        question (str): The question to ask the digital clone
        user_name (str): The name of the user whose digital clone is being queried
        vector_store: The vector store containing the user's data
        llm_chain: The LangChain chain for generating responses
        client: The Groq client for generating embeddings
        
    Returns:
        str: The generated response
    """
    if not vector_store or not llm_chain:
        return "Error: Digital clone is not properly initialized. Please check your setup."
    
    # Generate embedding for the question
    question_embedding = generate_embedding(question, client)
    if question_embedding is None:
        return "Error generating embedding for your question. Please try again."
    
    # Retrieve relevant context from vector store
    k = 5  # Number of documents to retrieve
    with st.spinner("Retrieving relevant context from your data..."):
        results = vector_store.search(question_embedding, k=k)
    
    if not results:
        return "I don't have enough context in my memory to answer this question confidently."
    
    # Format the context
    context_docs = []
    for doc, score, metadata in results:
        # Include metadata in the context if available
        meta_str = ""
        if metadata:
            # Add timestamp if available
            if "timestamp" in metadata and metadata["timestamp"]:
                meta_str += f" (from {metadata['timestamp'].strftime('%Y-%m-%d')})"
            # Add source if available
            if "source" in metadata:
                meta_str += f" (source: {metadata['source']})"
            # Add type if available
            if "type" in metadata:
                meta_str += f" (type: {metadata['type']})"
        
        context_docs.append(f"{doc}{meta_str}")
    
    context = "\n\n".join(context_docs)
    
    # Generate response
    with st.spinner("Generating response based on your personal data..."):
        response = llm_chain.invoke({
            "context": context,
            "question": question,
            "user_name": user_name
        })
    
    # Ensure response is a string (sometimes LangChain returns a dict with text)
    if isinstance(response, dict):
        if 'text' in response:
            return response['text']
        elif 'response' in response:
            return response['response']
        else:
            # Try to convert the full dict to a formatted string
            import json
            try:
                formatted_text = response.get('response', 
                                             response.get('answer',
                                                         response.get('output', 
                                                                     json.dumps(response, indent=2))))
                return str(formatted_text)
            except:
                return str(response)
    
    return str(response)
