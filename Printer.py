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