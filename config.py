from datetime import datetime
import time
from colorama import Fore, Back, Style

DIARY_DIR = "D:\\Diary"
KEYS_DIR = "D:\\keys"
PRIVATE_KEYS_DIR = f"{KEYS_DIR}\\private_key.pem"
PUBLIC_KEYS_DIR = f"{KEYS_DIR}\\public_key.pem"
MENU_WIDTH = 20
TITLE_WIDTH = 20

HEADER_STYLE = Fore.RED + Style.BRIGHT


today = datetime.now()
today_day_month = today.strftime("%d-%m")
current_year = today.strftime("20%y")
this_year_dir = DIARY_DIR + "\\" + current_year
today_file_dir = this_year_dir + "\\" + today_day_month + ".txt"
update_running_thread = True

def stop_all_thread():
    global update_running_thread
    
    update_running_thread = False

def update():
    global today,today_day_month, current_year, today_file_dir, today_day_month, this_year_dir
    
    while update_running_thread:
        today = datetime.now()
        today_day_month = today.strftime("%d-%m")
        current_year = today.strftime("20%y")
        this_year_dir = DIARY_DIR + "\\" + current_year
        today_file_dir = this_year_dir + "\\" + today_day_month + ".txt"
        
        time.sleep(1)