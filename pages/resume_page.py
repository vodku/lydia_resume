import streamlit as st
import plotly.graph_objects as go
from pathlib import Path
from io import BytesIO

def qrcode_image(data: str):
    try:
        import qrcode
        img = qrcode.make(data)
        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return buf
    except Exception:
        return None

def ensure_https(url: str) -> str:
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return "https://" + url

def show():
    """Display the resume page"""
    
    st.markdown('<h1 class="main-header">Lydia Hiba Alili</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #7f8c8d;">Junior Data Scientist - Finance</h2>', unsafe_allow_html=True)
    
    # Resume Navigation
    resume_section = st.selectbox(
        "Jump to Section:",
        ["📋 Profile Overview", "🎓 Education", "💼 Experience", "🛠️ Skills"]
    )
    
    if resume_section == "📋 Profile Overview":
        show_profile_overview()
    elif resume_section == "💼 Experience":
        show_experience()
    elif resume_section == "🛠️ Skills":
        show_skills()
    elif resume_section == "🎓 Education":
        show_education()

def show_profile_overview():
    """Display comprehensive profile overview with all information"""
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        img_path = Path("./img/profile.png")
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)
        
        # LinkedIn QR code
        linkedin = "https://www.linkedin.com/in/hiba-lydia-alili"
        qr = qrcode_image(linkedin)
        if qr:
            st.image(qr, use_container_width=True)
        
    with col2:
        st.markdown('<h3 class="section-header">🎯 Professional Summary</h3>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="skill-card">
        <p style="font-size: 1.1rem; line-height: 1.6;">
        Motivated and fast-learning developer currently skilling up in frontend development through hands-on experience building a Sales Agent application using Next.js and React. Strong foundation in data visualization, Python, and clean UI design from data science projects. Passionate about crafting responsive, intuitive interfaces and eager to grow in a collaborative, product-focused team. Currently building full-stack features including dynamic routing, API integration, and state management.
        </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Education Section
        st.markdown('<h3 class="section-header">🎓 Education</h3>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="skill-card">
        <h4>🎓 Bachelor's Degree | Simplon.co</h4>
        <p><strong>Paris, France</strong> | <em>2020 - 2021</em></p>
        <p>Data Science & Web Development (Partnership with Microsoft)</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="skill-card">
        <h4>🎓 Master's Degree | University of Lille 2</h4>
        <p><strong>Lille, France</strong> | <em>2017 - 2019</em></p>
        <p>Banking and Finance</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Professional Experience Section
        st.markdown('<h3 class="section-header">💼 Professional Experience</h3>', unsafe_allow_html=True)

        st.markdown("""
        <div class="skill-card">
        <h4>📊 Process Automation Specialist | Mirai Consulting</h4>
        <p><strong>Burnaby, British Columbia </strong> | <em>July 2025 - Today</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="skill-card">
        <h4>📊 Data Scientist | Opscidia</h4>
        <p><strong>Paris, France</strong> | <em>November 2020 - January 2022</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="skill-card">
        <h4>💼 Financial Analyst Intern | KPMG</h4>
        <p><strong>Algiers, Algeria</strong> | <em>March 2019 - August 2019</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="skill-card">
        <h4>📋 Tax Analyst Intern | PwC</h4>
        <p><strong>Algiers, Algeria</strong> | <em>March 2018 - August 2018</em></p>
        </div>
        """, unsafe_allow_html=True)

def show_experience():
    """Display simplified experience section"""
    
    st.markdown('<h2 class="section-header">💼 Professional Experience</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="skill-card">
    <h3>📊 Data Scientist | Opscidia</h3>
    <p><strong>Paris, France</strong> | <em>November 2020 - January 2022</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="skill-card">
    <h3>💼 Financial Analyst Intern | KPMG</h3>
    <p><strong>Algiers, Algeria</strong> | <em>March 2019 - August 2019</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="skill-card">
    <h3>📋 Tax Analyst Intern | PwC</h3>
    <p><strong>Algiers, Algeria</strong> | <em>March 2018 - August 2018</em></p>
    </div>
    """, unsafe_allow_html=True)

def show_skills():
    """Display skills section"""
    
    st.markdown('<h2 class="section-header">🛠️ Technical Skills</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    skill_categories = {
        "💻 Programming & Data Science": {
            'Python': 95, 'SQL': 50, 'R': 50
        },
        "📊 Data Analysis & ML": {
            'Pandas/NumPy': 95, 'Scikit-learn': 90, 'Statistical Analysis': 60, 
            'Feature Engineering': 60, 'Time Series Analysis': 50, 
            'NLP': 70
        },
        "📈 Visualization & Apps": {
            'Plotly/Dash': 92, 'Streamlit': 90, 'Matplotlib/Seaborn': 85, 
        }
    }
    
    def get_skill_badge_color(level):
        """Get color for skill level"""
        if level >= 90:
            return "#27ae60"  # Green
        elif level >= 80:
            return "#3498db"  # Blue
        elif level >= 70:
            return "#f39c12"  # Orange
        else:
            return "#95a5a6"  # Gray
    
    categories_list = list(skill_categories.items())
    
    # Distribute categories across 3 columns
    for i, (category, skills) in enumerate(categories_list):
        if i % 3 == 0:
            col = col1
        elif i % 3 == 1:
            col = col2
        else:
            col = col3
            
        with col:
            st.markdown(f"### {category}")
            
            for skill, level in skills.items():
                color = get_skill_badge_color(level)
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, {color}20, {color}10);
                    border: 2px solid {color};
                    border-radius: 10px;
                    padding: 8px 12px;
                    margin: 8px 0;
                    text-align: center;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <strong style="color: {color};">{skill}</strong><br>
                    <span style="font-size: 0.9em;">{"●" * (level // 20)}</span>
                </div>
                """, unsafe_allow_html=True)

def show_education():
    """Display simplified education section"""
    
    st.markdown('<h2 class="section-header">🎓 Education</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="skill-card">
    <h3>🎓 Bachelor's Degree | Simplon.co</h3>
    <p><strong>Paris, France</strong> | <em>2020 - 2021</em></p>
    <p>Data Science & Web Development (Partnership with Microsoft)</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="skill-card">
    <h3>🎓 Master's Degree | University of Lille 2</h3>
    <p><strong>Lille, France</strong> | <em>2017 - 2019</em></p>
    <p>Banking and Finance</p>
    </div>
    """, unsafe_allow_html=True)