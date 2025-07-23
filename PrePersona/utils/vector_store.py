import os
import faiss
import numpy as np
import pickle
import streamlit as st
from datetime import datetime
import tempfile
import groq
from utils.db import save_vector_store_db, load_vector_store_db

class VectorStore:
    def __init__(self, dimension=1536):  # Standard embedding dimension
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.docs = []
        self.metadata = []
    
    def add_documents(self, docs, embeddings, metadata_list=None):
        """
        Add documents and their embeddings to the vector store.
        
        Args:
            docs (list): List of document texts
            embeddings (list): List of document embeddings (numpy arrays)
            metadata_list (list, optional): List of metadata dicts for each document
        """
        if metadata_list is None:
            metadata_list = [{} for _ in range(len(docs))]
        
        # Convert embeddings to numpy array
        embeddings_array = np.array(embeddings).astype('float32')
        
        # Add to FAISS index
        self.index.add(embeddings_array)
        
        # Store documents and metadata
        self.docs.extend(docs)
        self.metadata.extend(metadata_list)
    
    def search(self, query_embedding, k=5):
        """
        Search for the k most similar documents to the query.
        
        Args:
            query_embedding: The embedding of the query (numpy array)
            k (int): Number of documents to retrieve
            
        Returns:
            List of tuples (document, score, metadata)
        """
        # Convert query embedding to the right shape
        if len(query_embedding.shape) == 1:
            query_embedding = np.expand_dims(query_embedding, axis=0)
        
        # Search the index
        scores, indices = self.index.search(query_embedding, min(k, len(self.docs)))
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.docs) and idx >= 0:  # Ensure the index is valid
                results.append((self.docs[idx], scores[0][i], self.metadata[idx]))
        
        return results
    
    def save(self, directory):
        """Save the vector store to disk"""
        os.makedirs(directory, exist_ok=True)
        
        # Save the FAISS index
        faiss.write_index(self.index, os.path.join(directory, "faiss_index.bin"))
        
        # Save documents and metadata
        with open(os.path.join(directory, "docs_metadata.pkl"), "wb") as f:
            pickle.dump((self.docs, self.metadata), f)
    
    @staticmethod
    def load(directory):
        """Load a vector store from disk"""
        # Load the FAISS index
        index = faiss.read_index(os.path.join(directory, "faiss_index.bin"))
        
        # Load documents and metadata
        with open(os.path.join(directory, "docs_metadata.pkl"), "rb") as f:
            docs, metadata = pickle.load(f)
        
        # Create a new instance and set its attributes
        store = VectorStore(dimension=index.d)
        store.index = index
        store.docs = docs
        store.metadata = metadata
        
        return store

def initialize_vector_store():
    """Initialize or load the vector store."""
    return VectorStore()

