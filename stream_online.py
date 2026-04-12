import time
import random
from datetime import datetime

ONLINE_LOG = 'app.log'
USERS = ['alice', 'bob', 'charlie', 'diana']

def stream_online_data():
    print("--- BugBuster: Starting LIVE Online Data Stream ---")
    
    # Изчистваме стария онлайн лог
    open(ONLINE_LOG, 'w').close() 
    
    attack_started = False
    start_time = time.time()
    
    with open(ONLINE_LOG, 'a') as f:
        while True:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            elapsed = time.time() - start_time
            
            # АТАКАТА на Иванчо започва след 15 секунди
            if elapsed > 15:
                if not attack_started:
                    print("\n🚨 SIMULATING ATTACK: 'charlie' is brute-forcing and sending anomalous payloads!\n")
                    attack_started = True
                
                user = 'charlie'
                payload_size = random.randint(5000, 10000) # Аномален payload
                log_line = f"{now} ERROR: User '{user}' wrong password. Payload: {payload_size}B\n"
                
            else:
                # Нормален трафик преди атаката
                user = random.choice(USERS)
                payload_size = random.randint(100, 500)
                if random.random() < 0.95:
                    log_line = f"{now} INFO: User '{user}' logged in smoothly. Payload: {payload_size}B\n"
                else:
                    log_line = f"{now} ERROR: User '{user}' wrong password. Payload: {payload_size}B\n"

            f.write(log_line)
            f.flush()
            print(f"Live: {log_line.strip()}")
            
            time.sleep(0.5 if attack_started else 2.0)

if __name__ == "__main__":
    stream_online_data()