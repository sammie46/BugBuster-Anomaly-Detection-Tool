Markdown
# 🐛 BugBuster: Anomaly Intelligence Center (AIC)

**BugBuster** is an automated, real-time telemetry analysis and anomaly detection system developed for the AmCham Hackathon 2026. 

By leveraging User and Entity Behavior Analytics (UEBA), BugBuster establishes baseline behavioral profiles for system users and proactively detects performance degradation, brute-force attacks, and payload anomalies before they cause critical system failures.

## 🎯 The Business Value
In modern enterprise environments, traditional rule-based security systems generate thousands of "false positive" alerts, causing **Alert Fatigue** for Security Operations Centers (SOC). 

BugBuster solves this by learning the *unique behavioral baseline* of every single user. 
* **Proactive, not Reactive:** We don't wait for a system crash. We detect the microscopic degradation leading up to it.
* **Zero Alert Fatigue:** By using Machine Learning (UEBA), BugBuster only alerts the team when an action statistically deviates from that specific user's historical norm.
* **Cost-Efficient:** Prevents costly enterprise downtime by catching brute-force attacks and payload spikes in their infancy.

## 🌟 Key Features
* **Historical Profiling (ML Phase):** Analyzes past logs to build individual user baselines (normal error rates, max payload sizes).
* **Real-time Monitoring:** Streams live telemetry data and compares it against established baselines.
* **Early Warning System:** Detects degradation trends (e.g., massive payload spikes, repeated failed logins) and instantly triggers a **Slack Webhook** alert to the engineering team.
* **SOC Dashboard:** A dark-themed, interactive Streamlit UI for the Security Operations Center to visualize traffic and degradation in real-time.

## 🏗️ Architecture & Microservices
The system is built with a modular approach, separating data generation, machine learning, and visualization:
1. `generate_history.py` - Synthesizes realistic historical telemetry.
2. `trend_builder.py` - Parses historical logs to build `user_baselines.json`.
3. `stream_online.py` - Simulates real-time system traffic and injects a live degradation/attack scenario.
4. `anomaly_detector.py` - The backend engine that detects baseline deviations and sends Slack alerts.
5. `app_ui.py` - The Streamlit graphical interface.

## 🚀 How to Run the Demo

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

###  2. Prepare the Environment (Train the Model)
Run these commands sequentially to generate history and build baselines:


```bash
python generate_history.py
python trend_builder.py
```

### 3. Start the Live Simulation
Open three separate terminals to visualize the full architecture:

Terminal 1 (Start the Backend Watchdog):
```bash
python anomaly_detector.py
```

Terminal 2 (Start the Dashboard):
```bash
streamlit run app_ui.py
```
Terminal 3 (Inject Live Traffic & Attack):
```bash
python stream_online.py
```
Wait 15 seconds after starting the live traffic to observe the system detect the anomaly, turn the dashboard red, and receive a Slack notification.

