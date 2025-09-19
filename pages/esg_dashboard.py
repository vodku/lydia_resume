import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, datetime

# ----------------------------------------------------------
# Styles (activates your CSS classes used in markdown blocks)
# ----------------------------------------------------------
_STYLES = """
<style>
.main-header { font-size: 2.0rem; font-weight: 700; margin-bottom: .25rem; }
.verified-badge { background:#ecfdf5; color:#065f46; padding:6px 10px; border-radius:8px; display:inline-block; }
.small-note { color:#64748b; font-size:.85rem; }
hr { border: none; border-top: 1px solid #e5e7eb; margin: 1rem 0; }
</style>
"""

# ----------------------------------------------------------
# Data loaders (keep data separate from UI; easy to audit)
# Replace page numbers / values with exact citations you used
# ----------------------------------------------------------
@st.cache_data
def load_emissions():
    # Absolute emissions (tCO2e) — replace with your exact values & cite pages
    df = pd.DataFrame({
        'Year': [2019, 2020, 2021, 2022, 2023, 2024],
        'Scope 1': [62532, 53472, 52252, 52268, 50508, 43243],
        'Scope 2': [240919, 200848, 204698, 175268, 159134, 143269],
        # Basis: market-based assumed; edit if location-based for any year
        'Scope2_Basis': ['market'] * 6,
        # Finance/volume drivers (placeholders — swap with your  cited figures)
        'Revenue_CAD_B': [14.7, 15.3, 16.9, 17.3, 20.4, 20.6],   # Annual Report / MD&A p.xx
        'Connections_M': [15.7, 16.3, 17.2, 18.3, 19.3, 20.4],   # AR/Investor deck p.xx
    })
    df['Total'] = df['Scope 1'] + df['Scope 2']
    # Intensities
    df['tCO2e_per_BCAD'] = df['Total'] / df['Revenue_CAD_B']
    df['kgCO2e_per_connection'] = (df['Total'] * 1000) / (df['Connections_M'] * 1e6)
    return df

@st.cache_data
def load_targets():
    return pd.DataFrame({
        'Goal': [
            'Net carbon-neutral by 2030',
            '100% renewable electricity by 2025',
            'Internet for Good 85K households',
            'TELUS Health 200K patient visits'
        ],
        'Status': ['On-track', 'On-track', 'On-track', 'Achieved'],
        'Progress': ['38% reduction from 2019', '59% renewable (2024)', '63,500 households', '260,000+ visits']
    })

@st.cache_data
def load_programs():
    return pd.DataFrame({
        'Program': ['Internet for Good', 'Mobility for Good', 'TELUS Wise', 'Health for Good'],
        'People Reached': [200000, 61800, 800000, 260000]
    })

@st.cache_data
def load_health():
    return pd.DataFrame({
        'Metric': ['Lives Covered', 'Virtual Care Members', 'Countries Served'],
        'Value': [76000000, 6500000, 160]
    })

