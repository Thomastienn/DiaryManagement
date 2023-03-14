from datetime import datetime
from Diary import Diary
from Feature import Feature

class Milestone(Feature):
    def __init__(self, diary: Diary, year: int) -> None:
        self.year = year
        self.diary = diary

        mile_dir = f"{diary.dir}\\{year}\\Milestone"
        super().__init__(mile_dir, self.get_menu())
    
    def change_year(self, year: int) -> None:
        self.year = year
        self.dir = f"{self.diary.dir}\\{year}\\Milestone"
    
    def get_menu(self) -> list:
        return ["SONGS", "MOVIES", "DAILY LIFE", "NEW FOOD", "NEW PEOPLE", "NEW PLACES", "NEW ACTIVITY", "TRENDING", "VERSIONS"]
    
    def get_time_stamp(self) -> str:
        return datetime.now().strftime("[%d/%m/20%y %H:%M:%S]") + ": "
    
    def handle_selection(self) -> str:
        try:
            user_milestone_select = int(input("Choose: "))
        except:
            user_milestone_select = 0

        if(user_milestone_select != 0):
            file_name = self.get_menu()[user_milestone_select-1].replace(" ", "_")
            
            return f"{self.dir}\\{file_name}.txt"