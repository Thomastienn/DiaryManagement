import os, threading, config, requests, json
from Diary import Diary
from Milestone import Milestone
from TextFile import TextFile
from Feature import Feature
from colorama import init

def write_main(main_writer: Feature):
    write_dir = main_writer.handle_selection_write()
    userText = input("Enter txt to write to file: ")
    
    if (userText):
        file_to_write = TextFile(full_dir = write_dir)
        file_to_write.write_file(main_writer.get_time_stamp() + userText)
    else:
        print("Empty message")

def read_main(main_reader: Feature):
    main_reader.navigate()

def find_main(main_finder: Feature):
    # Default value
    user_exact = True #22-12-2022 17-03-2023
    user_case_sensitive = False
    user_accent_mark = False
    
    def print_find_properties():
        main_finder.printHeader(config.MENU_WIDTH)
        print("1. EXACT: ", config.select_bool_style(user_exact))
        print("2. CASE SENSITIVE: ", config.select_bool_style(user_case_sensitive))
        print("3. ACCENT MARK: ", config.select_bool_style(user_accent_mark))
        print("-"*config.MENU_WIDTH)
        print(config.FUNCTION_STYLE + "0. START")
        print("-"*config.MENU_WIDTH)
    
    while True:
        os.system("cls")
        print_find_properties()
        user_chose = input("Set: ")
        
        if(user_chose == "0"):
            need_find_str = input("Enter search str: ")
            if(need_find_str):
                main_finder.find(need_find_str, exact=user_exact, 
                                case_sensitive=user_case_sensitive,
                                accent_mark=user_accent_mark)
            break
        if(user_chose == "1"):
            user_exact = not user_exact
        elif(user_chose == "2"):
            user_case_sensitive = not user_case_sensitive
        elif(user_chose == "3"):
            user_accent_mark = not user_accent_mark
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

def quote_main(feature: Feature):
    response = requests.get("https://api.quotable.io/random")
    data = json.loads(response.text)
    print("-"*config.MENU_WIDTH)
    print("Author: " + data["author"])
    print("Quote: " + "\"" + data["content"] + "\"")
    print("-"*config.MENU_WIDTH)

options = {
    # Features that all inherits
    # the class has
    "0": end,
    "1": write_main,
    "2": read_main,
    "3": find_main,
    
    # Features only in diary
    "4": milestone_main,
    "5": default,
    "6": quote_main
}  
    
def run():
    global current_feature, main_diary, main_milestone
    
    # Init and update the config file every second
    t = threading.Thread(target=config.update)
    t.start()
    
    main_diary = Diary(dir=config.DIARY_DIR)
    main_milestone = Milestone(diary=main_diary,year=int(config.current_year))
    
    current_feature = main_diary
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