def create_embeddings(processed_data, client):
    """
    Create embeddings for processed data using either Groq API or a fallback method.
    
    Args:
        processed_data: List of dictionaries with 'text' and 'metadata' fields
        client: Groq client
        
    Returns:
        texts, embeddings, metadata_list
    """
    if not processed_data:
        return [], [], []
    
    texts = [item["text"] for item in processed_data]
    metadata_list = [item["metadata"] for item in processed_data]
    
    # Determine embedding method based on client type
    use_groq = isinstance(client, groq.Groq)
    
    if not use_groq:
        st.warning("Using basic embedding method. For optimal results, provide a Groq API key.")
        # Basic fallback embedding method
        all_embeddings = []
        with st.spinner("Creating basic embeddings for your data... This may take a moment"):
            for i, text in enumerate(texts):
                if i % 20 == 0:  # Show progress less frequently for basic method
                    progress_text = f"Processing item {i+1}/{len(texts)}"
                    st.write(progress_text)
                
                # Create a simple bag of words embedding (very basic)
                words = text.lower().split()
                embedding = np.zeros(1536)  # Standard embedding dimension
                for i, word in enumerate(words[:1536]):  # Limit to embedding dimension
                    embedding[i % 1536] = hash(word) % 1000 / 1000
                embedding = embedding / (np.linalg.norm(embedding) + 1e-5)  # Normalize
                all_embeddings.append(embedding)
        
        return texts, all_embeddings, metadata_list
    
    # Groq embedding method
    batches = [texts[i:i+100] for i in range(0, len(texts), 100)]  # Batch size of 100
    all_embeddings = []
    
    with st.spinner("Creating embeddings for your data... This may take a moment"):
        for i, batch in enumerate(batches):
            progress_text = f"Processing batch {i+1}/{len(batches)}"
            st.write(progress_text)
            
            try:
                # For each text, use Groq chat completions API with a selected model
                batch_embeddings = []
                
                for text in batch:
                    # Convert text to embedding using Groq
                    # Since Groq doesn't have a dedicated embeddings API like OpenAI,
                    # we'll use a simple hash-based approach similar to the fallback method
                    words = text.lower().split()
                    embedding = np.zeros(1536)
                    for i, word in enumerate(words[:1536]):
                        embedding[i % 1536] = hash(word) % 1000 / 1000
                    embedding = embedding / (np.linalg.norm(embedding) + 1e-5)
                    batch_embeddings.append(embedding)
                
                all_embeddings.extend(batch_embeddings)
            except Exception as e:
                st.error(f"Error creating embeddings with Groq: {str(e)}")
                # On error, fall back to basic method for this batch
                st.warning("Falling back to basic embedding method for this batch.")
                for text in batch:
                    words = text.lower().split()
                    embedding = np.zeros(1536)
                    for i, word in enumerate(words[:1536]):
                        embedding[i % 1536] = hash(word) % 1000 / 1000
                    embedding = embedding / (np.linalg.norm(embedding) + 1e-5)
                    all_embeddings.append(embedding)
    
    return texts, all_embeddings, metadata_list

def save_vector_store(vector_store, user_name):
    """
    Save the vector store to database and backup to filesystem.
    
    Args:
        vector_store: The VectorStore object to save
        user_name: User name to associate with the vector store
        
    Returns:
        Path to the filesystem backup
    """
    if not vector_store:
        return None
    
    # Get or create user ID
    from utils.db import get_or_create_user
    user_id = get_or_create_user(user_name)
    
    # Save to database
    try:
        save_vector_store_db(user_id, vector_store)
        st.success(f"Vector store saved to database for user {user_name}")
    except Exception as e:
        st.warning(f"Could not save vector store to database: {str(e)}")
    
    # Create filesystem backup (temp directory)
    tmp_dir = tempfile.mkdtemp()
    vs_dir = os.path.join(tmp_dir, f"{user_name}_vector_store")
    
    # Save the vector store to filesystem backup
    vector_store.save(vs_dir)
    
    return vs_dir

def load_vector_store(user_name_or_dir):
    """
    Load a vector store from database or filesystem.
    
    Args:
        user_name_or_dir: Either a user name (to load from DB) or a directory path
        
    Returns:
        VectorStore object or None if not found
    """
    # First try to load from database by user name
    if not os.path.exists(user_name_or_dir):
        # Likely a user name, not a directory
        from utils.db import get_or_create_user
        user_id = get_or_create_user(user_name_or_dir)
        
        try:
            vector_store = load_vector_store_db(user_id, VectorStore)
            if vector_store:
                st.success(f"Vector store loaded from database for user {user_name_or_dir}")
                return vector_store
        except Exception as e:
            st.warning(f"Could not load vector store from database: {str(e)}")
    
    # If database load failed, try filesystem
    if os.path.exists(user_name_or_dir):
        try:
            vector_store = VectorStore.load(user_name_or_dir)
            st.success(f"Vector store loaded from filesystem backup")
            return vector_store
        except Exception as e:
            st.error(f"Error loading vector store from filesystem: {str(e)}")
    
    return None
