import os, threading, config
from datetime import datetime, timedelta
from Diary import Diary
from Milestone import Milestone
from TextFile import TextFile

def write_main():
    global main_diary, main_milestone, TODAY_FILE
    
    dir = ""
    time_stamp = ""

    user_choose = input("Diary or milestone (D/M): ")

    if(user_choose == "d"):
        time_stamp = datetime.now().strftime("[%H:%M:%S]") + ": "
    else:
        os.system('cls')
        main_milestone.printMilestoneMenu()

        try:
            user_milestone_select = int(input("Choose: "))
        except:
            user_milestone_select = 0

        if(user_milestone_select != 0):
            nm = "_".join(main_milestone.EXTRA[user_milestone_select-1].split(" "))
            dir = f"{main_milestone.dir}\\{nm}.txt"
            time_stamp = datetime.now().strftime("[%d/%m/20%y %H:%M:%S]") + ": "

    userText = input("Enter txt to write to file: ")

    if(not userText):
        print("Empty message")
    else:
        write_file = TextFile(dir=dir)
        write_file.write_file(time_stamp + userText)

def read_main():
    global main_diary, main_milestone

    user_choose = input("Diary or milestone (D/M): ")
    dir = ""

    cur_today = datetime.now()
    if(user_choose == "d"):
        while True:
            os.system("cls")
            
            cur_today_day_month = cur_today.strftime("%d-%m")
            cur_today_year = cur_today.strftime("20%y")
            main_diary.printTitle(f"{cur_today_day_month}-{cur_today_year}")

            cur_today_file_dir = config.DIARY_DIR + cur_today_day_month + "\\" + cur_today_year + ".txt"
            cur_today_file = TextFile(dir=cur_today_file_dir)
            
            decrypted_message = cur_today_file.decrypt_file()
            print(decrypted_message)

            user_choose = input("NAV: ")
            if(user_choose == "a"):
                cur_today = (cur_today - timedelta(days=1))
            elif(user_choose == "d"):
                cur_today = (cur_today + timedelta(days=1))
            else:
                try:
                    cur_today = datetime.strptime(user_choose[:-5] + "-" + user_choose[-2:], "%d-%m-%y")
                except Exception:
                    break
        
    else:
        os.system('cls')
        main_milestone.printMenu()

        try:
            user_milestone_select = int(input("Choose: "))
        except:
            user_milestone_select = 0

        if(user_milestone_select != 0):
            file_name = "_".join(main_milestone.MILESTONES[user_milestone_select-1].split(" "))
            dir = f"{main_milestone}\\{file_name}.txt"

            read_file = TextFile(dir)
            decrypted_message = read_file.decrypt_file()
            print(decrypted_message)

def default():
    print("In development\n")

options = {
    "1": write_main,
    "2": read_main,
}

def run():
    main_diary = Diary(dir=config.DIARY_DIR)
    main_milestone = Milestone(diary=main_diary,year=config.CURRENT_YEAR)
    
    # Update the config file every second
    t = threading.Thread(target=config.update)
    t.start()

    while True:
        os.system('cls')
        main_diary.printMenu()
        user_input = input("Choose an option: ")

        options.get(user_input, default)()

        print("Press to continue...")
        input()
run()

