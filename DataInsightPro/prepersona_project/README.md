# PrePersona - Your Digital Clone

An AI-powered digital persona platform that dynamically learns and adapts to user communication styles while maintaining robust system resilience.

## Features

- **AI-Powered Persona Generation**: Create a digital clone that learns to respond like you
- **Adaptive UI with Mood-Based Color Scheme**: Interface adapts based on detected mood
- **Data Upload**: Process various data types to train your digital clone
- **Continuous Learning**: Enhances the digital persona with each conversation
- **Robust Database System**: PostgreSQL with SQLite fallback for reliability

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables for API keys:
   - `GROQ_API_KEY` - Required for AI model access
   - `DATABASE_URL` - Optional for PostgreSQL connection

## Usage

Run the application:
```
streamlit run app.py
```

Access the application at: http://localhost:5000

## Project Structure

- `app.py` - Main application entry point
- `pages/` - Individual page components
  - `home.py` - Home page
  - `chat.py` - Chat interface
  - `query.py` - Digital clone query interface
  - `upload.py` - Data upload page
  - `profile.py` - User profile page
  - `about.py` - About page
- `utils/` - Utility modules
  - `mood_colors.py` - Adaptive color system
  - `ui_styles.py` - UI styling utilities
  - `db.py` - Database operations
  - `llm_handler.py` - AI model handling
  - `vector_store.py` - Vector database for embeddings
  - `continuous_learner.py` - Learning from conversations
  - `personality.py` - Personality profile handling
- `.streamlit/` - Streamlit configuration

## Database Setup

The application will automatically create the necessary database tables on first run. It supports:
- PostgreSQL (primary database)
- SQLite (fallback database for local development)

## Core Technologies

- Python-based personality modeling
- Machine learning personality adaptation
- Advanced error handling and database fallback mechanisms
- Multi-database support (PostgreSQL, SQLite)
- Contextual response generation with intelligent error recovery