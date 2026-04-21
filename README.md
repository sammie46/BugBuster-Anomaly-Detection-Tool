# 🐛 BugBuster: Anomaly Detection Tool
**AmCham Hackathon 2026**


## 📖 Project Description
**BugBuster** is a proactive anomaly detection tool designed to identify system degradations and security threats in global telemetry data. 

Traditional monitoring relies on static rules that often miss subtle, gradual issues (like slow memory leaks or API latency spikes) until they cause a critical outage. BugBuster solves this by using Machine Learning to understand the "normal" global trends of a system and automatically triggering alerts when current traffic deviates from these learned baselines.

*Note: For the purpose of this hackathon demonstration, we built custom data generator scripts to simulate both normal server traffic and specific attack vectors. The core product, however, is the anomaly detection engine itself.*

## ✨ Core Capabilities
* **Dynamic ML Baselines:** Uses an Isolation Forest machine learning model to learn normal system behavior from historical logs.
* **Seasonality Awareness:** Natively understands that normal traffic differs between day and night, reducing false positive alerts during off-hours.
* **Custom Detection Algorithm:** Evaluates live logs against the ML baseline using a custom Z-score weighted formula.
* **Automated Alerting:** Dispatches real-time Slack notifications when the anomaly score exceeds critical thresholds.

## 🎯 Detected Anomalies
The tool is designed to catch three primary cases based on global system metrics:
1. **Performance Degradation:** Sudden spikes in Global API Latency and CPU Usage.
2. **Brute-Force Attacks:** Unexpected surges in the Global Error Rate (e.g., mass HTTP 401/500 errors).
3. **Payload Anomalies:** Suspiciously large data transfers (Data Exfiltration), especially during low-traffic off-hours.

## 🏗️ Project Structure

### 1. The Core Tool (Anomaly Detection Engine)
* `trend_builder.py`: The ML Engine. Analyzes historical logs and builds the statistical baseline boundaries (`trends.json`).
* `anomaly_detector.py`: The live detection script. Reads the data stream, applies the detection algorithm, and triggers Slack alerts.
* `app_ui.py`: A Streamlit dashboard for real-time visualization of system metrics and detected anomalies.

### 2. The Demo Harness (Data Simulators)
*(Used only to demonstrate the tool's capabilities without a live production environment)*
* `generate_history.py`: Generates 72 hours of mock historical telemetry with day/night seasonality.
* `stream_online.py`: Simulates a live log stream, injecting normal traffic and triggering the 3 anomaly cases for the demo.

## 🚀 How to Run the Demo Locally

### 1. Install requirements:
```bash
pip install -r requirements.txt
```

### 2. Configure Slack Webhook:
```bash
SLACK_WEBHOOK_URL="[https://hooks.slack.com/services/YOUR/WEBHOOK/HERE](https://hooks.slack.com/services/YOUR/WEBHOOK/HERE)"
```

### 3. Run the simulation (in separate terminals):

Terminal 1: Build the ML baseline from simulated history
```bash
python trend_builder.py
```

Terminal 2: Start generating the live fake traffic & attacks
```bash
python stream_online.py
```

Terminal 3: Start the actual Anomaly Detector
```bash
python anomaly_detector.py
```
Terminal 4: Launch the UI
```bash
streamlit run app_ui.py
```

