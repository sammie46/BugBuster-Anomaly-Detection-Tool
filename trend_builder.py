import json
import os

HISTORICAL_LOG = 'historical.log'
BASELINES_FILE = 'user_baselines.json'

def build_trends():
    print("--- BugBuster: Building User Baselines (ML Training Phase) ---")
    
    if not os.path.exists(HISTORICAL_LOG):
        print("❌ Error: historical.log not found. Run 'py generate_history.py' first!")
        return

    user_data = {}

    # 1. Четене на историческите данни и събиране на статистика
    with open(HISTORICAL_LOG, 'r') as f:
        for line in f:
            try:
                # Изваждаме името на потребителя
                user = line.split("User '")[1].split("'")[0]
                
                # Изваждаме размера на пакета (Payload)
                payload_str = line.split("Payload: ")[1].replace("B\n", "").replace("B", "").strip()
                payload = int(payload_str)
                
                # Проверяваме дали редът е грешка
                is_error = 1 if "ERROR" in line else 0

                if user not in user_data:
                    user_data[user] = {"total_events": 0, "errors": 0, "payloads": []}

                user_data[user]["total_events"] += 1
                user_data[user]["errors"] += is_error
                user_data[user]["payloads"].append(payload)
                
            except Exception as e:
                continue # Игнорираме, ако някой ред е счупен

    baselines = {}
    
    # 2. Изчисляване на Тренд (Базова линия) за всеки потребител
    for user, data in user_data.items():
        total = data["total_events"]
        error_rate = data["errors"] / total if total > 0 else 0
        avg_payload = sum(data["payloads"]) / len(data["payloads"])
        max_payload = max(data["payloads"])
        
        baselines[user] = {
            "normal_error_rate": round(error_rate, 3), # напр. 0.05 е 5%
            "avg_payload": round(avg_payload, 2),
            "max_historical_payload": max_payload
        }

    # 3. Запазване на "наученото" във файл, за да го ползваме на живо
    with open(BASELINES_FILE, 'w') as f:
        json.dump(baselines, f, indent=4)

    print(f"✅ Training complete! Baselines saved to '{BASELINES_FILE}'.")
    print("\n--- Learned User Profiles ---")
    for user, stats in baselines.items():
        print(f"👤 {user}: Normal Error Rate: {stats['normal_error_rate']*100:.1f}%, Max Payload: {stats['max_historical_payload']}B")

if __name__ == "__main__":
    build_trends()