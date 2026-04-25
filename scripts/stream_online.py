import time
import random
from datetime import datetime

ONLINE_LOG = 'data/online_data.log'

def simulate_online_data():
    print("🌐 Starting Online DATA generation...")
    open(ONLINE_LOG, 'w').close() 
    start_time = time.time()
    
    with open(ONLINE_LOG, 'a') as f:
        while True:
            now = datetime.now()
            hour = now.hour
            elapsed = time.time() - start_time
            
        
            if 2 <= hour <= 6:
                lat, cpu, pay = random.randint(50, 120), random.randint(10, 35), random.randint(50, 200)
            else:
                lat, cpu, pay = random.randint(100, 300), random.randint(30, 75), random.randint(150, 800)
            err = random.randint(0, 3) 
            
         
            if elapsed > 15:
                case = random.choice([1, 2, 3])
                if case == 1: lat, cpu = random.randint(3000, 5000), random.randint(90, 100)
                elif case == 2: err = random.randint(25, 45)
                elif case == 3: 
                    now = now.replace(hour=3)
                    pay = random.randint(5000, 15000)
                time.sleep(3) 
            
            log_line = f"{now.strftime('%Y-%m-%d %H:%M:%S')},{lat},{cpu},{err},{pay}\n"
            f.write(log_line)
            f.flush()
            time.sleep(1.0)

if __name__ == "__main__":
    simulate_online_data()