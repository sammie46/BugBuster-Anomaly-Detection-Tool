import json
import pandas as pd
from sklearn.ensemble import IsolationForest

HISTORY_FILE = 'data/historical_logs.csv'
TRENDS_FILE = 'data/trends.json'

def build_trends_with_ml():
    print("🤖 Analyzing historical data and building trends using ML...")
    df = pd.read_csv(HISTORY_FILE)
    
   
    features = ['api_latency_ms', 'cpu_usage_pct', 'error_rate_pct', 'avg_payload_kb']
    X = df[features]
    model = IsolationForest(contamination=0.01, random_state=42)
    model.fit(X)
    
    
    df['is_normal'] = model.predict(X)
    normal_df = df[df['is_normal'] == 1]
    
    
    trends = {
        "mu_latency": float(normal_df['api_latency_ms'].mean()),
        "sigma_latency": float(normal_df['api_latency_ms'].std()),
        "mu_cpu": float(normal_df['cpu_usage_pct'].mean()),
        "sigma_cpu": float(normal_df['cpu_usage_pct'].std()),
        "mu_error": float(normal_df['error_rate_pct'].mean()),
        "sigma_error": float(normal_df['error_rate_pct'].std()),
        "mu_payload": float(normal_df['avg_payload_kb'].mean()),
        "sigma_payload": float(normal_df['avg_payload_kb'].std())
    }
    
    with open(TRENDS_FILE, 'w') as f:
        json.dump(trends, f, indent=4)
    print(f"✅ Trends built and saved to {TRENDS_FILE}")

if __name__ == "__main__":
    build_trends_with_ml()