import streamlit as st
import yfinance as yf
import plotly.graph_objs as go

# Set the page configuration
st.set_page_config(page_title="Stock Price Tracker", page_icon="📉", layout="wide")

# Custom CSS for Dark Mode
st.markdown(
    """
    <style>
    /* General App Background */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    /* Title Styles */
    .title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 20px;
    }
    /* Sidebar Customization */
    .stSidebar {
        background-color: #262730;
        color: #ffffff;
    }
    .stSidebar select {
        background-color: #1f1f1f;
        border: 1px solid #ffffff;
        color: #ffffff;
    }
    /* Buttons */
    .stDownloadButton button {
        background-color: #1f77b4;
        color: #ffffff;
        border-radius: 5px;
        padding: 10px;
        font-size: 1rem;
        margin-top: 10px;
    }
    .stDownloadButton button:hover {
        background-color: #155a91;
    }
    /* Data Table */
    .dataframe {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title Section
st.markdown('<div class="title">Stock Price Tracker 📉</div>', unsafe_allow_html=True)

# Sidebar for stock selection
st.sidebar.header("Select Stock Options")
available_symbols = [
    "AAPL", "TSLA", "GOOGL", "AMZN", "MSFT", "NFLX", "META", "NVDA", "AMD", "INTC", 
    "BA", "JPM", "WMT", "DIS", "PEP", "KO", "NKE", "V", "MA", "PFE", "MRNA", "UBER", 
    "LYFT", "SQ", "SHOP", "ZM", "ADBE", "ORCL", "CRM", "TSM", "XOM", "CVX", "SPCE", 
    "PLTR", "PYPL"
]
selected_stock = st.sidebar.selectbox("Choose a Stock:", available_symbols)

# Period and Interval
st.sidebar.markdown("**Customize Data Period and Interval**")
period = st.sidebar.selectbox("Select Period:", ["1d", "5d", "1mo", "3mo", "6mo", "1y", "5y", "max"], index=2)
interval = st.sidebar.selectbox("Select Interval:", ["1m", "5m", "15m", "1h", "1d", "1wk", "1mo"], index=4)

# Fetch and display stock data
if selected_stock:
    st.subheader(f"Selected Stock: **{selected_stock}**")

    # Fetch stock data
    stock = yf.Ticker(selected_stock)
    data = stock.history(period=period, interval=interval)

    if not data.empty:
        # Display stock price
        st.write(f"📊 **Latest Close Price:** ${data['Close'].iloc[-1]:.2f}")

        # Create and display chart
        fig = go.Figure(data=[go.Scatter(x=data.index, y=data["Close"], mode="lines", name="Close Price")])
        fig.update_layout(
            title={
                "text": f"<b>{selected_stock} Stock Price Over Time</b>",
                "x": 0.5,
                "xanchor": "center",
                "font": {"size": 20},
            },
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            template="plotly_dark",  # Apply Plotly dark theme
        )
        st.plotly_chart(fig, use_container_width=True)

        # Display data table
        st.write("📄 **Stock Data Table:**")
        st.dataframe(data.style.set_properties(**{'background-color': '#1e1e1e', 'color': 'white'}), use_container_width=True)

        # Download CSV button
        csv_data = data.to_csv().encode("utf-8")
        st.download_button(
            label="Download Data as CSV",
            data=csv_data,
            file_name=f"{selected_stock}_stock_data.csv",
            mime="text/csv",
        )
    else:
        st.error("No data available for the selected stock.")
