from datetime import datetime, timedelta
import time, os
from colorama import Fore, Back, Style

#! SETUP 
PROGRAM_DIR = "D:\\DiaryProgram"
DIARY_DIR = "D:\\Diary"
KEYS_DIR = "D:\\keys"

PRIVATE_KEYS_DIR = f"{KEYS_DIR}\\private_key.pem"
PUBLIC_KEYS_DIR = f"{KEYS_DIR}\\public_key.pem"
STATS_DB = PROGRAM_DIR + "\\database\\stats_diary.pkl"

MENU_WIDTH = 20
TITLE_WIDTH = 20

RESET_STYLE  = Fore.RESET

HEADER_STYLE = Fore.CYAN + Style.BRIGHT
INVALID_HEADER_STYLE = Fore.RED + Style.BRIGHT

TRUE_STYLE = Fore.GREEN + Style.BRIGHT
FALSE_STYLE = Fore.RED + Style.BRIGHT
NONE_STYLE = Fore.LIGHTWHITE_EX + Style.DIM
FOUND_STYLE = Fore.RED + Style.BRIGHT

FUNCTION_STYLE = Fore.WHITE
TIMESTAMP_STYLE = Fore.YELLOW + Style.BRIGHT
DAYTIME_STYLE = Fore.BLUE + Style.BRIGHT
DEFAULT_STYLE = Style.RESET_ALL
HIGHTLIGHT_STYLE = Fore.WHITE + Style.BRIGHT

PEOPLE_STYLE = Fore.BLUE + Style.BRIGHT
PLACES_STYLE = Fore.GREEN + Style.BRIGHT
UNCERTAIN_STYLE = Fore.LIGHTBLUE_EX

update_running_thread = True
has_valid_key = True
use_normalize_text = False


def init_update():
    global today,today_day_month, current_year, today_file_dir, today_day_month, this_year_dir, shortcut_date
        
    today = datetime.now()
    today_day_month = today.strftime("%d-%m")
    current_year = today.strftime("20%y")
    this_year_dir = DIARY_DIR + "\\" + current_year
    today_file_dir = this_year_dir + "\\" + today_day_month + ".txt"

    shortcut_date = {
        "s": datetime(year=2022, month=12, day=21),
        "td": datetime(year=int(current_year), month=today.month, day=today.day),
        "sy": datetime(year=int(current_year), month=1, day=1),
        "sm": datetime(year=int(current_year), month=int(today.strftime("%m")), day=1),
    }

init_update()

def select_valid_header_style():
    return HEADER_STYLE if has_valid_key else INVALID_HEADER_STYLE

def select_bool_style(boolean: bool, returnText: bool = True):
    if(boolean is None):
        style = NONE_STYLE
    else:
        style = TRUE_STYLE if boolean else FALSE_STYLE
    
    if(returnText):
        style += str(boolean)
        
    return style

def stop_all_thread():
    global update_running_thread
    
    update_running_thread = False

def update():
    while update_running_thread:
        init_update()
        time.sleep(1)