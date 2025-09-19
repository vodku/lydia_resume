import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import warnings
warnings.filterwarnings('ignore')

@st.cache_data
def fetch_stock_data(ticker, start_date, end_date):
    """Fetch stock data with caching"""
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date)
        return data
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None

def calculate_event_impact(stock_data, event_date, window_days=5):
    """
    Calculate the actual stock impact around an ESG event using event study methodology
    
    Parameters:
    - stock_data: DataFrame with stock price data
    - event_date: Date of the ESG event
    - window_days: Number of days before/after to analyze
    
    Returns:
    - impact_percentage: Calculated abnormal return
    - details: Dictionary with calculation details
    """
    try:
        event_date = pd.to_datetime(event_date)
        
        # Handle timezone compatibility
        if stock_data.index.tz is not None:
            if event_date.tz is None:
                event_date = event_date.tz_localize(stock_data.index.tz)
        else:
            if event_date.tz is not None:
                event_date = event_date.tz_localize(None)
        
        # Find the closest trading day to the event
        try:
            closest_idx = stock_data.index.get_indexer([event_date], method='nearest')[0]
            event_trading_date = stock_data.index[closest_idx]
        except:
            return 0.0, {"error": "Could not find trading date"}
        
        # Define event window (day before to day after the event)
        event_idx = stock_data.index.get_loc(event_trading_date)
        
        # Get prices for the event window
        if event_idx >= 1 and event_idx < len(stock_data) - 1:
            price_before = stock_data['Close'].iloc[event_idx - 1]
            price_after = stock_data['Close'].iloc[event_idx + 1]
            event_price = stock_data['Close'].iloc[event_idx]
            
            # Calculate the 2-day return around the event
            two_day_return = ((price_after - price_before) / price_before) * 100
            
            # Calculate normal volatility (30-day rolling standard deviation)
            returns = stock_data['Close'].pct_change()
            normal_volatility = returns.rolling(30).std().iloc[event_idx] * 100
            
            # If the return is significantly above normal daily volatility, attribute it to the event
            # Otherwise, it's likely just normal market noise
            if abs(two_day_return) > normal_volatility:
                impact = two_day_return
            else:
                impact = two_day_return * 0.5  # Partial attribution
            
            details = {
                "event_date": event_date.strftime('%Y-%m-%d'),
                "trading_date": event_trading_date.strftime('%Y-%m-%d'),
                "price_before": price_before,
                "event_price": event_price,
                "price_after": price_after,
                "two_day_return": two_day_return,
                "normal_volatility": normal_volatility,
                "attribution": "full" if abs(two_day_return) > normal_volatility else "partial"
            }
            
            return impact, details
        else:
            return 0.0, {"error": "Insufficient data around event date"}
            
    except Exception as e:
        return 0.0, {"error": f"Calculation error: {str(e)}"}

@st.cache_data
def fetch_stock_data(ticker, start_date, end_date):
    """Fetch stock data with caching"""
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date)
        return data
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None

def calculate_event_impact(stock_data, event_date, window_days=5):
    """
    Calculate the actual stock impact around an ESG event using event study methodology
    
    Parameters:
    - stock_data: DataFrame with stock price data
    - event_date: Date of the ESG event
    - window_days: Number of days before/after to analyze
    
    Returns:
    - impact_percentage: Calculated abnormal return
    - details: Dictionary with calculation details
    """
    try:
        event_date = pd.to_datetime(event_date)
        
        # Handle timezone compatibility
        if stock_data.index.tz is not None:
            if event_date.tz is None:
                event_date = event_date.tz_localize(stock_data.index.tz)
        else:
            if event_date.tz is not None:
                event_date = event_date.tz_localize(None)
        
        # Find the closest trading day to the event
        try:
            closest_idx = stock_data.index.get_indexer([event_date], method='nearest')[0]
            event_trading_date = stock_data.index[closest_idx]
        except:
            return 0.0, {"error": "Could not find trading date"}
        
        # Define event window (day before to day after the event)
        event_idx = stock_data.index.get_loc(event_trading_date)
        
        # Get prices for the event window
        if event_idx >= 1 and event_idx < len(stock_data) - 1:
            price_before = stock_data['Close'].iloc[event_idx - 1]
            price_after = stock_data['Close'].iloc[event_idx + 1]
            event_price = stock_data['Close'].iloc[event_idx]
            
            # Calculate the 2-day return around the event
            two_day_return = ((price_after - price_before) / price_before) * 100
            
            # Calculate normal volatility (30-day rolling standard deviation)
            returns = stock_data['Close'].pct_change()
            normal_volatility = returns.rolling(30).std().iloc[event_idx] * 100
            
            # If the return is significantly above normal daily volatility, attribute it to the event
            # Otherwise, it's likely just normal market noise
            if abs(two_day_return) > normal_volatility:
                impact = two_day_return
            else:
                impact = two_day_return * 0.5  # Partial attribution
            
            details = {
                "event_date": event_date.strftime('%Y-%m-%d'),
                "trading_date": event_trading_date.strftime('%Y-%m-%d'),
                "price_before": price_before,
                "event_price": event_price,
                "price_after": price_after,
                "two_day_return": two_day_return,
                "normal_volatility": normal_volatility,
                "attribution": "full" if abs(two_day_return) > normal_volatility else "partial"
            }
            
            return impact, details
        else:
            return 0.0, {"error": "Insufficient data around event date"}
            
    except Exception as e:
        return 0.0, {"error": f"Calculation error: {str(e)}"}

