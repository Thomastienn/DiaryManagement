from datetime import datetime
import rsa

def utf8len(s):
    return len(s.encode('utf-8'))

userChoose = "Day la doan test thu split test theo do dai neu bi dai qua bi cat bot giong nhu kieu line break nhung ma no bi dom hon. This is a line test for spliting test if the length is exceeded, the text will be split similar to line break but a cheaper version as dasjoadfi ma asdoi nasd a dsnaks nas adjio sadj sa dnoias dna dnsajk dan wq iqwj e afn jasknf a sdji aosd aosd najd nas dnajd sna dknajs nas jodiasj oiajs iodjaskd nsqkn dqkjw dqo iwjqo iwdjqpw jdqij qoiwj qo ijd Day la doan test thu split test theo do dai neu bi dai qua bi cat bot giong nhu kieu line break nhung ma no bi dom hon"

words_list = userChoose.split(" ")
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

for piece in final_res:
    print(piece + "\nEND\n")



# def option1():
#     print("Option 1 selected")

# def option2():
#     print("Option 2 selected")

# def option3():
#     print("Option 3 selected")

# def default():
#     print("Invalid choice")

# options = {
#     "1": option1,
#     "2": option2,
#     "3": option3
# }

# while True:
#     print("========== MENU ==========")
#     print("1. Option 1")
#     print("2. Option 2")
#     print("3. Option 3")
#     print("==========================")
#     choice = input("Enter the number of your choice (1-3): ")
#     options.get(choice, default)()
