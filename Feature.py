import rsa, ast, os

class Feature:
    def __init__(self, dir: str, menu: list) -> None:
        self.dir = dir
        self.menu = menu 

    def printMenu(self) -> None:
        WIDTH = 10

        print("-"*WIDTH)
        print("0. Exit")
        for i in range(len(self.menu)):
            print(str(i+1) + ". " + self.menu[i])
        print("-"*WIDTH)

    def printTitle(mes):
        print("-"*10)
        print(mes)
        print("-"*10)