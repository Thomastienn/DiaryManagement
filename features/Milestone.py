import os
from datetime import datetime
from Diary import Diary
from Feature import Feature
from utils.TextFile import TextFile
from unidecode import unidecode
import utils.config

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
        return config.MILESTONE_SUB_MENU
    
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
        
        if(decrypted_message):
            print(self.iterate_txt(decrypted_message)["content"])
        
    def navigate(self) -> None:
        while True:
            os.system('cls')
            self.printSubMenu()

            user_chose = input("Choose: ")
            if(user_chose != "0"):
                self.__process_user_choose(user_chose)
            else:
                self.change_year(int(config.current_year))
                break
            input("Press anything to continue...")
    
    def printSubMenu(self) -> None:
        self.printTitle(self.year, style=config.TIMESTAMP_STYLE)
        super().printMenu(self.get_sub_menu())
        
    def find(self, find_str, exact, case_sensitive, accent_mark, normalization, whole_word) -> None:
        self.printHeader(config.MENU_WIDTH)
        print("YYYY YYYY")
        print("-"*config.MENU_WIDTH)
        
        user_range = input("Range: ")
        start_end = user_range.split(" ")
        start_year = int(start_end[0])
        end_year = int(start_end[1])
        
        user_category = []
        all_options = self.get_sub_menu()
        
        while(True):
            os.system("cls")
            print("-"*config.MENU_WIDTH)
            print("Category: "," ".join(all_options))
            print("Added: " + " ".join(user_category))
            print("-"*config.MENU_WIDTH)
            
            if(len(user_category) == len(self.get_sub_menu())):
                break
            
            user_choose_category = input("Choose category(num/a): ")
            if(user_choose_category == ""):
                break
            if(user_choose_category == "a"):
                user_category = self.get_sub_menu()
                print("Added all")         
                break
            else:
                try:
                    user_category.append(all_options[int(user_choose_category)])
                    del all_options[int(user_choose_category)]
                except IndexError:
                    continue
                except (TypeError, ValueError):
                    break
            
        
        search_str = self.preprocess_find_str(
            find_str=find_str,
            case_sensitive=case_sensitive,
            accent_mark=accent_mark,
            exact=exact
        )
            
        current_year = start_year
        while current_year <= end_year:
            for milestone_category in user_category:
                file_name = milestone_category.replace(" ", "_")
                file_dir = f"{config.DIARY_DIR}\\{current_year}\\Milestone\\{file_name}.txt"
                
                file_read = TextFile(full_dir = file_dir)
                
                self.process_find_in_text_file(
                    find_file=file_read,
                    search_str=search_str,
                    accent_mark=accent_mark,
                    case_sensitive=case_sensitive,
                    title=f"{current_year}-{milestone_category}",
                    normalization=normalization,
                    whole_word=whole_word
                )
                
            current_year += 1
    