def show():
    """Display the ESG-Stock Correlation Analysis project"""
    
    st.markdown('<h1 class="main-header">📈 Telus ESG Impact on Stock Performance</h1>', unsafe_allow_html=True)
    
     
    # Navigation tabs - Fixed the tab structure
    tab1, = st.tabs(["📈 Stock Performance & ESG Events"])
    
    with tab1:
        show_stock_analysis()

def show_stock_analysis():
    """Display real stock performance with calculated ESG event impacts"""
    
    st.markdown("## 📈 **Telus Stock Performance & ESG Events Analysis**")
    
    # Fetch real Telus data
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=2*365)  # 2 years of data
        
        with st.spinner("Fetching real Telus stock data..."):
            telus_data = fetch_stock_data("T.TO", start_date, end_date)
        
        if telus_data is None or telus_data.empty:
            st.error("Unable to fetch Telus stock data. Please check your internet connection.")
            return
        
        # Get current metrics
        current_price = telus_data['Close'].iloc[-1]
        prev_price = telus_data['Close'].iloc[-2]
        daily_change = ((current_price - prev_price) / prev_price) * 100
        
        # 52-week range
        week_52_high = telus_data['High'].rolling(252).max().iloc[-1]
        week_52_low = telus_data['Low'].rolling(252).min().iloc[-1]
        
        # Display current metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Current Price", f"${current_price:.2f} CAD", f"{daily_change:+.2f}%")
        
        with col2:
            st.metric("52-Week Range", f"${week_52_low:.2f} - ${week_52_high:.2f}")
        
        with col3:
            # Market cap calculation (approximate)
            shares_outstanding = 1.5e9  # Approximate shares outstanding
            market_cap = current_price * shares_outstanding / 1e9
            st.metric("Market Cap", f"~${market_cap:.1f}B CAD")
        
        with col4:
            # Dividend yield (approximate based on recent data)
            annual_dividend = 1.66  # Approximate annual dividend
            dividend_yield = (annual_dividend / current_price) * 100
            st.metric("Dividend Yield", f"{dividend_yield:.2f}%")
        
    except Exception as e:
        st.error(f"Error processing stock data: {e}")
        return
    
    # ESG Events Data - Using verified annual ESG reporting dates (beginning of month)
    esg_events_raw = [
        {'name': '2024 ESG Data Sheet Release', 'date': '2025-05-01', 'color': 'green'},
        {'name': 'S&P Global ESG Score Update', 'date': '2025-09-01', 'color': 'blue'},
        {'name': '2023 ESG Data Sheet Release', 'date': '2024-05-01', 'color': 'green'},
        {'name': 'S&P Global ESG Score Update', 'date': '2024-09-01', 'color': 'blue'},
        {'name': '2022 ESG Data Sheet Release', 'date': '2023-05-01', 'color': 'green'}
    ]
    
    esg_events = []
    calculation_details = []
    
    for event in esg_events_raw:
        impact, details = calculate_event_impact(telus_data, event['date'])
        
        event_with_impact = event.copy()
        event_with_impact['impact'] = f"{impact:+.2f}%"
        event_with_impact['impact_value'] = impact
        esg_events.append(event_with_impact)
        calculation_details.append(details)
    
    
    fig = go.Figure()
    
    # Add real stock price line
    fig.add_trace(go.Scatter(
        x=telus_data.index,
        y=telus_data['Close'],
        mode='lines',
        name='Telus Stock Price',
        line=dict(color='#4B0F62', width=3),
        hovertemplate='Date: %{x}<br>Price: $%{y:.2f} CAD<extra></extra>'
    ))
    
    for i, event in enumerate(esg_events):
        event_date = pd.to_datetime(event['date'])
        
        # Make event_date timezone-aware to match telus_data.index
        if telus_data.index.tz is not None:
            if event_date.tz is None:
                event_date = event_date.tz_localize(telus_data.index.tz)
        
        # Convert data index to timezone-naive for comparison if needed
        data_start = telus_data.index[0]
        data_end = telus_data.index[-1]
        
        if data_start.tz is not None:
            data_start_naive = data_start.tz_localize(None)
            data_end_naive = data_end.tz_localize(None)
            event_date_naive = event_date.tz_localize(None) if event_date.tz is not None else event_date
        else:
            data_start_naive = data_start
            data_end_naive = data_end
            event_date_naive = event_date.tz_localize(None) if event_date.tz is not None else event_date
        
        # Check if event date is within our data range
        if event_date_naive >= data_start_naive and event_date_naive <= data_end_naive:
            # Find the closest trading day to the event
            try:
                closest_idx = telus_data.index.get_indexer([event_date], method='nearest')[0]
                closest_date = telus_data.index[closest_idx]
                event_price = telus_data.loc[closest_date, 'Close']
                
                # Add event marker
                fig.add_trace(go.Scatter(
                    x=[closest_date],
                    y=[event_price + 0.5],  # Slightly above the price line
                    mode='markers+text',
                    marker=dict(
                        size=25,
                        color=event['color'],
                        symbol='star',
                        line=dict(width=2, color='black')
                    ),
                    text=event['impact'],
                    textposition="top center",
                    textfont=dict(size=12, color='black'),
                    name=f"{event['name']} ({event['date']})",
                    showlegend=True,
                    hovertemplate=f"<b>{event['name']}</b><br>Date: {event['date']}<br>Calculated Impact: {event['impact']}<br>Price: $%{{y:.2f}} CAD<extra></extra>"
                ))
                
                # Add vertical line
                fig.add_vline(
                    x=closest_date,
                    line_dash="dash",
                    line_color=event['color'],
                    line_width=2,
                    opacity=0.7
                )
            except Exception as e:
                st.write(f"⚠️ Error processing {event['name']}: {e}")
        else:
            continue
    
    # Update chart layout
    fig.update_layout(
        title="Telus Stock Price with Calculated ESG Event Impacts",
        xaxis_title="Date",
        yaxis_title="Price (CAD)",
        height=600,
        showlegend=True,
        hovermode='x unified'
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
    # ESG Impact Table with calculated values
    st.markdown("### 📈 **ESG Event Impact Summary**")
    
    impact_df = pd.DataFrame({
        'ESG Event': [e['name'] for e in esg_events],
        'Date': [e['date'] for e in esg_events],
        'Stock Impact': [e['impact'] for e in esg_events],
        'Event Type': ['ESG Reporting', 'ESG Score Update', 'ESG Reporting', 'ESG Score Update', 'ESG Reporting']
    })
    
    st.dataframe(impact_df, use_container_width=True, hide_index=True)
    
    # Calculate real performance metrics
    col1, col2 = st.columns(2)
    
    with col1:
        
        st.markdown("### 📊 **Performance Metrics**")
        col1, col2 = st.columns(2)
        
        with col1:
            # Calculate actual metrics from real data
            total_return = ((telus_data['Close'].iloc[-1] - telus_data['Close'].iloc[0]) / telus_data['Close'].iloc[0]) * 100
            st.metric("Total Return (2-year)", f"{total_return:+.1f}%")
        
        with col2:
            # Real volatility calculation
            daily_returns = telus_data['Close'].pct_change().dropna()
            volatility = daily_returns.std() * np.sqrt(252) * 100
            st.metric("Annualized Volatility", f"{volatility:.1f}%")
