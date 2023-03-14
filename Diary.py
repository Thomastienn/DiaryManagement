import os, config
from datetime import datetime, timedelta
from Feature import Feature
from TextFile import TextFile

class Diary(Feature):
    def __init__(self, dir: str) -> None:
        super().__init__(dir, self.get_menu())
        
    def get_menu(self):
        return ["Write", "Read", "Keys", "Find"]
    
    def get_time_stamp(self) -> str:
        return datetime.now().strftime("[%H:%M:%S]") + ": "
    
    def handle_selection(self) -> None:
        return config.today_file_dir
    
    def navigate(self) -> None:
        cur_today = datetime.now()
        while True:
            os.system("cls")
            
            cur_today_day_month = cur_today.strftime("%d-%m")
            cur_today_year = cur_today.strftime("20%y")
            cur_today_file_upper_dir = config.DIARY_DIR + "\\" + cur_today_year

            date_title = f"{cur_today_day_month}-{cur_today_year}"
            self.printTitle(date_title)
            
            cur_today_file = TextFile(upper_dir=cur_today_file_upper_dir, file_name=cur_today_day_month)
            
            decrypted_message = cur_today_file.decrypt_file()
            print(decrypted_message)

            user_choose = input("NAV: ")
            if(user_choose == "a"):
                cur_today = (cur_today - timedelta(days=1))
            elif(user_choose == "d"):
                cur_today = (cur_today + timedelta(days=1))
            else:
                try:
                    cur_today = datetime.strptime(user_choose[:-5] + "-" + user_choose[-2:], "%d-%m-%y")
                except Exception:
                    break
                
    def find(self, find_str, exact=True, case_sensitive=False, tokenize=False) -> None:
        pass