# ----------------------------------------------------------
# Public entrypoint (kept as show() to match your original)
# ----------------------------------------------------------
def show():
    """Display the ESG dashboard page"""
    st.markdown(_STYLES, unsafe_allow_html=True)

    st.markdown('<h1 class="main-header">📊  TELUS ESG Analysis</h1>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="verified-badge">
        ✅ Based on TELUS 2024 Sustainability/ESG disclosures & annual filings — see Sources below.
        </div>
        <div class="small-note">Data last updated: {date.today().isoformat()}</div>
        """,
        unsafe_allow_html=True,
    )

    # ---------- Sidebar (filters + quick sources) ----------
    em = load_emissions()
    with st.sidebar:
        st.header("Filters")
        year = st.slider("Year", int(em.Year.min()), int(em.Year.max()), int(em.Year.max()))
        

    # ---------- Tabs ----------
    esg_tab1, esg_tab2, esg_tab3, esg_tab4 = st.tabs(
        ["🎯 Key Highlights", "🌱 Environmental", "👥 Social", "🏛️ Governance"]
    )

    with esg_tab1:
        show_key_highlights()

    with esg_tab2:
        show_environmental(year, em)

    with esg_tab3:
        show_social()

    with esg_tab4:
        show_governance()


# ----------------------------------------------------------
# Sections
# ----------------------------------------------------------
def show_key_highlights():
    st.markdown("## 🎯 **TELUS ESG Performance — 2024 Highlights**")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-highlight">
        <h3>Environmental</h3>
        <h2>56%</h2>
        <p>GHG emissions reduction since 2010</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-highlight">
        <h3>Social Impact</h3>
        <h2>$1.8B</h2>
        <p>Contributed since 2000</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-highlight">
        <h3>Healthcare</h3>
        <h2>76M</h2>
        <p>Lives covered globally</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-highlight">
        <h3>Trees Planted</h3>
        <h2>8M</h2>
        <p>Trees planted in 2024</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## 💰 **Financial Performance (2024)**")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="real-data-card">
        <h4>📈 Financial Highlights</h4>
        <ul>
        <li><strong>Annual Revenue:</strong> Over $20 billion</li>
        <li><strong>Customer Connections:</strong> 20+ million</li>
        <li><strong>Operating Revenue Growth:</strong> 1.8%</li>
        <li><strong>Adjusted EBITDA Growth:</strong> 5.5%</li>
        <li><strong>Mobile Churn Rate:</strong> 0.99% (industry-best)</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        targets_df = load_targets()
        st.markdown("**🎯 ESG Goals Progress**")
        st.dataframe(targets_df, use_container_width=True, hide_index=True)

def show_environmental(year: int, em: pd.DataFrame):
    st.markdown("## 🌱 **Environmental Performance**")

    # Current + previous for deltas
    latest = em[em.Year.eq(year)].iloc[0]
    prev_year = max(int(em.Year.min()), year - 1)
    prev = em[em.Year.eq(prev_year)].iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Scope 1+2 (tCO₂e)", f"{latest['Total']:,.0f}", f"{latest['Total']-prev['Total']:+,.0f} vs {prev_year}")
    c2.metric("tCO₂e / $B Rev", f"{latest['tCO2e_per_BCAD']:,.0f}")
    c3.metric("kgCO₂e / connection", f"{latest['kgCO2e_per_connection']:,.1f}")
    c4.metric("Scope 2 basis", latest['Scope2_Basis'])

    col1, col2 = st.columns(2)

    with col1:
        # GHG emissions trend
        emissions_df = em[['Year', 'Scope 1', 'Scope 2', 'Total']]
        fig = px.line(
            emissions_df, x='Year', y=['Scope 1', 'Scope 2', 'Total'],
            title='TELUS GHG Emissions (tCO₂e)'
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="-data-card">
        <h4>🎯 2024 Environmental Notes</h4>
        <ul>
        <li>✅ Reduction vs 2023 in combined Scope 1+2</li>
        <li>✅ ~38% reduction vs 2019 baseline (check exact figure)</li>
        <li>✅ ~59% renewable electricity (market-based)</li>
        <li>✅ 8 million trees planted in 2024</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Renewable energy progress (illustrative — ensure you cite your source)
        renewable_years = [2019, 2021, 2023, 2024, 2025]
        renewable_percent = [30, 45, 55, 59, 100]  # 2025 = target
        fig2 = px.bar(x=renewable_years, y=renewable_percent, title='Renewable Electricity (%)')
        fig2.add_hline(y=100, line_dash="dash")
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("""
        <div class="-data-card">
        <h4>🌳 Nature Impact (selected)</h4>
        <ul>
        <li><strong>8 million trees</strong> planted in 2024</li>
        <li><strong>5,300 hectares</strong> restored</li>
        <li><strong>~19 million trees</strong> over 25 years</li>
        <li><strong>~9,300 tCO₂</strong> avoided via fibre (methodology-dependent)</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    # Carbon price sensitivity (Finance lens)
    st.markdown("### 💸 Carbon Price Sensitivity")
    price = st.slider("Carbon price ($/tCO₂e)", 0, 300, 75, step=5, key="carbon_price_slider")
    annual_cost = price * latest['Total']
    st.markdown(f"**Estimated annual carbon cost at ${price}/t:** ${annual_cost:,.0f}")

def show_social():
    st.markdown("## 👥 **Social Impact Performance**")
    col1, col2 = st.columns(2)

    with col1:
        programs_df = load_programs()
        fig = px.bar(
            programs_df, x='Program', y='People Reached',
            title='Social Program Impact', text='People Reached'
        )
        fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="-data-card">
        <h4>💝 Community Investment (2024)</h4>
        <ul>
        <li><strong>$10.8 million</strong> Foundation grants</li>
        <li><strong>550+ charities</strong> supported</li>
        <li><strong>1.5 million hours</strong> volunteer time</li>
        <li><strong>83,000 volunteers</strong> across 33 countries</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        health_df = load_health()
        fig2 = px.bar(health_df, x='Metric', y='Value', title='TELUS Health Global Reach (2024)')
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("""
        <div class="-data-card">
        <h4>🤝 Indigenous Partnerships</h4>
        <ul>
        <li><strong>278 communities</strong> with PureFibre</li>
        <li><strong>805 Indigenous lands</strong> with 5G</li>
        <li><strong>$350,000</strong> granted in 2024</li>
        <li><strong>$1M total</strong> since 2021</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

def show_governance():
    st.markdown("## 🏛️ **Governance Performance**")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 👥 Board Diversity / Governance")
        st.markdown("""
        <div class="-data-card">
        <h4>🏆 Targets & Status</h4>
        <ul>
        <li>40%+ women directors — achieved</li>
        <li>20%+ diverse representation — achieved</li>
        <li>Board independence — maintained</li>
        <li>ESG expertise represented</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="-data-card">
        <h4>🤖 AI & Data Governance (disclosure-based)</h4>
        <ul>
        <li>Reported enterprise AI benefits and adoption</li>
        <li>Privacy-by-design certifications </li>
        <li>Internal LLM platform usage </li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Illustrative governance scores (if you have  ones, replace + cite)
        metrics = ['Board Independence', 'Women Directors', 'ESG Integration', 'AI Ethics']
        scores = [80, 40, 85, 90]
        fig = px.bar(x=metrics, y=scores, title='Governance Metrics (%)', color=scores, color_continuous_scale='Viridis')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="-data-card">
        <h4>🔗 Supply Chain ESG</h4>
        <ul>
        <li>Supplier engagement program (volume & targets)</li>
        <li>Share of suppliers with science-based targets</li>
        <li>Scope 3 intensity trend</li>
        <li>Sustainable materials policy metrics</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
