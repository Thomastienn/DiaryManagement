import os, threading, config
from datetime import datetime, timedelta
from Diary import Diary
from Milestone import Milestone
from TextFile import TextFile
from Feature import Feature

def write_main():
    main_writer = main_milestone
    user_choose = input("Diary or milestone (D/M): ")

    if(user_choose == "d"):
        main_writer = main_diary
    else:
        os.system('cls')
        main_milestone.printMenu()

    write_dir = main_writer.handle_selection()
    userText = input("Enter txt to write to file: ")
    
    if (userText):
        file_to_write = TextFile(full_dir = write_dir)
        file_to_write.write_file(main_writer.get_time_stamp() + userText)
    else:
        print("Empty message")

def read_main():
    user_choose = input("Diary or milestone (D/M): ")

    if(user_choose == "d"):
        main_diary.navigate()
        
    elif(user_choose == "m"):
        os.system('cls')
        main_milestone.printMenu()

        try:
            user_milestone_select = int(input("Choose: "))
        except:
            user_milestone_select = 0

        if(user_milestone_select != 0):
            file_name = main_milestone.get_menu()[user_milestone_select-1].replace(" ", "_")

            read_file = TextFile(upper_dir=main_milestone.dir, file_name=file_name)
            decrypted_message = read_file.decrypt_file()
            
            print(decrypted_message)
    else:
        return

def default():
    print("In development\n")

options = {
    "1": write_main,
    "2": read_main,
}

def run():
    # Init and update the config file every second
    t = threading.Thread(target=config.update)
    t.start()
    
    global main_diary, main_milestone
    
    main_diary = Diary(dir=config.DIARY_DIR)
    main_milestone = Milestone(diary=main_diary,year=config.current_year)
    

    while True:
        os.system('cls')
        main_diary.printMenu()
        user_input = input("Choose an option: ")

        options.get(user_input, default)()

        print("Press to continue...")
        input()
run()

