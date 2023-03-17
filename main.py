import os, threading, config
from Diary import Diary
from Milestone import Milestone
from TextFile import TextFile
from Feature import Feature
from MessageCode import MessageCode

def create_new_year_folder():
    if(not os.path.exists(config.this_year_dir)):
        os.mkdir(config.this_year_dir)

def write_main(main_writer: Feature):
    write_dir = main_writer.handle_selection_write()
    userText = input("Enter txt to write to file: ")
    
    if (userText):
        create_new_year_folder()
        file_to_write = TextFile(full_dir = write_dir)
        file_to_write.write_file(main_writer.get_time_stamp() + userText)
    else:
        print("Empty message")

def read_main(main_reader: Feature):
    main_reader.navigate()

def find_main(main_finder: Feature):
    pass

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

options = {
    "0": end,
    "1": write_main,
    "2": read_main,
    "3": find_main,
    
    # Features only in diary
    "4": milestone_main,
    "5": find_main
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
        avail_options = (str(i) for i in range(len(current_feature.get_menu())))
        
        if(user_input in avail_options):
            options.get(user_input, default)(current_feature)
        
        print("Press to continue...")
        input()

if __name__ == "__main__":
    run()

