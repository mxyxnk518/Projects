import os
import json
import pickle
import base64
import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Text, LargeBinary, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import numpy as np

# Create database connection
DATABASE_URL = os.environ.get('DATABASE_URL')
# Create a persistent SQLite database in case PostgreSQL is not available
SQLITE_URL = 'sqlite:///prepersona.db'  # This creates a file in the current directory

Base = declarative_base()

# Global flag to track database type
use_sqlite = False

# Try to connect to PostgreSQL first
if DATABASE_URL:
    try:
        engine = create_engine(DATABASE_URL, connect_args={
            'connect_timeout': 30,
            'application_name': 'prepersona_app'
        })
        # Test connection with a quick query
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        
        Session = sessionmaker(bind=engine)
        print("Connected to PostgreSQL database")
    except Exception as e:
        print(f"Failed to connect to PostgreSQL database: {str(e)}")
        use_sqlite = True
else:
    print("No PostgreSQL DATABASE_URL found")
    use_sqlite = True

# Fall back to SQLite if PostgreSQL connection failed
if use_sqlite:
    print(f"Using SQLite database: {SQLITE_URL}")
    engine = create_engine(SQLITE_URL)
    Session = sessionmaker(bind=engine)

class User(Base):
    """User model for storing user information and settings."""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    settings = Column(Text, nullable=True)  # JSON-encoded settings
    
    def get_settings(self):
        """Get user settings as a dictionary."""
        if not self.settings:
            return {}
        return json.loads(self.settings)
    
    def set_settings(self, settings_dict):
        """Set user settings from a dictionary."""
        self.settings = json.dumps(settings_dict)

class UserData(Base):
    """Model for storing processed user data entries."""
    __tablename__ = 'user_data'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    source = Column(String(100), nullable=True)
    data_type = Column(String(50), nullable=True)  # e.g., "journal", "chat", "email"
    timestamp = Column(DateTime, nullable=True)
    meta_data = Column(Text, nullable=True)  # JSON-encoded metadata (renamed from metadata to avoid conflict)
    embedding = Column(LargeBinary, nullable=True)  # Pickled numpy array
    
    def get_metadata(self):
        """Get metadata as a dictionary."""
        if not self.meta_data:
            return {}
        return json.loads(self.meta_data)
    
    def set_metadata(self, metadata_dict):
        """Set metadata from a dictionary."""
        self.meta_data = json.dumps(metadata_dict)
    
    def get_embedding(self):
        """Get embedding as a numpy array."""
        if not self.embedding:
            return None
        return pickle.loads(self.embedding)
    
    def set_embedding(self, embedding_array):
        """Set embedding from a numpy array."""
        if embedding_array is not None:
            self.embedding = pickle.dumps(embedding_array)

class PersonalityProfile(Base):
    """Model for storing user personality profiles extracted from their data."""
    __tablename__ = 'personality_profiles'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Core personality attributes
    decision_style = Column(String(50), nullable=True)
    emotional_baseline = Column(String(50), nullable=True)
    language_tone = Column(String(50), nullable=True)
    
    # JSON-encoded extended attributes
    core_values = Column(Text, nullable=True)  # JSON array of values
    behavior_patterns = Column(Text, nullable=True)  # JSON object
    preferences = Column(Text, nullable=True)  # JSON object
    
    def get_core_values(self):
        """Get core values as a list."""
        if not self.core_values:
            return []
        return json.loads(self.core_values)
    
    def set_core_values(self, values_list):
        """Set core values from a list."""
        self.core_values = json.dumps(values_list)
    
    def get_behavior_patterns(self):
        """Get behavior patterns as a dictionary."""
        if not self.behavior_patterns:
            return {}
        return json.loads(self.behavior_patterns)
    
    def set_behavior_patterns(self, patterns_dict):
        """Set behavior patterns from a dictionary."""
        self.behavior_patterns = json.dumps(patterns_dict)
    
    def get_preferences(self):
        """Get preferences as a dictionary."""
        if not self.preferences:
            return {}
        return json.loads(self.preferences)
    
    def set_preferences(self, preferences_dict):
        """Set preferences from a dictionary."""
        self.preferences = json.dumps(preferences_dict)

