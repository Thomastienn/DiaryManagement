from Diary import Diary
from Feature import Feature

class Milestone(Feature):
    MILESTONES = ["SONGS", "MOVIES", "DAILY LIFE", "NEW FOOD", "NEW PEOPLE", "NEW PLACES", "NEW ACTIVITY", "TRENDING", "VERSIONS"]

    def __init__(self, diary: Diary, year: int) -> None:
        self.year = year
        
        mile_dir = f"{diary.dir}\\{year}\\Milestone"
        super().__init__(mile_dir, self.MILESTONES)