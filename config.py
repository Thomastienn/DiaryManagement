from datetime import datetime
import time

DIARY_DIR = "D:\\Diary"
KEYS_DIR = "D:\\keys"
PRIVATE_KEYS_DIR = f"{KEYS_DIR}\\private_key.pem"
PUBLIC_KEYS_DIR = f"{KEYS_DIR}\\public_key.pem"

today = datetime.now()
today_day_month = today.strftime("%d-%m")
current_year = today.strftime("20%y")
today_file_dir = DIARY_DIR + current_year + "\\" + today_day_month + ".txt"

def update():
    global current_year, today_file_dir
    
    while True:
        today = datetime.now()
        today_day_month = today.strftime("%d-%m")
        current_year = today.strftime("20%y")
        today_file_dir = DIARY_DIR + current_year + "\\" + today_day_month + ".txt"
        
        time.sleep(1)