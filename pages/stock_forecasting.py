import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def show():
    """Display Telus stock forecasting with custom AutoARIMA model"""
    
    st.markdown('<h1 class="main-header">🔮 Telus Stock Price Forecasting with AutoARIMA</h1>', unsafe_allow_html=True)
    
    # Load forecast data and real stock data
    forecast_data = load_forecast_data()
    stock_data = fetch_telus_data()
    
    if forecast_data is not None and stock_data is not None:
        show_forecast_analysis(stock_data, forecast_data)
    else:
        st.error("Unable to load forecast or stock data")

@st.cache_data
def load_forecast_data():
    """Load the custom AutoARIMA forecast data"""
    try:
        # Read the forecast CSV
        forecast_df = pd.read_csv('T.TO.csv')
        forecast_df['ds'] = pd.to_datetime(forecast_df['ds'])
        return forecast_df
    except Exception as e:
        st.error(f"Error loading forecast data: {e}")
        return None

@st.cache_data
def fetch_telus_data():
    """Fetch real Telus stock data from Yahoo Finance"""
    try:
        ticker = "T.TO"
        end_date = datetime.now()
        start_date = end_date - timedelta(days=2*365)  # 2 years of data
        
        telus = yf.Ticker(ticker)
        hist = telus.history(start=start_date, end=end_date)
        
        if not hist.empty:
            return hist
        else:
            return None
            
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")
        return None

