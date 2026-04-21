import random
import csv
from datetime import datetime, timedelta

HISTORY_FILE = 'historical_logs.csv'

def generate_historical_data():
    print("⏳ Generating 72 hours of historical baseline data...")
    start_time = datetime.now() - timedelta(days=3)
    
    with open(HISTORY_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'api_latency_ms', 'cpu_usage_pct', 'error_rate_pct', 'avg_payload_kb'])
        
        for i in range(72 * 60): 
            current_time = start_time + timedelta(minutes=i)
            hour = current_time.hour
            
            if 2 <= hour <= 6:
                lat, cpu, pay = random.randint(50, 120), random.randint(10, 35), random.randint(50, 200)
            else:
                lat, cpu, pay = random.randint(100, 300), random.randint(30, 75), random.randint(150, 800)
            err = random.randint(0, 3) 
            writer.writerow([current_time.strftime("%Y-%m-%d %H:%M:%S"), lat, cpu, err, pay])
            
    print(f"✅ Historical logs ready in {HISTORY_FILE}")

if __name__ == "__main__":
    generate_historical_data()