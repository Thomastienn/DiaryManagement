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
INVALID_HEADER_STYLE = Fore.RED + Style.BRIGHT

TRUE_STYLE = Fore.GREEN + Style.BRIGHT
FALSE_STYLE = Fore.RED + Style.BRIGHT
NONE_STYLE = Fore.LIGHTWHITE_EX + Style.DIM

FUNCTION_STYLE = Fore.WHITE
TIMESTAMP_STYLE = Fore.YELLOW

update_running_thread = True
has_valid_key = True
use_normalize_text = False

normalize_language_with_accent_mark = {
    "bùn": "buồn",
    "đãk": "đã",
    "qá": "quá",
    "zị": "vị",
    "zữ": "dữ",
    "zũ": "vũ",
    "zãi": "vãi",
    "típ": "tiếp",
    "hỉu": "hiểu",
    "cừi": "cười",
    "cúi": "cuối",
    "mụt": "một",
    "nhìu": "nhiều",
    "nhiu": "nhiêu",
    "qá": "quá",
    "xún": "xuống",
    "lừi": "lười",
    "chiện": "chuyện",
    "gòi": "rồi",
    "gữi": "rưỡi",
    "lứt": "lướt",
    "pạn": "bạn",
    "pán": "bán",
    "pắn": "bắn",
    "pàn": "bàn",
    "zẫn": "vẫn",
    "củm": "cảm",
    "ló": "nó",
    "lúm": "lắm",
    "chìu": "chiều",
    "xợ": "sợ",
    "bụn": "bụng",
    "tìn": "tiền",
    "qên": "quên",
    "ngụ": "ngủ",
    "đọ": "đó",
    "dứi": "dưới",
    "nớp": "lớp",
    "nụa": "nữa",
    "gùi": "rồi",
    "kím": "kiếm",
    "gớt": "rớt",
    "đth": "điện thoại",
}

normalize_language_no_accent_mark = {
    "ac": "acc",
    "ang": "ăn",
    "bt": "bài tập",
    "byt": "buýt",
    "bic": "biết",
    "chs": "chơi",
    "coa": "có",
    "cgi": "cái gì",
    "cnhat": "chủ nhật",
    "ch": "chưa",
    "chug": "chung",
    "cum": "cũng",
    "cko": "cho",
    "ckac": "chắc",
    "dc": "được",
    "dr": "đúng rồi",
    "droi": "đúng rồi",
    "ei": "ê",
    "ga": "ra",
    "goi": "roi",
    "gut": "rút",
    "gke": "ghê",
    "h": "giờ",
    "hog": "không",
    "hok": "học",
    "hec": "hết",
    "hme": "hề",
    "koi": "coi",
    "ktra": "kiểm tra",
    "loi": "nói",
    "lun": "luôn",
    "liu": "liệu",
    "lay": "nay",
    "ms": "mới",
    "mng": "mọi người",
    "mec": "mệt",
    "min": "mình",
    "ng": "người",
    "nc": "nước",
    "nka": "nha",
    "nhma": "nhưng mà",
    "nhao": "nhau",
    "pay": "bay",
    "pa": "ba",
    "pan": "ban",
    "khom": "không",
    "ko": "không",
    "kon": "con",
    "qa": "qua",
    "qen": "quen",
    "qcao": "quảng cáo",
    "quánh": "đánh",
    "sn": "sinh nhật",
    "sou": "sầu",
    "thiec": "thiệt",
    "trc": "trước",
    "thg": "thang",
    "tar": "ta",
    "tr": "trời",
    "thoy": "thôi",
    "th": "thôi",
    "un": "uống",
    "xog": "xong",
    "ze": "ve",
    "zu": "du",
    "zo": "vô",
    "ziet": "viet",
    "zoi": "với",
    "zi": "gì",
    "z": "vậy",
    "zay": "vậy",
    "zua": "vua",
}


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