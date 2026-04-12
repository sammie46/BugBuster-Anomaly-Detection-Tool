import random
from datetime import datetime, timedelta

HISTORICAL_LOG = 'historical.log'
USERS = ['alice', 'bob', 'charlie', 'diana']

def generate_historical_data(days=5):
    print(f"--- BugBuster: Generating {days} days of Historical Data ---")
    
    with open(HISTORICAL_LOG, 'w') as f:
        # Връщаме времето 5 дни назад
        start_date = datetime.now() - timedelta(days=days)
        
        # Генерираме по 50 лога на ден
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            for _ in range(50):
                user = random.choice(USERS)
                
                # НОРМАЛНО поведение: Пакетите са малки (100-500 Bytes)
                payload_size = random.randint(100, 500) 
                
                # 95% успешни влизания, 5% нормални човешки грешки
                if random.random() < 0.95:
                    f.write(f"{current_date.strftime('%Y-%m-%d %H:%M:%S')} INFO: User '{user}' logged in smoothly. Payload: {payload_size}B\n")
                else:
                    f.write(f"{current_date.strftime('%Y-%m-%d %H:%M:%S')} ERROR: User '{user}' wrong password. Payload: {payload_size}B\n")
                
                current_date += timedelta(minutes=random.randint(5, 30))
                
    print("✅ Historical Data successfully saved in 'historical.log'.")

if __name__ == "__main__":
    generate_historical_data()