import os, threading, config, rsa, requests, secret_storage, time, pickle, dbop
from Diary import Diary
from Milestone import Milestone
from TextFile import TextFile
from Feature import Feature
from colorama import init
from pyasn1.error import SubstrateUnderrunError
from googletrans import Translator
from datetime import timedelta, datetime

def send_notification(mess: str, desc: str, noti_type="info"):
    requests.post('https://api.mynotifier.app', {
        "apiKey": secret_storage.MYNOTIFIER_API_KEY,
        "message": mess,
        "description": desc,
        "type": noti_type, # info, error, warning or success
    })

def write_main(main_writer: Feature):
    write_dir = main_writer.handle_selection_write()
    userText = input("Enter txt to write to file: ")
    
    if (userText):
        file_to_write = TextFile(full_dir = write_dir)
        file_to_write.write_file(main_writer.get_time_stamp() + userText)
    else:
        print("Empty message")

def read_main(main_reader: Feature):
    if(not config.has_valid_key):
        print("Don't be sneaky")
        send_notification(mess="Watchout!", desc="Someone is trying to read your diary", noti_type="warning")
        return
    main_reader.navigate()

def find_main(main_finder: Feature):
    if(not config.has_valid_key):
        print("Don't be sneaky")
        send_notification(mess="Watchout!", desc="Someone is trying to read your diary", noti_type="warning")
        return
    
    # Default value
    user_exact = True #22-12-2022 17-03-2023
    user_case_sensitive = False
    user_accent_mark = False
    user_normalization = False
    
    def print_find_properties():
        def print_option(name: str, user_bool: bool):
            print(config.FUNCTION_STYLE + name, config.select_bool_style(user_bool))
        
        main_finder.printHeader(config.MENU_WIDTH)
        print_option("1. EXACT: ", user_exact)
        print_option("2. CASE SENSITIVE: ", user_case_sensitive)
        print_option("3. ACCENT MARK: ", user_accent_mark)
        print_option("4. NORMALIZATION: ", user_normalization)
        
        print(config.HEADER_STYLE + "-"*config.MENU_WIDTH)
        print(config.HIGHTLIGHT_STYLE + "0. START")
        print(config.HEADER_STYLE + "-"*config.MENU_WIDTH)
    
    while True:
        os.system("cls")
        print_find_properties()
        user_chose = input("Set: ")
        
        if(user_chose == "0"):
            need_find_str = input("Enter search str: ")
            if(need_find_str):
                main_finder.find(need_find_str, exact=user_exact, 
                                case_sensitive=user_case_sensitive,
                                accent_mark=user_accent_mark,
                                normalization=user_normalization)
            break
        if(user_chose == "1"):
            user_exact = not user_exact
        elif(user_chose == "2"):
            user_case_sensitive = not user_case_sensitive
        elif(user_chose == "3"):
            user_accent_mark = not user_accent_mark
        elif(user_chose == "4"):
            user_normalization = not user_normalization
        else:
            break


def milestone_main(feature: Feature):
    global current_feature
    current_feature = main_milestone

def default():
    print("In development\n")
  
    
def end(feature: Feature):
    global current_feature
    
    if(current_feature is main_diary):
        config.stop_all_thread()
        exit()
    else:
        current_feature = main_diary

def insert_key(feature: Feature):
    print("Enter your key: ")
    
    line = input()
    res = ""
    while line:
        res += line + "\n"    
        line = input()
        
    with open(config.PRIVATE_KEYS_DIR, 'w') as key_file:
        key_file.write(res)
    
    check_key_valid()
    
def remove_key(feature: Feature):
    with open(config.PRIVATE_KEYS_DIR, 'w') as key_file:
        key_file.truncate(0)
    print("Delete successfully!\n")
    
    config.has_valid_key = False

def check_key_valid():
    config.has_valid_key = True
    try:
        with open(config.PRIVATE_KEYS_DIR, 'rb') as key_file:
            rsa.PrivateKey.load_pkcs1(key_file.read())
    except (ValueError, SubstrateUnderrunError):
        config.has_valid_key = False

def toggle_translation(feature: Feature):
    translator = Translator()

def toggle_normalize_text(feature: Feature):
    config.use_normalize_text = not config.use_normalize_text
    print("Toggle successfully!\n")
    
def update_light_weight_db():
    db = dbop.get_database(config.STATS_DB)
    
    start_date = current_day = db["last_light_updated"]
    end_date = config.shortcut_date["td"]
    
    if(start_date == end_date):
        return
    
    relative_no_files = 0
    relative_total_bytes = 0
    
    # Not include today
    while current_day != end_date:
        cur_today_day_month, cur_today_year = current_day.strftime("%d-%m"), str(current_day.year)
        cur_today_file_upper_dir = config.DIARY_DIR + "\\" + cur_today_year
        current_date_file = TextFile(upper_dir=cur_today_file_upper_dir,
                                    file_name=cur_today_day_month)
        current_day = current_day + timedelta(days=1)
        
        if(not current_date_file.is_existed()):
            relative_no_files += 1
            continue
        
        relative_total_bytes += current_date_file.stored_size()
    
    dbop.update_relative_database(config.STATS_DB, [\
        ("total_days", end_date-start_date), \
        ("total_days_skipped", relative_no_files), \
        ("last_light_updated", config.shortcut_date["td"])])

