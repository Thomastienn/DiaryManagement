import os, threading, config, rsa, requests, secret_storage, time
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

def show_stats(feature: Feature):
    os.system("cls")
    print(config.HIGHTLIGHT_STYLE + "LOADING...\n")
    
    days_past = (config.today - config.shortcut_date["s"]).days
    
    no_files = 0
    current_day = config.shortcut_date["s"]
    while current_day != config.shortcut_date["td"]:
        cur_today_day_month, cur_today_year = current_day.strftime("%d-%m"), str(current_day.year)
        cur_today_file_upper_dir = config.DIARY_DIR + "\\" + cur_today_year
        current_date_file = TextFile(upper_dir=cur_today_file_upper_dir,
                                    file_name=cur_today_day_month)
        
        if(not current_date_file.is_existed()):
            no_files += 1
            
        current_day = current_day + timedelta(days=1)
    
    os.system("cls")
    print(config.HIGHTLIGHT_STYLE + "There have been " + config.HEADER_STYLE + str(days_past) + config.HIGHTLIGHT_STYLE + " days")
    print(config.HIGHTLIGHT_STYLE + "You skipped " + config.HEADER_STYLE + str(no_files) + config.HIGHTLIGHT_STYLE + " days")
    
    
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
    
def run():
    global current_feature, main_diary, main_milestone
    
    # Init and update the config file every second
    t = threading.Thread(target=config.update)
    t.start()
    
    main_diary = Diary(dir=config.DIARY_DIR)
    main_milestone = Milestone(diary=main_diary,year=int(config.current_year))
    
    current_feature = main_diary
    
    check_key_valid()

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