class VectorStoreDB(Base):
    """Model for storing vector stores."""
    __tablename__ = 'vector_stores'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    index_data = Column(LargeBinary, nullable=False)  # Pickled FAISS index
    docs_metadata = Column(LargeBinary, nullable=False)  # Pickled docs and metadata
    
    def get_index_data(self):
        """Get the FAISS index data."""
        if not self.index_data:
            return None
        return pickle.loads(self.index_data)
    
    def set_index_data(self, index):
        """Set the FAISS index data."""
        if index is not None:
            self.index_data = pickle.dumps(index)
    
    def get_docs_metadata(self):
        """Get the docs and metadata as a tuple."""
        if not self.docs_metadata:
            return None
        return pickle.loads(self.docs_metadata)
    
    def set_docs_metadata(self, docs_metadata):
        """Set the docs and metadata from a tuple."""
        if docs_metadata is not None:
            self.docs_metadata = pickle.dumps(docs_metadata)

class ConversationHistory(Base):
    """Model for storing conversation history."""
    __tablename__ = 'conversation_history'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    question = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    model_used = Column(String(50), nullable=True)  # e.g., "openai", "anthropic"
    meta_data = Column(Text, nullable=True)  # JSON-encoded metadata (renamed from metadata to avoid conflict)

    def get_metadata(self):
        """Get metadata as a dictionary."""
        if not self.meta_data:
            return {}
        return json.loads(self.meta_data)
    
    def set_metadata(self, metadata_dict):
        """Set metadata from a dictionary."""
        self.meta_data = json.dumps(metadata_dict)

# Initialize database
def init_db():
    """Initialize the database by creating all tables."""
    try:
        # Make sure all tables are created
        Base.metadata.create_all(engine)
        
        # Verify the tables by trying to make a test query
        session = Session()
        try:
            # Test query to check if tables exist
            if use_sqlite:
                # For SQLite, we need to use text() to properly declare SQL expressions
                from sqlalchemy import text
                session.execute(text("SELECT 1 FROM users LIMIT 1"))
            else:
                # For PostgreSQL
                session.execute("SELECT 1 FROM users LIMIT 1")
                
            session.close()
            print("Database tables verified successfully")
        except Exception as test_error:
            print(f"Tables do not exist yet, creating them now: {str(test_error)}")
            # Force recreation of tables if they don't exist
            Base.metadata.create_all(engine)
            session.close()
            
        return True
    except Exception as e:
        print(f"Failed to initialize database: {str(e)}")
        # Only show error to user if we're not in the initial import process
        if hasattr(st, 'error'):
            st.error(f"Failed to initialize database: {str(e)}")
        return False

# User management functions
def get_or_create_user(name):
    """Get a user by name or create if not exists."""
    # Handle empty name 
    if not name:
        return None
        
    try:
        session = Session()
        user = session.query(User).filter(User.name == name).first()
        
        if not user:
            user = User(name=name)
            session.add(user)
            session.commit()
        
        result = user.id
        session.close()
        return result
    except Exception as e:
        import streamlit as st
        st.error(f"Database error in get_or_create_user: {str(e)}")
        
        # Create a fallback user ID for development/testing
        return 1

def store_user_data(user_id, processed_data, embeddings=None):
    """
    Store processed user data in the database.
    
    Args:
        user_id: The ID of the user
        processed_data: List of dictionaries with 'text' and 'metadata' fields
        embeddings: Optional list of embeddings corresponding to the texts
    """
    session = Session()
    
    for i, item in enumerate(processed_data):
        text = item['text']
        metadata = item['metadata']
        
        # Extract common metadata fields
        source = metadata.get('source')
        data_type = metadata.get('type')
        timestamp = metadata.get('timestamp')
        
        # Create user data entry
        user_data = UserData(
            user_id=user_id,
            text=text,
            source=source,
            data_type=data_type,
            timestamp=timestamp
        )
        
        # Set metadata
        user_data.set_metadata(metadata)
        
        # Set embedding if available
        if embeddings and i < len(embeddings):
            user_data.set_embedding(embeddings[i])
        
        session.add(user_data)
    
    session.commit()
    session.close()

def save_vector_store_db(user_id, vector_store):
    """
    Save a vector store to the database.
    
    Args:
        user_id: The ID of the user
        vector_store: The VectorStore object to save
    """
    session = Session()
    
    # Check if a vector store already exists for this user
    existing = session.query(VectorStoreDB).filter(VectorStoreDB.user_id == user_id).first()
    
    if existing:
        # Update existing
        existing.set_index_data(vector_store.index)
        existing.set_docs_metadata((vector_store.docs, vector_store.metadata))
        existing.updated_at = datetime.utcnow()
    else:
        # Create new
        vs_db = VectorStoreDB(user_id=user_id)
        vs_db.set_index_data(vector_store.index)
        vs_db.set_docs_metadata((vector_store.docs, vector_store.metadata))
        session.add(vs_db)
    
    session.commit()
    session.close()

