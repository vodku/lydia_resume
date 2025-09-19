import streamlit as st

def load_css():
    """Load common CSS styles for the entire application"""
    
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #4B0F62;
        text-align: center;
        margin-bottom: 2rem;
    }
    .verified-badge {
        background: linear-gradient(45deg, #00A651, #4B0F62);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        display: inline-block;
        margin: 1rem 0;
        font-weight: bold;
    }
    .real-data-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-left: 5px solid #00A651;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 10px;
    }
    .metric-highlight {
        background: #4B286D;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
    .profile-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
    }
    .skill-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .project-card {
        background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .contact-item {
        background: #e3f2fd;
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 3px solid #2196f3;
    }
    .section-header {
        font-size: 1.8rem;
        color: #2c3e50;
        border-bottom: 3px solid #3498db;
        padding-bottom: 0.5rem;
        margin: 2rem 0 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)