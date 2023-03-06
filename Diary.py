import os
import ast
import rsa
from datetime import datetime, timedelta

# Constants
CURRENT_YEAR = datetime.now().strftime("20%y")
PRIVATE_KEYS_DIR = "D:\\keys\\private_key.pem"
MILESTONE_DIR = f"D:\\Diary\\{CURRENT_YEAR}\\Milestone"
EXTRA = ["SONGS", "MOVIES", "DAILY LIFE", "NEW FOOD", "NEW PEOPLE", "NEW PLACES", "NEW ACTIVITY", "TRENDING", "VERSIONS"]

def decrypt_rsa_message(ciphertext_file, private_key_file):
    # Get private key
    with open(private_key_file, 'rb') as key_file:
        private_key = rsa.PrivateKey.load_pkcs1(key_file.read())

    # If there is the file
    try:
        with open(ciphertext_file, 'rb') as f:
            returnText = ""

            ciphertext = f.read()

            list = ciphertext.decode("utf-8").split("\n")

            # Decrypt by each line
            for line in list:
                # If the line is valid
                if(len(line) != 0):
                    try:
                        # line is string representation of byte
                        # Ex: b'ads\123\saf\bsbs'
                        # ast -> turns into real byte
                        plaintext = rsa.decrypt(ast.literal_eval(line), private_key)
                        returnText += plaintext.decode("utf-8") + "\n"
                    except:
                        continue
            return returnText
    except Exception:
        return "You didn't write diary this date"

def break_long_string_into_list(text):
    words_list = text.split(" ")
    final_res = []
    curNumBytes = 0
    MAX_BYTES = 240
    line_text = ""

    for word in words_list:
        real_word = word + " "
        curNumBytes += utf8len(real_word)
        if(curNumBytes > MAX_BYTES):
            final_res.append(line_text)
            curNumBytes = 0
            line_text = ""
        line_text += real_word
    final_res.append(line_text)

    return final_res

def write_to_file_with_encryption(filename, text):
    # Get public key
    with open("D:\\keys\\public_key.pem", "rb") as key_file:
        public_key = rsa.PublicKey.load_pkcs1(key_file.read())

    for piece in break_long_string_into_list(text):
        # piece: string -> into message: byte
        message = piece.encode("utf-8")
        encrypted_text = rsa.encrypt(message, public_key)

        # Create a new file if it's not existed
        mode = "a" if os.path.exists(filename) else "w"

        # Write the string representation of the byte
        with open(filename, mode, encoding="utf-8") as file:
            file.write(str(encrypted_text) + "\n")
    print("Success")

def printMenu():
    WIDTH = 10

    print("-"*WIDTH)
    print("0. Exit")
    print("1. Write")
    print("2. Read")
    print("3. Keys")
    print("4. Find")
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

def utf8len(s):
    return len(s.encode('utf-8'))

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