# To sync with the current statistic if something goes wrong
# Only use once per 90 days
# It will use as a sync feature once the diary is 4 years old
def update_heavy_db():
    db = dbop.get_database(config.STATS_DB)
    if((config.shortcut_date["td"] - db["last_heavy_updated"]).days < 90):
        return
    
    total_bytes = 0
    total_lines = 0
    total_chars = 0
    
    for (root,dirs,files) in os.walk(top=config.DIARY_DIR):
        for f in files:
            if f.endswith(".txt"):
                # construct the full file path
                file_path = os.path.join(root, f)
                text_file = TextFile(full_dir=file_path)
                
                text = text_file.decrypt_file()
                total_bytes += text_file.stored_size()
                total_lines += len(text.split("\n"))
                total_chars += len(text)
    
    update_missing_date()
    dbop.update_database(config.STATS_DB, [\
        ("total_days",(config.shortcut_date["td"] + timedelta(days=1) - config.shortcut_date["s"]).days), \
        ("total_storage", total_bytes), \
        ("total_lines", total_lines), \
        ("total_characters", total_chars), \
        ("last_heavy_updated", config.shortcut_date["td"])])

def update_missing_date():
    current_day = config.shortcut_date["s"]
    end_date = config.shortcut_date["td"]
    no_files = 0
    while current_day != end_date:
        cur_today_day_month, cur_today_year = current_day.strftime("%d-%m"), str(current_day.year)
        cur_today_file_upper_dir = config.DIARY_DIR + "\\" + cur_today_year
        current_date_file = TextFile(upper_dir=cur_today_file_upper_dir,
                                    file_name=cur_today_day_month)
        current_day = current_day + timedelta(days=1)
        
        if(not current_date_file.is_existed()):
            no_files += 1
            continue
        
    dbop.update_database(config.STATS_DB, [("total_days_skipped", no_files)])

def show_stats(feature: Feature):
    if(not config.has_valid_key):
        print("No key no stats")
        return
    
    os.system("cls")
    print(config.HIGHTLIGHT_STYLE + "LOADING...\n")
    
    db_file = open(config.STATS_DB, "rb")
    db = pickle.load(db_file)
    
    total_days = db["total_days"]
    no_files = db["total_days_skipped"]
    total_lines = db["total_lines"]
    total_chars = db["total_characters"]
    total_bytes = db["total_storage"]
    
    os.system("cls")
    print(config.HIGHTLIGHT_STYLE + "There have been " + config.HEADER_STYLE + str(total_days) + config.HIGHTLIGHT_STYLE + " days")
    print(config.HIGHTLIGHT_STYLE + "You skipped " + config.HEADER_STYLE + str(no_files) + config.HIGHTLIGHT_STYLE + " days")
    print(config.HIGHTLIGHT_STYLE + "You wrote " + config.HEADER_STYLE + str(total_lines) + config.HIGHTLIGHT_STYLE + " lines with " + config.HEADER_STYLE + str(total_chars) + config.HIGHTLIGHT_STYLE + " characters")
    print(config.HIGHTLIGHT_STYLE + "The storage is " + config.HEADER_STYLE + str(total_bytes) + config.HIGHTLIGHT_STYLE + " bytes or " + config.HEADER_STYLE + str(round(total_bytes/1024*100)/100) + config.HIGHTLIGHT_STYLE + " KB or " + config.HEADER_STYLE + str(round(total_bytes/1024/1024 *100)/100) + config.HIGHTLIGHT_STYLE + " MB")
    
    print("\n")

options = {
    # Features that all inherits
    # the class has
    "0": end,
    "1": write_main,
    "2": read_main,
    "3": find_main,
    
    # Features only in diary
    "4": milestone_main,
    "5": insert_key,
    "6": remove_key,
    "7": toggle_normalize_text,
    "8": toggle_translation,
    "9": show_stats,
}  


def update_db():
    update_light_weight_db()
    update_heavy_db()

def run():
    global current_feature, main_diary, main_milestone
    
    # Init and update the config file every second
    t = threading.Thread(target=config.update)
    t.start()
    
    main_diary = Diary(dir=config.DIARY_DIR)
    main_milestone = Milestone(diary=main_diary,year=int(config.current_year))
    
    current_feature = main_diary
    
    check_key_valid()
    
    t_db = threading.Thread(target=update_db)
    t_db.start()
    
    while True:
        os.system('cls')
        current_feature.printMenu(current_feature.get_menu())
        
        user_input = input("Choose an option: ")
        avail_options = [str(i) for i in range(len(current_feature.get_menu()) + 1)]
        
        if(user_input in avail_options):
            options.get(user_input, default)(current_feature)
        
        print("Press to continue...")
        input()

if __name__ == "__main__":
    init(autoreset=True)
    run()

