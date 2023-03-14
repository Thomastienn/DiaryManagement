import config
from abc import abstractmethod

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
    
    @abstractmethod        
    def navigate(self) -> None:
        pass
    
    @abstractmethod        
    def find(self, find_str, exact=True, case_sensitive=False, tokenize=False) -> None:
        pass
        
    def printMenu(self) -> None:
        width = config.MENU_WIDTH
        print(self.__class__.__name__.center(width, "-"))
        print("0. Exit")
        for i in range(len(self.menu)):
            print(str(i+1) + ". " + self.menu[i])
        print("-"*width)

    def printTitle(self, mes: str) -> None:
        width = config.TITLE_WIDTH
        print("-"*width)
        print(str(mes).center(width, " "))
        print("-"*width)
        
    