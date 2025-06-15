from datetime import datetime
import time
from colorama import Fore, Style

#! SETUP 
PROGRAM_DIR = "D:\\May MSI\\DiaryProgram"
DIARY_DIR = "D:\\May MSI\\Diary"
KEYS_DIR = "D:\\May MSI\\keys"
IMAGE_TEMP_DIR = "C:\\Users\\thoma\\TempImages"
RESOLUTION = 360

MILESTONE_SUB_MENU = ["SONGS", "MOVIES", "BOOKS", "DAILY LIFE", "NEW FOOD", "NEW PEOPLE", "NEW PLACES", "NEW ACTIVITY", "TRENDING", "VERSIONS"]
DIARY_MENU = ["Write", "Read", "Find", "Milestone", "Insert key", "Remove key", "Statistics", "Guide", "Valid Files"]

PRIVATE_KEYS_DIR = f"{KEYS_DIR}\\private_key.pem"
PUBLIC_KEYS_DIR = f"{KEYS_DIR}\\public_key.pem"
IMAGE_KEY_DIR = f"{KEYS_DIR}\\public_key.pkl"

DATABASE_DIR = PROGRAM_DIR + "\\database"
STATS_DB = DATABASE_DIR + "\\stats_diary.pkl"
PEOPLE_DB = DATABASE_DIR + "\\people.pkl"
PLACES_DB = DATABASE_DIR + "\\places.pkl"
NOTES_DB = DATABASE_DIR + "\\notes.pkl"

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
NUMBERIC_STYLE = Fore.RED + Style.BRIGHT

PEOPLE_STYLE = Fore.BLUE + Style.BRIGHT
PLACES_STYLE = Fore.GREEN + Style.BRIGHT
UNCERTAIN_STYLE = Fore.MAGENTA + Style.BRIGHT

update_running_thread = True
has_valid_key = True
use_normalize_text = False
use_annotate_normalize = False
use_translation = False
classifying_mode = False
highlight_text = True
break_sentence = False

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
