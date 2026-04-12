import streamlit as st
import pandas as pd
import time
import os
import json

ONLINE_LOG = 'app.log'
BASELINES_FILE = 'user_baselines.json'

st.set_page_config(
    page_title="BugBuster AIC",
    page_icon="🐛",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    .metric-card { background-color: #1E2127; padding: 15px; border-radius: 8px; border-left: 4px solid #4CAF50; }
    .metric-alert { border-left: 4px solid #F44336; background-color: #2D1A1A; }
    .alert-banner { background-color: #F44336; color: white; padding: 20px; border-radius: 8px; font-weight: bold; font-size: 20px; text-align: center; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=1) 
def load_data():
    if not os.path.exists(ONLINE_LOG):
        return pd.DataFrame()
    
    data = []
    with open(ONLINE_LOG, 'r') as f:
        for line in f:
            try:
                parts = line.strip().split(' ', 2)
                if len(parts) >= 3:
                    timestamp = f"{parts[0]} {parts[1]}"
                    log_type = "ERROR" if "ERROR:" in parts[2] else "INFO"
                    user = parts[2].split("User '")[1].split("'")[0]
                    payload = int(parts[2].split("Payload: ")[1].replace("B", ""))
                    data.append({"Timestamp": timestamp, "Type": log_type, "User": user, "Payload": payload, "Raw": line.strip()})
            except:
                pass
    return pd.DataFrame(data)

def load_baselines():
    if os.path.exists(BASELINES_FILE):
        with open(BASELINES_FILE, 'r') as f:
            return json.load(f)
    return {}



st.title("🐛 BugBuster: Anomaly Intelligence Center")
st.markdown("Real-time System Degradation & Threat Monitoring")

df = load_data()
baselines = load_baselines()

if df.empty:
    st.info("Waiting for telemetry data... Please start 'stream_online.py'.")
else:
  
    total_logs = len(df)
    unique_users = df['User'].nunique()
    
 
    recent_logs = df.tail(10)
    anomalies_detected = 0
    attacker = None
    
    for _, row in recent_logs.iterrows():
        user = row['User']
        if user in baselines:
            if row['Payload'] > baselines[user]['max_historical_payload'] * 2 or row['Type'] == 'ERROR':
                 anomalies_detected += 1
                 if row['Type'] == 'ERROR' and row['Payload'] > 5000:
                     attacker = user

  
    if attacker:
        st.markdown(f'<div class="alert-banner">🚨 CRITICAL ALERT: Brute-force & Anomalous Payload detected from user: {attacker}! 🚨</div>', unsafe_allow_html=True)


    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Logs Analyzed", value=total_logs, delta=f"+{len(recent_logs)}/sec")
    with col2:
         st.metric(label="Active Users", value=unique_users)
    with col3:
        if anomalies_detected > 0:
            st.metric(label="Security Alerts (Recent)", value=anomalies_detected, delta="High Threat", delta_color="inverse")
        else:
            st.metric(label="Security Alerts (Recent)", value=0, delta="Stable", delta_color="normal")

    st.divider()

 
    st.subheader("System Traffic & Degradation Pulse")
    

    df['Rolling_Payload'] = df['Payload'].rolling(window=5, min_periods=1).mean()
    chart_data = df.tail(40)[['Timestamp', 'Rolling_Payload']].set_index('Timestamp')
    

    chart_data['Baseline (Normal)'] = 500 
    
   
    st.line_chart(chart_data, color=["#F44336", "#4CAF50"]) 


    st.subheader("Recent Activity Feed")

    def highlight_errors(val):
        color = 'red' if val == 'ERROR' else 'green'
        return f'color: {color}'
    
    display_df = df.tail(10)[['Timestamp', 'Type', 'User', 'Payload']]
    st.dataframe(display_df.style.map(highlight_errors, subset=['Type']), width="stretch")


time.sleep(1)
st.rerun()