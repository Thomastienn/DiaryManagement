import os
import ast
import rsa
from datetime import datetime

PRIVATE_KEYS_DIR = "D:\\keys\\private_key.pem"
MILESTONE_DIR = "D:\\Diary\\2023\\Milestone"
EXTRA = ["SONGS", "MOVIES", "DAILY LIFE", "NEW FOOD", "NEW PEOPLE", "NEW PLACES", "NEW ACTIVITY", "TRENDING", "VERSIONS"]

def decrypt_rsa_message(ciphertext_file, private_key_file):
    with open(private_key_file, 'rb') as key_file:
        private_key = rsa.PrivateKey.load_pkcs1(key_file.read())

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

def write_to_file_with_encryption(filename, timestamp):
    text = input("Enter txt to write to file: ")

    with open("D:\\keys\\public_key.pem", "rb") as key_file:
        public_key = rsa.PublicKey.load_pkcs1(key_file.read())

    message = f"{timestamp}: {text}".encode("utf-8")
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


def run():
    while True:
        os.system('cls')
        printMenu()
        user_input = input("Choose an option: ")
        if(user_input == "0"):
            return
        elif(user_input == "1"):
            dir = ""

            user_choose = input("Diary or milestone (D/M): ")

            if(user_choose == "d"):
                today=datetime.now().strftime("%d-%m")
                dir = "D:\\Diary\\" + datetime.now().strftime(str(20) + "%y") + "\\" + today + ".txt"
                timestamp = datetime.now().strftime("[%H:%M:%S]")
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
                    timestamp = datetime.now().strftime("[%d/%m/20%y %H:%M:%S]")

            write_to_file_with_encryption(dir, timestamp)

        elif(user_input == "2"):
            user_choose = input("Diary or milestone (D/M): ")
            dir = ""

            if(user_choose == "d"):
                user_date = input("What date??(DD-MM-YYYY): ")
                user_year = user_date[-4:]
                user_day_month = user_date[:-5]
                dir = f"D:\\Diary\\{user_year}\\{user_day_month}.txt"
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

