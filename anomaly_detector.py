import time
import os
import json
import urllib.request
from dotenv import load_dotenv

# Зареждаме тайните от .env файла (Сейфа)
load_dotenv()

ONLINE_LOG = 'app.log'
BASELINES_FILE = 'user_baselines.json'

# Взимаме линка сигурно от системните променливи
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
        # Отиваме в края на файла, за да четем само новите неща в реално време
        f.seek(0, os.SEEK_END)
        
        # Брояч за поредни грешки (за засичане на Brute-force)
        consecutive_errors = {user: 0 for user in baselines.keys()}
        
        # Пази кога за последно сме пратили Slack съобщение за даден потребител (Защита от спам)
        last_alert_time = {} 

        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            
            try:
                # Извличаме данните от реда
                user = line.split("User '")[1].split("'")[0]
                payload = int(line.split("Payload: ")[1].replace("B\n", "").strip())
                is_error = "ERROR" in line

                baseline = baselines.get(user)
                if not baseline:
                    continue # Ако е непознат потребител, го пропускаме

                # --- 🧠 ML ЛОГИКА ЗА ЗАСИЧАНЕ НА АНОМАЛИИ ---
                anomaly_reasons = []

                # Правило 1: Payload Anomaly (Ако пакетът е 2 пъти по-голям от най-големия нормален в историята)
                if payload > baseline["max_historical_payload"] * 2:
                    anomaly_reasons.append(f"Anomalous Payload ({payload}B vs normal max {baseline['max_historical_payload']}B)")

                # Правило 2: Brute-Force Attack (Много грешни пароли една след друга)
                if is_error:
                    consecutive_errors[user] += 1
                else:
                    consecutive_errors[user] = max(0, consecutive_errors[user] - 1) # Намаляваме, ако влезе успешно

                if consecutive_errors[user] >= 3:
                    anomaly_reasons.append("Brute-force attack suspected (Multiple failed logins)")

                # --- АЛАРМА ---
                if anomaly_reasons:
                    alert_msg = f"User '{user}' behaving suspiciously! Reasons: {', '.join(anomaly_reasons)}"
                    print(f"⚠️ ANOMALY DETECTED: {alert_msg}")
                    
                    # Проверяваме дали са минали поне 10 секунди от последната Slack аларма
                    current_time = time.time()
                    if current_time - last_alert_time.get(user, 0) > 10:
                        send_slack_notification(alert_msg)
                        last_alert_time[user] = current_time # Обновяваме таймера
                    
                    # Ресетваме брояча временно, за да не спами Slack по 5 пъти в секунда
                    consecutive_errors[user] = -5 

            except Exception as e:
                pass # Игнорираме счупени редове

if __name__ == "__main__":
    monitor_live_traffic()