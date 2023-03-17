import os, config
from datetime import datetime, timedelta
from Feature import Feature
from TextFile import TextFile

class Diary(Feature):
    def __init__(self, dir: str) -> None:
        super().__init__(dir)
        
    def get_menu(self):
        return ["Write", "Read", "Find", "Milestone", "Keys"]
    
    def get_time_stamp(self) -> str:
        return datetime.now().strftime("[%H:%M:%S]") + ": "
    
    def handle_selection_write(self) -> None:
        return config.today_file_dir
    
    def navigate(self) -> None:
        cur_today = datetime.now()
        while True:
            os.system("cls")
            
            cur_today_day_month, cur_today_year = self.__datetime_to_month_year(cur_today)
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
                    cur_today = datetime.strptime(self.__to_format_datetime(user_choose), "%d-%m-%y")
                except ValueError:
                    break
                
    def __datetime_to_month_year(self, date_time: datetime):
        return (date_time.strftime("%d-%m"), date_time.strftime("20%y"))
    
    def __to_format_datetime(self, string_datetime: str) -> str:
        return string_datetime[:-5] + "-" + string_datetime[-2:]
    
    def find(self, find_str: str, exact: bool, case_sensitive: bool, accent_mark: bool) -> None:
        os.system("cls")
        self.printHeader(config.MENU_WIDTH)
        print("DD-MM-YYYY DD-MM-YYYY")
        print("-"*config.MENU_WIDTH)
        user_range = input("Range: ")
        
        start_end = user_range.split(" ")
        
        start_date = datetime.strptime(self.__to_format_datetime(start_end[0]), "%d-%m-%y")
        end_date = datetime.strptime(self.__to_format_datetime(start_end[1]), "%d-%m-%y")
        
        if(not case_sensitive):
            find_str = find_str.lower()
        search_str = [find_str]
        if(not exact):
            search_str = [word for word in find_str.split(" ")]
        
        # Retrieve text from diary
        # Process case sensitive
        # Find the str
        current_date = start_date
        while current_date != end_date:
            cur_today_day_month, cur_today_year = self.__datetime_to_month_year(current_date)
            cur_today_file_upper_dir = config.DIARY_DIR + "\\" + cur_today_year
            current_date_file = TextFile(upper_dir=cur_today_file_upper_dir,
                                         file_name=cur_today_day_month)
            
            all_text_day = current_date_file.decrypt_file()
            if(not case_sensitive):
                all_text_day = all_text_day.lower()
                
            for word in search_str:
                found = self.find_all(all_text_day, word)
                if(found != -1):
                    all_lines_found = self.__index_occ_to_start_line(all_text_day, found)
            if(all_lines_found):
                date_title = f"{cur_today_day_month}-{cur_today_year}"
                print(self.printTitle(date_title))
                for line in all_lines_found:
                    print(line)
                print()
            
            current_date = current_date + timedelta(days=1)
            
    def __index_occ_to_start_line(self, text: str, occurences: list) -> list:
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