def show_forecast_analysis(stock_data, forecast_data):
    """Display the complete forecast analysis"""
    
    # Current stock metrics
    st.markdown("### 📊 **Current Telus Stock Information**")
    
    current_price = stock_data['Close'].iloc[-1]
    prev_close = stock_data['Close'].iloc[-2]
    change = current_price - prev_close
    change_pct = (change / prev_close) * 100
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Current Price", f"${current_price:.2f} CAD", f"{change_pct:+.2f}%")
    
    with col2:
        high_52w = stock_data['High'].rolling(window=252).max().iloc[-1]
        low_52w = stock_data['Low'].rolling(window=252).min().iloc[-1]
        st.metric("52W Range", f"${low_52w:.2f} - ${high_52w:.2f}")
    
    with col3:
        volume = stock_data['Volume'].iloc[-1]
        st.metric("Volume", f"{volume:,.0f}")
    
    with col4:
        market_cap = current_price * 1.5e9 / 1e9  # Approximate shares outstanding
        st.metric("Market Cap", f"~${market_cap:.1f}B CAD")
    
    # AutoARIMA Model Explanation
    st.markdown("### 🤖 **AutoARIMA Model Overview**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="skill-card">
        <h4>📈 Model Methodology</h4>
        <ul>
        <li><strong>AutoARIMA:</strong> Automatic ARIMA model selection using AIC/BIC criteria</li>
        <li><strong>Data Source:</strong> Historical Telus (T.TO) stock prices from Yahoo Finance</li>
        <li><strong>Model Selection:</strong> Optimizes parameters (p,d,q)(P, D, Q) automatically</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Main forecast visualization
    st.markdown("### 📈 **Telus Stock Price: Historical Data + AutoARIMA Forecast**")
    
    # Create the main chart
    fig = go.Figure()
    
    # Historical stock data (last 18 months for context)
    historical_data = stock_data.tail(252 + 126)  # ~18 months
    
    fig.add_trace(go.Scatter(
        x=historical_data.index,
        y=historical_data['Close'],
        mode='lines',
        name='Historical Telus Stock Price',
        line=dict(color='#4B0F62', width=3),
        hovertemplate='Date: %{x}<br>Price: $%{y:.2f} CAD<extra></extra>'
    ))
    
    # AutoARIMA forecast
    fig.add_trace(go.Scatter(
        x=forecast_data['ds'],
        y=forecast_data['AutoARIMA'],
        mode='lines',
        name='AutoARIMA Forecast',
        line=dict(color='red', width=3, dash='dash'),
        hovertemplate='Date: %{x}<br>Forecast: $%{y:.2f} CAD<extra></extra>'
    ))
    
    # Add a vertical line to separate historical and forecast
    if not forecast_data.empty:
        forecast_start = forecast_data['ds'].iloc[0]
        fig.add_vline(
            x=forecast_start.timestamp() * 1000,  # Convert to milliseconds for Plotly
            line_dash="dot",
            line_color="gray",
            annotation_text="Forecast Start",
            annotation_position="top right"
        )
    
    # Add confidence bands (approximate based on historical volatility)
    if len(forecast_data) > 0:
        # Calculate historical volatility for confidence bands
        daily_returns = stock_data['Close'].pct_change().dropna()
        volatility = daily_returns.std()
        
        # Create expanding confidence bands
        forecast_values = forecast_data['AutoARIMA'].values
        confidence_multiplier = np.sqrt(np.arange(1, len(forecast_values) + 1)) * volatility
        
        upper_band = forecast_values * (1 + 1.96 * confidence_multiplier)
        lower_band = forecast_values * (1 - 1.96 * confidence_multiplier)
        
        # Upper confidence band
        fig.add_trace(go.Scatter(
            x=forecast_data['ds'],
            y=upper_band,
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Lower confidence band with fill
        fig.add_trace(go.Scatter(
            x=forecast_data['ds'],
            y=lower_band,
            mode='lines',
            fill='tonexty',
            fillcolor='rgba(255,0,0,0.2)',
            line=dict(width=0),
            name='95% Confidence Interval',
            hoverinfo='skip'
        ))
    
    fig.update_layout(
        title="Telus (T.TO) Stock Price: Historical Data + AutoARIMA Forecast",
        xaxis_title="Date",
        yaxis_title="Price (CAD)",
        height=600,
        showlegend=True,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Forecast Analysis
    st.markdown("### 🎯 **Forecast Analysis & Insights**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📊 **Current vs Forecast**")
        
        if len(forecast_data) > 0:
            forecast_end = forecast_data['AutoARIMA'].iloc[-1]
            total_change = ((forecast_end - current_price) / current_price) * 100
            
            st.metric("Current Price", f"${current_price:.2f} CAD")
            st.metric("6-Month Target", f"${forecast_end:.2f} CAD", f"{total_change:+.1f}%")
            
    
    with col2:
        st.markdown("#### 📈 **Forecast Statistics**")
        
        if len(forecast_data) > 0:
            forecast_values = forecast_data['AutoARIMA'].values
            
            st.metric("Forecast Horizon", f"{len(forecast_data)} trading days")
            st.metric("Price Range", f"${forecast_values.min():.2f} - ${forecast_values.max():.2f}")
            st.metric("Forecast Volatility", f"${forecast_values.std():.2f}")
            
            # Trend analysis
            trend = "Upward" if forecast_values[-1] > forecast_values[0] else "Downward"
            trend_strength = abs((forecast_values[-1] - forecast_values[0]) / forecast_values[0]) * 100
            st.metric("Overall Trend", f"{trend} ({trend_strength:.1f}%)")
    
    with col3:
        st.markdown("#### 🤖 **Model Performance**")
        
        st.metric("Model Type", "AutoARIMA")
        st.metric("Fitted Model", "ARIMA(0,1,1)(0,1,0)[365]")
        st.metric("Training Data Points Used", f"752 days")
        
        # Data quality
        st.metric("MAE", "1.35 CAD")
        st.metric("MAPE", "6.1%")

    with st.expander("Show AutoARIMA Model Code"):
        st.code("""
    import yfinance as yf
    from statsforecast import StatsForecast
    from statsforecast.models import AutoARIMA
    from datetime import datetime, timedelta
    from statsmodels.graphics.tsaplots import plot_acf
    from statsmodels.graphics.tsaplots import plot_pacf
    from statsmodels.tsa.seasonal import seasonal_decompose
    from statsforecast.arima import arima_string
    from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
    import seaborn as sns
    import scipy.stats as stats

    # Collect data
    ticker = "T.TO"
            
    # Get 3 years of data for robust forecasting
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3*365)

    # Fetch data
    telus = yf.Ticker(ticker)
    hist = telus.history(start=start_date, end=end_date)

    # Prepare data for StatsForecast
    hist["unique_id"] = ticker
    hist = hist.reset_index()
    hist = hist[["Date", "Close", "unique_id"]]
    hist.columns = ["ds", "y", "unique_id"]

    # Train & Test split
    Y_train_df = hist[hist.ds<='2025-06-30'] 
    Y_test_df = hist[hist.ds>'2025-06-30']

    
    Y_train_df["ds"] = pd.to_datetime(Y_train_df["ds"])

    season_length = 365 # Daily data 
    horizon = len(Y_test_df) # number of predictions

    # Fit AutoARIMA model
    models = [AutoARIMA(season_length=season_length, D=1)]
    sf = StatsForecast(models=models, freq='D')
    sf.fit(df=Y_train_df)
    arima_string(sf.fitted_[0,0].model_)

    # Validate model on test set
    Y_hat_df_test = sf.forecast(df=Y_train_df, h=horizon, fitted=True)
        pred_col = [c for c in Y_hat_df_test.columns if c not in ('unique_id','ds') and 'lo' not in c and 'hi' not in c][0]
    eval_df = (
        Y_hat_df_test.merge(Y_test_df[['ds','y']], on='ds', how='left', suffixes=('_hat',''))
                .dropna(subset=['y'])
    )

    y_true = eval_df['y'].values
    y_pred = eval_df[pred_col].values

    # Calculate error metrics
    mae = mean_absolute_error(y_true, y_pred)
    mape = mean_absolute_percentage_error(y_true, y_pred) * 100  # sklearn returns a fraction
    print(f"MAE: {mae:.2f} CAD")
    print(f"MAPE: {mape:.2f}%")
                
    # Forecast future values
    horizon=100
    Y_hat_df = sf.forecast(df=Y_train_df, h=horizon, fitted=True)
    Y_hat_df.head())""")