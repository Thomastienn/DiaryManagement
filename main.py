import os, threading, config, keyboard, msvcrt, time
from Diary import Diary
from Milestone import Milestone
from TextFile import TextFile

def create_new_year_folder():
    if(not os.path.exists(config.this_year_dir)):
        os.mkdir(config.this_year_dir)

def write_main():
    main_writer = main_milestone
    
    user_chose = input("Diary or milestone (D/M): ")
    
    if(user_chose == "d"):
        main_writer = main_diary 

    write_dir = main_writer.handle_selection()
    userText = input("Enter txt to write to file: ")
    
    if (userText):
        create_new_year_folder()
        file_to_write = TextFile(full_dir = write_dir)
        file_to_write.write_file(main_writer.get_time_stamp() + userText)
    else:
        print("Empty message")

def read_main():
    user_choose = input("Diary or milestone (D/M): ")
    main_reader = main_milestone

    if(user_choose == "d"):
        main_reader = main_diary
        
    main_reader.navigate()

def find_main():
    pass

def default():
    print("In development\n")

def end():
    config.stop_all_thread()
    exit()
    
options = {
    "0": end,
    "1": write_main,
    "2": read_main,
}


def run():
    # Init and update the config file every second
    t = threading.Thread(target=config.update)
    t.start()
    
    global main_diary, main_milestone
    
    main_diary = Diary(dir=config.DIARY_DIR)
    main_milestone = Milestone(diary=main_diary,year=int(config.current_year))
    
    while True:
        os.system('cls')
        main_diary.printMenu()
        
        user_input = input("Choose an option: ")
        options.get(user_input, default)()
        
        print("Press to continue...")
        input()

if __name__ == "__main__":
    run()

