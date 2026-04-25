import streamlit as st
import pandas as pd
import time
import os
import json

ONLINE_LOG = 'data/online_data.log'
TRENDS_FILE = 'data/trends.json'

st.set_page_config(
    page_title="BugBuster AIC",
    page_icon="🐛",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    .alert-banner { background-color: #F44336; color: white; padding: 20px; border-radius: 8px; font-weight: bold; font-size: 20px; text-align: center; margin-bottom: 20px;}
    .normal-banner { background-color: #4CAF50; color: white; padding: 10px; border-radius: 8px; font-weight: bold; font-size: 16px; text-align: center; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=1) 
def load_data():
    if not os.path.exists(ONLINE_LOG):
        return pd.DataFrame()
    try:
       
        df = pd.read_csv(ONLINE_LOG, names=["Timestamp", "Latency", "CPU", "ErrorRate", "Payload"])
        return df
    except:
        return pd.DataFrame()

def load_trends():
    if os.path.exists(TRENDS_FILE):
        with open(TRENDS_FILE, 'r') as f:
            return json.load(f)
    return {}

st.title("🐛 BugBuster: Anomaly Intelligence Center")
st.markdown("Real-time ML Global System Degradation & Threat Monitoring")

df = load_data()
trends = load_trends()

if df.empty:
    st.info("Waiting for telemetry data... Please run 'python stream_online.py'.")
else:
    
    latest = df.iloc[-1]
    

    alert_msg = ""
    is_anomaly = False
    
    if latest['Latency'] > 1000 or latest['CPU'] > 85:
        is_anomaly = True
        alert_msg = f"🚨 CRITICAL ALERT: Performance Degradation! (Latency: {latest['Latency']}ms, CPU: {latest['CPU']}%)"
    elif latest['ErrorRate'] > 15:
        is_anomaly = True
        alert_msg = f"🚨 CRITICAL ALERT: Distributed Brute-Force Detected! (Error Rate: {latest['ErrorRate']}%)"
    elif latest['Payload'] > 2000:
        is_anomaly = True
        alert_msg = f"🚨 CRITICAL ALERT: Payload Anomaly / Data Exfiltration! (Payload: {latest['Payload']}KB)"

    if is_anomaly:
        st.markdown(f'<div class="alert-banner">{alert_msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="normal-banner">✅ System operates within normal ML baselines</div>', unsafe_allow_html=True)

   
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Global API Latency", value=f"{latest['Latency']} ms", delta="Spike" if latest['Latency'] > 1000 else "Normal", delta_color="inverse" if latest['Latency'] > 1000 else "normal")
    with col2:
        st.metric(label="CPU Usage", value=f"{latest['CPU']} %", delta="High Load" if latest['CPU'] > 85 else "Normal", delta_color="inverse" if latest['CPU'] > 85 else "normal")
    with col3:
        st.metric(label="Global Error Rate", value=f"{latest['ErrorRate']} %", delta="Attack Suspected" if latest['ErrorRate'] > 15 else "Stable", delta_color="inverse" if latest['ErrorRate'] > 15 else "normal")
    with col4:
        st.metric(label="Avg Payload", value=f"{latest['Payload']} KB", delta="Exfiltration" if latest['Payload'] > 2000 else "Normal", delta_color="inverse" if latest['Payload'] > 2000 else "normal")

    st.divider()

 
    st.subheader("System Degradation Pulse (Real-time)")
    
    chart_data = df.tail(50).copy()
    chart_data = chart_data.set_index('Timestamp')
    
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.markdown("**API Latency (ms)**")
        st.line_chart(chart_data['Latency'], color="#F44336")
    with col_chart2:
        st.markdown("**CPU Usage (%)**")
        st.line_chart(chart_data['CPU'], color="#4CAF50")

   
    st.subheader("Recent Activity Feed")
    display_df = df.tail(10).sort_index(ascending=False)
    st.dataframe(display_df, width="stretch")

time.sleep(1)
st.rerun()