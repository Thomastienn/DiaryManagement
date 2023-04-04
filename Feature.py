import config
from abc import abstractmethod
from TextFile import TextFile
from unidecode import unidecode
class Feature():
    def __init__(self, dir: str) -> None:
        self.dir = dir
    
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
    def find(self, find_str, exact, case_sensitive, accent_mark) -> None:
        pass
    
    def find_all(self, origin: str, list_sub: list) -> list:
        all_occurences = set()
        
        for sub in list_sub:
            start = 0
            while True:
                index = origin.find(sub, start)
                if index == -1:
                    break
                
                all_occurences.add(index)
                start = index + 1
        return list(all_occurences)
    
    def printMenu(self, menu: list) -> None:
        width = config.MENU_WIDTH
        self.printHeader(width)
        print("0. Exit")
        for i in range(len(menu)):
            print(config.FUNCTION_STYLE + str(i+1) + ". " + menu[i])
        print(config.HEADER_STYLE + "-"*width)

    def printTitle(self, mes: str) -> None:
        width = config.TITLE_WIDTH
        print("-"*width)
        print(str(mes).center(width, " "))
        print("-"*width)
        
    def printHeader(self, width):
        print(config.HEADER_STYLE + self.__class__.__name__.center(width, "-"))
     
    def preprocess_find_str(self, find_str, case_sensitive, accent_mark, exact) -> list:
        if(not case_sensitive):
            find_str = find_str.lower()
        if(not accent_mark):
            find_str = unidecode(find_str)
        search_str = []
        if(not exact):
            search_str = find_str.split(" ")
        else:
            search_str.append(find_str)
            
        return search_str
       
    def process_find_in_text_file(self, find_file: TextFile, search_str, accent_mark, case_sensitive, title) -> None:
        all_text_day = find_file.decrypt_file()
        if(not all_text_day):
            return
        immutable_all_text_day = all_text_day
        if(not accent_mark):
            all_text_day = unidecode(all_text_day)
        
        if(not case_sensitive):
            all_text_day = all_text_day.lower()
            
        found = self.find_all(all_text_day, search_str)
        if(len(found) != 0):
            all_lines_found = self.index_occ_to_start_line(immutable_all_text_day, found)
            print(self.printTitle(title))
            for line in all_lines_found:
                print(line)
            print()
        
    def index_occ_to_start_line(self, text: str, occurences: list) -> list:
        start_lines = []
        end_lines = []
        for occ in occurences:
            start_line_index = occ
            end_line_index = occ
            
            while(text[start_line_index] != "["):
                start_line_index -= 1
            while(text[end_line_index] != "\n"):
                end_line_index += 1    
                
            start_lines.append(start_line_index)
            end_lines.append(end_line_index)
        
        res = []
        for start,end in zip(start_lines, end_lines):
            res.append(text[start:end])
            
        return res
        
    