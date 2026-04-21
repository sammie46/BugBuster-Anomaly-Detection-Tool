import time
import os
import json
import urllib.request
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

ONLINE_LOG = 'online_data.log'
TRENDS_FILE = 'trends.json'
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_notification(message):
    if not SLACK_WEBHOOK: return
    payload = {"text": f"🚨 *BugBuster Alert* 🚨\n> {message}"}
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(SLACK_WEBHOOK, data=data, headers={'Content-Type': 'application/json'})
    try: urllib.request.urlopen(req)
    except Exception: pass

def track_and_analyze():
   
    if not os.path.exists(TRENDS_FILE):
        print("❌ Run build_trends.py first!")
        return
    with open(TRENDS_FILE, 'r') as f:
        trends = json.load(f)

    print("🔎Tracking online data, analyzing, and deciding...")
    if not os.path.exists(ONLINE_LOG): open(ONLINE_LOG, 'w').close()
    last_alert = 0

    with open(ONLINE_LOG, 'r') as f:
        f.seek(0, os.SEEK_END) 
        
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            
            try:
                
                ts_str, lat_str, cpu_str, err_str, pay_str = line.strip().split(',')
                lat, cpu, err, pay = float(lat_str), float(cpu_str), float(err_str), float(pay_str)
                dt = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
                
               
                f1 = (lat - trends['mu_latency']) / trends['sigma_latency']
                f2 = (cpu - trends['mu_cpu']) / trends['sigma_cpu']
                f3 = (err - trends['mu_error']) / trends['sigma_error']
                f4 = (pay - trends['mu_payload']) / trends['sigma_payload']
                f5 = 1 if 2 <= dt.hour <= 6 else 0 
                
                score = (0.3 * f1) + (0.2 * f2) + (0.2 * f3) + (0.2 * f4) + (0.1 * f5)
                
                
                if score > 5:
                    reasons = []
                    if lat > 1000: reasons.append(f"Latency Spike ({lat}ms)")
                    if err > 15: reasons.append(f"High Error Rate ({err}%)")
                    if pay > 2000: reasons.append(f"Payload Anomaly ({pay}KB)")
                    
                    msg = f"Anomaly Score: {score:.2f} > 5\n*Triggers:* {', '.join(reasons)}"
                    print(f"⚠️ {msg}")
                    
                    
                    if time.time() - last_alert > 10:
                        send_slack_notification(msg)
                        last_alert = time.time()

            except Exception:
                pass 

if __name__ == "__main__":
    track_and_analyze()