# PrePersona - Digital Clone AI

## Overview

PrePersona is an AI-powered digital clone application that learns how users think, communicate, and make decisions. Built with Streamlit, it creates personalized AI models based on user data that can predict how users would respond to new situations. The application uses vector embeddings and personality profiling to create authentic digital representations of users.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit with multi-page application structure
- **UI System**: Dark mode theming with mood-based color adaptation
- **Page Structure**: Modular page design with shared navigation
- **State Management**: Streamlit session state for user data and settings
- **Styling**: Custom CSS with responsive design and micro-interactions

### Backend Architecture
- **Database Layer**: SQLAlchemy ORM with PostgreSQL primary and SQLite fallback
- **AI Integration**: Groq API for LLM services with multiple model support
- **Vector Storage**: FAISS for semantic search and document embeddings
- **Data Processing**: Multi-format file processing pipeline
- **Learning System**: Continuous learning from user interactions

### Data Storage Solutions
- **Primary Database**: PostgreSQL with connection pooling and SSL support
- **Fallback Database**: SQLite for development and offline use
- **Vector Database**: FAISS-based in-memory vector store with persistence
- **File Storage**: Temporary file handling for uploads and processing

## Key Components

### User Management System
- User creation and authentication
- Personality profile storage and updates
- Conversation history tracking
- Settings and preferences management

### Data Processing Pipeline
- Multi-format file upload support (TXT, JSON, CSV, MD)
- Text extraction and cleaning
- Metadata preservation and enrichment
- Batch processing capabilities

### Vector Embedding System
- Document chunking and embedding generation
- Semantic similarity search
- Context retrieval for personalized responses
- Metadata-based filtering

### Personality Analysis Engine
- AI-powered personality extraction from user data
- Behavioral pattern recognition
- Communication style analysis
- Continuous profile updates from conversations

### LLM Integration Layer
- Groq API integration with multiple model support
- Dynamic prompt generation based on user personality
- Context-aware response generation
- Temperature and parameter optimization

### Continuous Learning System
- Real-time learning from user interactions
- Personality profile updates based on conversation patterns
- Conversation history analysis
- Adaptive response improvement

## Data Flow

1. **Data Ingestion**: Users upload personal data files (journals, chats, notes)
2. **Processing**: Files are parsed, cleaned, and converted to structured format
3. **Embedding**: Text data is converted to vector embeddings using AI models
4. **Storage**: Embeddings stored in FAISS index, metadata in database
5. **Personality Extraction**: AI analyzes data to create personality profile
6. **Query Processing**: User questions trigger similarity search in vector store
7. **Context Retrieval**: Relevant personal data retrieved based on query
8. **Response Generation**: LLM generates personalized response using context
9. **Learning**: System learns from interaction to improve future responses

## External Dependencies

### AI Services
- **Groq API**: Primary LLM service for text generation and analysis
- **Models Supported**: llama3-70b-8192, mixtral-8x7b-32768, gemma-7b-it

### Database Services
- **PostgreSQL**: Production database with SSL connection support
- **SQLite**: Development and fallback database

### Python Libraries
- **Streamlit**: Web application framework
- **SQLAlchemy**: Database ORM and connection management
- **FAISS**: Vector similarity search and indexing
- **LangChain**: LLM orchestration and prompt management
- **NumPy**: Numerical operations for embeddings
- **Pandas**: Data manipulation and analysis

### Infrastructure
- **Environment Variables**: API keys and database URLs
- **File System**: Temporary file storage for uploads
- **Session Management**: Streamlit session state for user data

## Deployment Strategy

### Environment Setup
- **API Keys**: Groq API key required for AI functionality
- **Database**: PostgreSQL connection via DATABASE_URL environment variable
- **Fallback**: Automatic SQLite fallback for development environments

### Application Structure
- **Entry Point**: `app.py` serves as main application file
- **Page Routing**: Multi-page Streamlit application with navigation
- **Utility Modules**: Shared functionality in `utils/` directory
- **Asset Management**: Static assets and documentation in dedicated folders

### Configuration Management
- **Database Initialization**: Automatic table creation and migration
- **Session Persistence**: User data and settings maintained across sessions
- **Error Handling**: Graceful degradation with informative error messages
- **Performance**: Caching and optimization for vector operations

### Security Considerations
- **API Key Protection**: Secure handling of sensitive credentials
- **Data Privacy**: Local processing with optional cloud AI services
- **Database Security**: Connection encryption and parameterized queries
- **Input Validation**: File type and content validation for uploads