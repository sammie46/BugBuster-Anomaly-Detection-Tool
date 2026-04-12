import time
import os
import json
import urllib.request
from dotenv import load_dotenv


load_dotenv()

ONLINE_LOG = 'app.log'
BASELINES_FILE = 'user_baselines.json'


SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")

if not SLACK_WEBHOOK:
    print("⚠️ Security Warning: SLACK_WEBHOOK_URL is missing in .env file!")

def send_slack_notification(message):
    payload = {"text": f"🚨 *BugBuster ML ALERT* 🚨\n> {message}"}
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(SLACK_WEBHOOK, data=data, headers={'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"Failed to send Slack alert: {e}")

def load_baselines():
    if not os.path.exists(BASELINES_FILE):
        print("❌ Error: user_baselines.json not found! Run 'trend_builder.py' first.")
        return None
    with open(BASELINES_FILE, 'r') as f:
        return json.load(f)

def monitor_live_traffic():
    baselines = load_baselines()
    if not baselines: return

    print("--- BugBuster: Active ML Anomaly Detection Started ---")
    print("Watching live traffic and comparing to user baselines...\n")

    if not os.path.exists(ONLINE_LOG):
        open(ONLINE_LOG, 'w').close()

    with open(ONLINE_LOG, 'r') as f:
       
        f.seek(0, os.SEEK_END)
        
       
        consecutive_errors = {user: 0 for user in baselines.keys()}
        
    
        last_alert_time = {} 

        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            
            try:
            
                user = line.split("User '")[1].split("'")[0]
                payload = int(line.split("Payload: ")[1].replace("B\n", "").strip())
                is_error = "ERROR" in line

                baseline = baselines.get(user)
                if not baseline:
                    continue 

                anomaly_reasons = []

             
                if payload > baseline["max_historical_payload"] * 2:
                    anomaly_reasons.append(f"Anomalous Payload ({payload}B vs normal max {baseline['max_historical_payload']}B)")

               
                if is_error:
                    consecutive_errors[user] += 1
                else:
                    consecutive_errors[user] = max(0, consecutive_errors[user] - 1) 

                if consecutive_errors[user] >= 3:
                    anomaly_reasons.append("Brute-force attack suspected (Multiple failed logins)")

                
                if anomaly_reasons:
                    alert_msg = f"User '{user}' behaving suspiciously! Reasons: {', '.join(anomaly_reasons)}"
                    print(f"⚠️ ANOMALY DETECTED: {alert_msg}")
                    
                    
                    current_time = time.time()
                    if current_time - last_alert_time.get(user, 0) > 10:
                        send_slack_notification(alert_msg)
                        last_alert_time[user] = current_time
                    
                   
                    consecutive_errors[user] = -5 

            except Exception as e:
                pass 

if __name__ == "__main__":
    monitor_live_traffic()