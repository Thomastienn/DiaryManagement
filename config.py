from datetime import datetime, timedelta
import time
from colorama import Fore, Back, Style

DIARY_DIR = "D:\\Diary"
KEYS_DIR = "D:\\keys"
PRIVATE_KEYS_DIR = f"{KEYS_DIR}\\private_key.pem"
PUBLIC_KEYS_DIR = f"{KEYS_DIR}\\public_key.pem"
MENU_WIDTH = 20
TITLE_WIDTH = 20

HEADER_STYLE = Fore.CYAN + Style.BRIGHT
TRUE_STYLE = Fore.GREEN + Style.BRIGHT
FALSE_STYLE = Fore.RED + Style.BRIGHT
FUNCTION_STYLE = Fore.WHITE

update_running_thread = True

def init_update():
    global today,today_day_month, current_year, today_file_dir, today_day_month, this_year_dir, shortcut_date
        
    today = datetime.now()
    today_day_month = today.strftime("%d-%m")
    current_year = today.strftime("20%y")
    this_year_dir = DIARY_DIR + "\\" + current_year
    today_file_dir = this_year_dir + "\\" + today_day_month + ".txt"

    shortcut_date = {
        "s": datetime(year=2022, month=12, day=21),
        "td": today,
        "sy": datetime(year=int(current_year), month=1, day=1),
        "sm": datetime(year=int(current_year), month=int(today.strftime("%m")), day=1),
    }

init_update()

def select_bool_style(boolean: bool):
    style = TRUE_STYLE if boolean else FALSE_STYLE
    return style + str(boolean)

def stop_all_thread():
    global update_running_thread
    
    update_running_thread = False

def update():
    while update_running_thread:
        init_update()
        time.sleep(1)