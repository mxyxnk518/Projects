"""
Enhanced card display function for PrePersona with micro-interaction hover effects.
"""
import streamlit as st

def simple_card(title, content, icon=None, accent_color=None):
    """
    Display content in a simple card with micro-interaction hover effects.
    
    Args:
        title: Card title
        content: HTML content for the card body
        icon: Optional icon name from Font Awesome
        accent_color: Optional accent color for the card
    """
    # Clean up any closing div tags in the content
    content = content.replace("</div>", "")
    
    # Set default accent color if none provided
    accent_color = accent_color or "#4d7cfe"
    
    # Create the HTML with minimal nesting and hover effects
    st.markdown(f"""
    <style>
    /* Card base styles */
    .interactive-card {{
        background-color: var(--bg-card, #1c2333);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 16px rgba(0,0,0,0.4);
        border-left: 4px solid {accent_color};
        position: relative;
        transition: all 0.3s ease;
        cursor: pointer;
    }}
    
    /* Card hover effects */
    .interactive-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.5);
        border-left: 6px solid {accent_color};
    }}
    
    /* Card before element for top gradient */
    .interactive-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, {accent_color}, transparent);
        opacity: 0.7;
        transition: opacity 0.3s ease, height 0.3s ease;
    }}
    
    /* Enhanced gradient on hover */
    .interactive-card:hover::before {{
        opacity: 1;
        height: 6px;
    }}
    
    /* Card title styles */
    .interactive-card-title {{
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 1.35rem;
        color: var(--text-primary, #e0e1e6);
        display: flex;
        align-items: center;
        transition: color 0.3s ease;
    }}
    
    /* Card title hover effect */
    .interactive-card:hover .interactive-card-title {{
        color: {accent_color};
    }}
    
    /* Icon styles */
    .interactive-card-title i {{
        margin-right: 0.75rem;
        color: {accent_color};
        font-size: 1.3em;
        transition: transform 0.3s ease, color 0.3s ease;
    }}
    
    /* Icon hover animation */
    .interactive-card:hover .interactive-card-title i {{
        transform: scale(1.2);
        color: lighten({accent_color}, 10%);
    }}
    
    /* Link styles within cards */
    .interactive-card a {{
        color: {accent_color};
        text-decoration: none;
        transition: color 0.3s ease;
        position: relative;
    }}
    
    /* Link hover effects */
    .interactive-card a:hover {{
        color: lighten({accent_color}, 15%);
    }}
    
    /* Card content styles */
    .interactive-card-content {{
        transition: transform 0.3s ease;
    }}
    
    /* Content subtle scale effect on hover */
    .interactive-card:hover .interactive-card-content {{
        transform: scale(1.02);
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Icon HTML if provided
    icon_html = f'<i class="fas fa-{icon}"></i>' if icon else ''
    
    # Full card HTML with interactive elements
    card_html = f"""
    <div class="interactive-card">
      <div class="interactive-card-title">{icon_html} {title}</div>
      <div class="interactive-card-content">
        {content}
      </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)