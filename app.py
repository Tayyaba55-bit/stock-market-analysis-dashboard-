import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ========================
# PAGE CONFIG
# ========================
st.set_page_config(page_title="Stock Market Dashboard", layout="wide")

# ========================
# LOAD DATA
# ========================
@st.cache_data
def load_data():
    df = pd.read_csv("f:\merged_dataset.csv")  # Replace with your CSV file path
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    return df

df = load_data()

# ========================
# SIDEBAR CONTROLS
# ========================
st.sidebar.title("Dashboard Controls")
start_date = st.sidebar.date_input("Start Date", df["Date"].min())
end_date = st.sidebar.date_input("End Date", df["Date"].max())
df = df[(df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))]

show_sma20 = st.sidebar.checkbox("Show SMA 20", True)
show_sma50 = st.sidebar.checkbox("Show SMA 50", True)
show_rsi = st.sidebar.checkbox("Show RSI", True)
show_bollinger = st.sidebar.checkbox("Show Bollinger Bands", True)

# ========================
# DARK THEME CSS + White headings & KPI numbers
# ========================
st.markdown("""
<style>
body {
    background-color: #0f111a;
    color: white;
}
.block-container {
    padding: 1rem;
    background-color: #111827;
    border-radius: 10px;
}

/* KPI numbers and labels */
.stMetricLabel {
    color: white !important;
    font-weight: bold;
    font-size: 18px;
}
.stMetricValue {
    color: white !important;
    font-weight: bold;
    font-size: 24px;
}

/* Dashboard title and subheaders */
h1, h2, h3, h4, h5, h6 {
    color: white !important;
    font-weight: bold;
}

/* Raw Data Table */
.stDataFrame {
    background-color: #1e293b !important;
    color: white !important;
}

/* Sidebar adjustments */
.sidebar .block-container {
    background-color: #0f111a;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ========================
# DASHBOARD TITLE
# ========================
st.title("Stock Market Dashboard")

# ========================
# KPI CARDS (Top Metrics)
# ========================
col1, col2, col3, col4 = st.columns(4)
latest_close = df["Close"].iloc[-1]
prev_close = df["Close"].iloc[-2]
change = latest_close - prev_close
percent = (change / prev_close) * 100

col1.metric(label="Current Price", value=f"${latest_close:.2f}", delta=f"{percent:.2f}%")
col2.metric(label="Highest Price", value=f"${df['High'].max():.2f}")
col3.metric(label="Lowest Price", value=f"${df['Low'].min():.2f}")
col4.metric(label="Total Volume", value=f"{df['Volume'].sum():,.0f}")

st.markdown("---")

# ========================
# MINI CHARTS ROW 1
# ========================
st.subheader("Market Mini Charts")
c1, c2, c3, c4 = st.columns(4)

# Close Trend
fig1 = px.line(df.tail(60), x="Date", y="Close", color_discrete_sequence=["#00F5A0"])
fig1.update_layout(height=180, template="plotly_dark",
                   margin=dict(l=5,r=5,t=5,b=5),
                   plot_bgcolor="#111827", paper_bgcolor="#111827")
c1.plotly_chart(fig1, use_container_width=True)

# Volume
df["Color"] = np.where(df["Close"] > df["Open"], "Up", "Down")
fig2 = px.bar(df.tail(60), x="Date", y="Volume", color="Color",
              color_discrete_map={"Up":"#00F5A0","Down":"#FF4B4B"})
fig2.update_layout(height=180, template="plotly_dark",
                   margin=dict(l=5,r=5,t=5,b=5),
                   plot_bgcolor="#111827", paper_bgcolor="#111827")
c2.plotly_chart(fig2, use_container_width=True)

# Daily Returns
df["Returns"] = df["Close"].pct_change()
fig3 = px.area(df.tail(60), x="Date", y="Returns", color_discrete_sequence=["#3B82F6"])
fig3.update_layout(height=180, template="plotly_dark",
                   margin=dict(l=5,r=5,t=5,b=5),
                   plot_bgcolor="#111827", paper_bgcolor="#111827")
c3.plotly_chart(fig3, use_container_width=True)

# Daily Range
df["Range"] = df["High"] - df["Low"]
fig4 = px.line(df.tail(60), x="Date", y="Range", color_discrete_sequence=["#FACC15"])
fig4.update_layout(height=180, template="plotly_dark",
                   margin=dict(l=5,r=5,t=5,b=5),
                   plot_bgcolor="#111827", paper_bgcolor="#111827")
c4.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ========================
# MINI CHARTS ROW 2 (Technical Indicators)
# ========================
st.subheader("Technical Indicators")
c5, c6, c7, c8 = st.columns(4)

# SMA20 Trend
df["SMA20"] = df["Close"].rolling(20).mean()
fig5 = px.line(df.tail(60), x="Date", y="SMA20", color_discrete_sequence=["#FACC15"])
fig5.update_layout(height=180, template="plotly_dark",
                   margin=dict(l=5,r=5,t=5,b=5),
                   plot_bgcolor="#111827", paper_bgcolor="#111827")
c5.plotly_chart(fig5, use_container_width=True)

# SMA50 Trend
df["SMA50"] = df["Close"].rolling(50).mean()
fig6 = px.line(df.tail(60), x="Date", y="SMA50", color_discrete_sequence=["#3B82F6"])
fig6.update_layout(height=180, template="plotly_dark",
                   margin=dict(l=5,r=5,t=5,b=5),
                   plot_bgcolor="#111827", paper_bgcolor="#111827")
c6.plotly_chart(fig6, use_container_width=True)

# High-Low Spread
df["Spread"] = df["High"] - df["Low"]
fig7 = px.area(df.tail(60), x="Date", y="Spread", color_discrete_sequence=["#FF00FF"])
fig7.update_layout(height=180, template="plotly_dark",
                   margin=dict(l=5,r=5,t=5,b=5),
                   plot_bgcolor="#111827", paper_bgcolor="#111827")
c7.plotly_chart(fig7, use_container_width=True)

# Volatility
df["Volatility"] = df["Close"].rolling(10).std()
fig8 = px.line(df.tail(60), x="Date", y="Volatility", color_discrete_sequence=["#00FFFF"])
fig8.update_layout(height=180, template="plotly_dark",
                   margin=dict(l=5,r=5,t=5,b=5),
                   plot_bgcolor="#111827", paper_bgcolor="#111827")
c8.plotly_chart(fig8, use_container_width=True)

st.markdown("---")

# ========================
# MAIN PRICE CHART
# ========================
st.subheader("Main Price Chart")
fig = go.Figure()
fig.add_trace(go.Candlestick(
    x=df["Date"], open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"],
    increasing_line_color="#00F5A0", decreasing_line_color="#FF4B4B"
))

# Bollinger Bands
if show_bollinger:
    df["STD"] = df["Close"].rolling(20).std()
    df["Upper"] = df["SMA20"] + 2*df["STD"]
    df["Lower"] = df["SMA20"] - 2*df["STD"]
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Upper"], line=dict(color="gray", dash="dot"), name="Upper Band"))
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Lower"], line=dict(color="gray", dash="dot"), name="Lower Band"))

fig.update_layout(height=400, template="plotly_dark",
                  margin=dict(l=5,r=5,t=5,b=5),
                  plot_bgcolor="#111827", paper_bgcolor="#111827")
st.plotly_chart(fig, use_container_width=True)

# ========================
# RSI CHART
# ========================
if show_rsi:
    st.subheader("RSI Chart")
    delta = df["Close"].diff()
    gain = (delta.where(delta>0,0)).rolling(14).mean()
    loss = (-delta.where(delta<0,0)).rolling(14).mean()
    rs = gain/loss
    df["RSI"] = 100 - (100/(1+rs))
    rsi_fig = px.line(df, x="Date", y="RSI", color_discrete_sequence=["#FF00FF"])
    rsi_fig.add_hline(y=70, line_dash="dash", line_color="red")
    rsi_fig.add_hline(y=30, line_dash="dash", line_color="green")
    rsi_fig.update_layout(height=250, template="plotly_dark",
                          margin=dict(l=5,r=5,t=5,b=5),
                          plot_bgcolor="#111827", paper_bgcolor="#111827")
    st.plotly_chart(rsi_fig, use_container_width=True)

st.markdown("---")

# ========================
# RAW DATA TABLE
# ========================
st.subheader("Raw Data (Last 200 rows)")
st.dataframe(df.tail(200).style.set_properties(**{
    'background-color': '#1e293b',
    'color': 'white'
}))






