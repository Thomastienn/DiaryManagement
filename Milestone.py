import os
from datetime import datetime
from Diary import Diary
from Feature import Feature
from TextFile import TextFile
from MessageCode import MessageCode

class Milestone(Feature):
    def __init__(self, diary: Diary, year: int) -> None:
        self.year = year
        self.diary = diary

        mile_dir = f"{diary.dir}\\{year}\\Milestone"
        super().__init__(mile_dir)
    
    def change_year(self, year: int) -> None:
        self.year = year
        self.dir = f"{self.diary.dir}\\{year}\\Milestone"
    
    def get_menu(self) -> list:
        return ["Write", "Read", "Find"]
    
    def get_sub_menu(self) -> list:
        return ["SONGS", "MOVIES", "DAILY LIFE", "NEW FOOD", "NEW PEOPLE", "NEW PLACES", "NEW ACTIVITY", "TRENDING", "VERSIONS"]
    
    def get_time_stamp(self) -> str:
        return datetime.now().strftime("[%d/%m/20%y %H:%M:%S]") + ": "
    
    def handle_selection_write(self) -> str:
        os.system('cls')
        self.printSubMenu()
        
        try:
            user_milestone_select = int(input("Choose: "))
        except:
            user_milestone_select = 0

        if(user_milestone_select != 0):
            file_name = self.get_sub_menu()[user_milestone_select-1].replace(" ", "_")
            
            return f"{self.dir}\\{file_name}.txt"
        
    def __process_user_choose(self, user_selection):
        if(not user_selection.isdigit()):
            if(user_selection == "a"):
                self.change_year(self.year - 1)
            elif(user_selection == "d"):
                self.change_year(self.year + 1)
            return
        user_selection = int(user_selection)
        file_name = self.get_sub_menu()[user_selection-1].replace(" ", "_")
        read_file = TextFile(upper_dir=self.dir, file_name=file_name)
        
        decrypted_message = read_file.decrypt_file()
        print(decrypted_message)
        
    def navigate(self) -> None:
        while True:
            os.system('cls')
            self.printSubMenu()

            user_chose = input("Choose: ")
            if(user_chose != "0"):
                self.__process_user_choose(user_chose)
            else:
                break
            input("Press anything to continue...")
    
    def printSubMenu(self) -> None:
        self.printTitle(self.year)
        super().printMenu(self.get_sub_menu())
        
    def find(self, find_str, exact=True, case_sensitive=False, tokenize=False) -> None:
        pass
    