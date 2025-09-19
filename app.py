import streamlit as st
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent))

# Import page modules
from pages import resume_page, esg_dashboard, esg_stock_project, stock_forecasting
from utils import common_styles

def main():
    # Page configurationa
    st.set_page_config(
        page_title="Lydia's Portfolio",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply common styles
    common_styles.load_css()
    
    # Sidebar navigation
    st.sidebar.title("📊 Portfolio Navigation")
    
    page_selection = st.sidebar.selectbox(
        "Choose a page:",
        [
            "🏠 Resume & Portfolio",
            "📈 ESG Dashboard", 
            "🎯 ESG-Stock Correlation Analysis",
            "🔮 Stock Forecasting Models"
        ]
    )
    
    # Page routing
    if page_selection == "🏠 Resume & Portfolio":
        resume_page.show()
    elif page_selection == "📈 ESG Dashboard":
        esg_dashboard.show()
    elif page_selection == "🎯 ESG-Stock Correlation Analysis":
        esg_stock_project.show()
    elif page_selection == "🔮 Stock Forecasting Models":
        stock_forecasting.show()
    
    # Sidebar additional info
    st.sidebar.markdown("---")
    st.sidebar.markdown("*Built with Streamlit & Python*")

if __name__ == "__main__":
    main()