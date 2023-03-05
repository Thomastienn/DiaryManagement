import os
import ast
import rsa
from datetime import datetime, timedelta

CURRENT_YEAR = datetime.now().strftime("20%y")
PRIVATE_KEYS_DIR = "D:\\keys\\private_key.pem"
MILESTONE_DIR = f"D:\\Diary\\{CURRENT_YEAR}\\Milestone"
EXTRA = ["SONGS", "MOVIES", "DAILY LIFE", "NEW FOOD", "NEW PEOPLE", "NEW PLACES", "NEW ACTIVITY", "TRENDING", "VERSIONS"]

def decrypt_rsa_message(ciphertext_file, private_key_file):
    with open(private_key_file, 'rb') as key_file:
        private_key = rsa.PrivateKey.load_pkcs1(key_file.read())

    try:
        with open(ciphertext_file, 'rb') as f:
            returnText = ""

            ciphertext = f.read()

            list = ciphertext.decode("utf-8").split("\n")

            for line in list:
                if(len(line) != 0):
                    try:
                        plaintext = rsa.decrypt(ast.literal_eval(line), private_key)
                        returnText += plaintext.decode("utf-8") + "\n"
                    except:
                        continue
            return returnText
    except Exception:
        return "You didn't write diary this date"

def write_to_file_with_encryption(filename, text):
    with open("D:\\keys\\public_key.pem", "rb") as key_file:
        public_key = rsa.PublicKey.load_pkcs1(key_file.read())

    message = text.encode("utf-8")
    encrypted_text = rsa.encrypt(message, public_key)

    mode = "a" if os.path.exists(filename) else "w"
    with open(filename, mode, encoding="utf-8") as file:
        file.write(str(encrypted_text) + "\n")
    print("Success")

def printMenu():
    WIDTH = 10

    print("-"*WIDTH)
    print("0. Exit")
    print("1. Write")
    print("2. Read")
    print("-"*WIDTH)

def printMilestoneMenu():
    WIDTH = 10

    print("-"*WIDTH)
    print("0. Exit")
    for i in range(len(EXTRA)):
        print(str(i+1) + ". " + EXTRA[i])
    print("-"*WIDTH)

def printTitle(mes):
    print("-"*10)
    print(mes)
    print("-"*10)


def run():
    while True:
        os.system('cls')
        printMenu()
        user_input = input("Choose an option: ")
        if(user_input == "0"):
            return
        elif(user_input == "1"):
            dir = ""
            timeStamp = ""

            user_choose = input("Diary or milestone (D/M): ")

            if(user_choose == "d"):
                today=datetime.now().strftime("%d-%m")
                dir = "D:\\Diary\\" + datetime.now().strftime("20%y") + "\\" + today + ".txt"
                timeStamp = datetime.now().strftime("[%H:%M:%S]") + ": "
            else:
                os.system('cls')
                printMilestoneMenu()

                try:
                    user_milestone_select = int(input("Choose: "))
                except:
                    user_milestone_select = 0

                if(user_milestone_select != 0):
                    nm = "_".join(EXTRA[user_milestone_select-1].split(" "))
                    dir = f"{MILESTONE_DIR}\\{nm}.txt"
                    timeStamp = datetime.now().strftime("[%d/%m/20%y %H:%M:%S]") + ": "

            userText = input("Enter txt to write to file: ")

            if(len(userText) == 0):
                print("Empty message")
            else:
                write_to_file_with_encryption(dir, timeStamp + userText)

        elif(user_input == "2"):
            user_choose = input("Diary or milestone (D/M): ")
            dir = ""

            if(user_choose == "d"):
                today=datetime.now()

                while True:
                    todayString = today.strftime("%d-%m")
                    todayYear = today.strftime("20%y")
                    os.system("cls")

                    printTitle(f"{todayString}-{todayYear}")
                    dir = f"D:\\Diary\\{todayYear}\\{todayString}.txt"

                    decrypted_message = decrypt_rsa_message(dir, PRIVATE_KEYS_DIR)
                    print(decrypted_message)

                    user_choose = input("NAV: ")
                    if(user_choose == "a"):
                        today = (today - timedelta(days=1))
                    elif(user_choose == "d"):
                        today = (today + timedelta(days=1))
                    else:
                        try:
                            today = datetime.strptime(user_choose[:-5] + "-" + user_choose[-2:], "%d-%m-%y")
                        except Exception:
                            break
                
            else:
                os.system('cls')
                printMilestoneMenu()

                try:
                    user_milestone_select = int(input("Choose: "))
                except:
                    user_milestone_select = 0

                if(user_milestone_select != 0):
                    nm = "_".join(EXTRA[user_milestone_select-1].split(" "))
                    dir = f"{MILESTONE_DIR}\\{nm}.txt"

                    decrypted_message = decrypt_rsa_message(dir, PRIVATE_KEYS_DIR)
                    print(decrypted_message)

        print("Press to continue...")
        input()
run()