def load_vector_store_db(user_id, VectorStore):
    """
    Load a vector store from the database.
    
    Args:
        user_id: The ID of the user
        VectorStore: The VectorStore class to instantiate
        
    Returns:
        A VectorStore object or None if not found
    """
    session = Session()
    vs_db = session.query(VectorStoreDB).filter(VectorStoreDB.user_id == user_id).first()
    
    if not vs_db:
        session.close()
        return None
    
    # Get data
    index = vs_db.get_index_data()
    docs, metadata = vs_db.get_docs_metadata()
    
    # Create new VectorStore instance and set its attributes
    store = VectorStore(dimension=index.d)
    store.index = index
    store.docs = docs
    store.metadata = metadata
    
    session.close()
    return store

def save_conversation(user_id, question, response, model_used=None, metadata=None):
    """
    Save a conversation to the database.
    
    Args:
        user_id: The ID of the user
        question: The user's question
        response: The AI's response
        model_used: The model used for the response
        metadata: Optional metadata dictionary
    """
    # Skip if no valid user_id
    if not user_id:
        return False
        
    try:
        session = Session()
        
        conv = ConversationHistory(
            user_id=user_id,
            question=question,
            response=response,
            model_used=model_used
        )
        
        if metadata:
            conv.set_metadata(metadata)
        
        session.add(conv)
        session.commit()
        session.close()
        return True
    except Exception as e:
        import streamlit as st
        st.error(f"Database error in save_conversation: {str(e)}")
        return False

def get_conversations(user_id, limit=10):
    """
    Get the user's recent conversations.
    
    Args:
        user_id: The ID of the user
        limit: The maximum number of conversations to retrieve
        
    Returns:
        List of ConversationHistory objects
    """
    session = Session()
    convs = session.query(ConversationHistory).filter(
        ConversationHistory.user_id == user_id
    ).order_by(ConversationHistory.timestamp.desc()).limit(limit).all()
    
    result = [(c.question, c.response, c.timestamp) for c in convs]
    session.close()
    return result

def update_personality_profile(user_id, profile_data):
    """
    Update or create a personality profile for a user.
    
    Args:
        user_id: The ID of the user
        profile_data: Dictionary of personality profile data
    """
    session = Session()
    
    # Check if a profile already exists
    profile = session.query(PersonalityProfile).filter(
        PersonalityProfile.user_id == user_id
    ).first()
    
    if not profile:
        profile = PersonalityProfile(user_id=user_id)
        session.add(profile)
    
    # Update profile with data
    if 'decision_style' in profile_data:
        profile.decision_style = profile_data['decision_style']
    if 'emotional_baseline' in profile_data:
        profile.emotional_baseline = profile_data['emotional_baseline']
    if 'language_tone' in profile_data:
        profile.language_tone = profile_data['language_tone']
    
    # Update JSON fields
    if 'core_values' in profile_data:
        profile.set_core_values(profile_data['core_values'])
    if 'behavior_patterns' in profile_data:
        profile.set_behavior_patterns(profile_data['behavior_patterns'])
    if 'preferences' in profile_data:
        profile.set_preferences(profile_data['preferences'])
    
    session.commit()
    session.close()

def get_personality_profile(user_id):
    """
    Get a user's personality profile.
    
    Args:
        user_id: The ID of the user
        
    Returns:
        Dictionary with personality profile data or None if not found
    """
    # Skip if no valid user_id
    if not user_id:
        return None
        
    try:
        session = Session()
        profile = session.query(PersonalityProfile).filter(
            PersonalityProfile.user_id == user_id
        ).first()
        
        if not profile:
            session.close()
            return None
        
        result = {
            'decision_style': profile.decision_style,
            'emotional_baseline': profile.emotional_baseline,
            'language_tone': profile.language_tone,
            'core_values': profile.get_core_values(),
            'behavior_patterns': profile.get_behavior_patterns(),
            'preferences': profile.get_preferences(),
            'created_at': profile.created_at,
            'updated_at': profile.updated_at
        }
        
        session.close()
        return result
    except Exception as e:
        import streamlit as st
        st.error(f"Database error in get_personality_profile: {str(e)}")
        return None

# Initialize database on import
init_db()