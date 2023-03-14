import rsa, ast, os
from abc import ABC, abstractmethod

class Feature():
    def __init__(self, dir: str, menu: list) -> None:
        self.dir = dir
        self.menu = menu 
    
    @abstractmethod        
    def get_menu(self) -> list:
        pass
    
    @abstractmethod        
    def get_time_stamp(self) -> str:
        pass
    
    @abstractmethod        
    def handle_selection_write(self) -> None:
        pass

    def printMenu(self) -> None:
        WIDTH = 10

        print("-"*WIDTH)
        print("0. Exit")
        for i in range(len(self.menu)):
            print(str(i+1) + ". " + self.menu[i])
        print("-"*WIDTH)

    def printTitle(self, mes):
        print("-"*10)
        print(mes)
        print("-"*10)