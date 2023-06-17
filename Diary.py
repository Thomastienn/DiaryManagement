import os, config, calendar, time, storage, dbop
from datetime import datetime, timedelta
from Feature import Feature
from TextFile import TextFile
from unidecode import unidecode

class Diary(Feature):
    def __init__(self, dir: str) -> None:
        super().__init__(dir)
        
    def get_menu(self):
        return ["Write", "Read", "Find", "Milestone", "Insert key", "Remove key", "Setting",
                "Statistics"]
    
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

            date_title = f"{calendar.day_name[cur_today.weekday()]} {cur_today_day_month}-{cur_today_year}"

            cur_today_file = TextFile(upper_dir=cur_today_file_upper_dir, file_name=cur_today_day_month)
            
            if(config.classifying_mode):
                unknown_words = self.__list_unknown_capital_words(cur_today_file)
                
                for i, unk_word in enumerate(unknown_words):
                    self.printTitle(date_title, style=config.DAYTIME_STYLE)
                    for j, word in enumerate(unknown_words):
                        if(i == j):
                            print(config.HEADER_STYLE + word, end=" ")
                        else:
                            print(config.UNCERTAIN_STYLE + word, end=" ")
                    print("\n")
                    print(config.HEADER_STYLE + unk_word)
                    
                    database_select = {
                        "pe": config.PEOPLE_DB,
                        "pl": config.PLACES_DB
                    }
                    
                    print()
                    print(config.DAYTIME_STYLE + "-"*20)
                    print(config.PEOPLE_STYLE + "pe | people")
                    print(config.PLACES_STYLE + "pl | places")
                    print(config.DAYTIME_STYLE + "-"*20)
                    print()
                    
                    user_classify = input(config.UNCERTAIN_STYLE +  "Classify: " + config.DEFAULT_STYLE)
                    if(user_classify == "b"):
                        break
                    
                    try:
                        db_dir = database_select[user_classify]
                    except KeyError:
                        print(config.FALSE_STYLE + "\nNot adding!\n")
                        os.system("cls")
                        continue
                        
                    db = dbop.get_database(db_dir)
                    db.add(unk_word)
                    dbop.write_database(db, db_dir)

                    print(config.TRUE_STYLE + "\nAdded successfully!\n")
                    os.system("cls")
            else:
                self.printTitle(date_title, style=config.DAYTIME_STYLE)
                decrypted_message = cur_today_file.decrypt_file()
                if(decrypted_message):
                    text = self.iterate_txt(decrypted_message)
                    print(text)

            if(config.classifying_mode):
                self.printTitle(date_title, style=config.DAYTIME_STYLE)
            
            print()
            user_choose = input("NAV: ")
            if(user_choose == "a"):
                cur_today = (cur_today - timedelta(days=1))
            elif(user_choose == "d"):
                cur_today = (cur_today + timedelta(days=1))
            elif(user_choose == "anno"):
                config.use_annotate_normalize = not config.use_annotate_normalize
            elif(user_choose == "nor"):
                config.use_normalize_text = not config.use_normalize_text
            elif(user_choose == "csf"):
                config.classifying_mode = not config.classifying_mode
            else:
                try:
                    cur_today = datetime.strptime(self.__to_format_datetime(user_choose), "%d-%m-%y")
                except ValueError:
                    break
    
    def __list_unknown_capital_words(self, text_file: TextFile) -> list:
        storage.update_latest()
        
        decrypted_message = text_file.decrypt_file()
        res = []
        
        for word in decrypted_message.split(" "):
            if(not word):
                continue
            is_time_stamp = False
            
            if("[" in word or "]" in word):
                is_time_stamp = True
                
            if(word[0].isupper() and not is_time_stamp):
                if(unidecode(word.lower()) not in storage.people and unidecode(word.lower()) not in storage.places and word not in storage.people and word not in storage.places):
                    res.append(word)
        
        return res
                
    
    def __datetime_to_month_year(self, date_time: datetime):
        return (date_time.strftime("%d-%m"), date_time.strftime("20%y"))
    
    def __to_format_datetime(self, string_datetime: str) -> str:
        return string_datetime[:-5] + "-" + string_datetime[-2:]
    
    def find(self, find_str: str, exact: bool, case_sensitive: bool, accent_mark: bool, normalization: bool, whole_word: bool) -> None:
        os.system("cls")
        self.printHeader(config.MENU_WIDTH)
        print("DD-MM-YYYY DD-MM-YYYY")
        print(config.HEADER_STYLE + "-"*config.MENU_WIDTH)
        user_range = input("Range: ")
        print(config.HIGHTLIGHT_STYLE + "\nYou want to find " + config.HEADER_STYLE + "\"" + find_str + "\"")
        
        start_end = user_range.split(" ")
        
        start = start_end[0]
        if(start in config.shortcut_date):
            start_date = config.shortcut_date.get(start)
        else:
            # Format: yYYYY 
            # Ex: y2022
            if(start[0] == "y"):
                start_date = datetime(day=1, month=1, year=int(start[1:]))
            elif(start[0] == "m"):
                start_date = datetime(day=1, month=int(start[1:]), year=int(config.current_year))
            else:
                start_date = datetime.strptime(self.__to_format_datetime(start), "%d-%m-%y")
        
        end = start_end[1]
        if(end in config.shortcut_date):
            end_date = config.shortcut_date.get(end)
        else:
            if(end[0] == "y"):
                end_date = datetime(day=1, month=1, year=int(end[1:] + 1))
            elif(end[0] == "m"):
                next_month = int(end[1:]) + 1
                if(next_month == 13):
                    next_month = 1
                end_date = datetime(day=1, month=next_month, year=int(config.current_year))
            else:
                end_date = datetime.strptime(self.__to_format_datetime(end), "%d-%m-%y")
            
        search_str = self.preprocess_find_str(
            find_str=find_str,
            case_sensitive=case_sensitive,
            accent_mark=accent_mark,
            exact=exact
        )
        
        print(config.HIGHTLIGHT_STYLE + "SEARCHING " + (config.HIGHTLIGHT_STYLE + " + ").join(list(map(lambda b: config.HEADER_STYLE + "\"" + b + "\"",search_str))) + "\n")
        
        # Retrieve text from diary
        # Process case sensitive
        # Find the str
        current_date = start_date
        end_date = end_date+timedelta(days=1)
        
        all_times_found = 0
        invalid_files = 0
        no_written_files = 0
        start_time = time.time()
        while current_date != end_date:
            cur_today_day_month, cur_today_year = self.__datetime_to_month_year(current_date)
            cur_today_file_upper_dir = config.DIARY_DIR + "\\" + cur_today_year
            current_date_file = TextFile(upper_dir=cur_today_file_upper_dir,
                                         file_name=cur_today_day_month)
            
            times_found, is_written = self.process_find_in_text_file(
                find_file=current_date_file,
                search_str=search_str,
                accent_mark=accent_mark,
                case_sensitive=case_sensitive,
                title=f"{cur_today_day_month}-{cur_today_year}",
                normalization=normalization,
                whole_word=whole_word
            )
            if(times_found):
                all_times_found += times_found
            else:
                invalid_files += 1
                
            if(not is_written):
                no_written_files +=  1
            
            current_date = current_date + timedelta(days=1)
        
        end_time = time.time()
        time_taken = (end_time-start_time)*10**3
        time_taken_str = f"{time_taken:.03f}" + config.HIGHTLIGHT_STYLE + " ms"
        if(time_taken > 1000):
            time_taken_str = f"{time_taken/1000:.03f}" + config.HIGHTLIGHT_STYLE + " s"
        
        day_range = (end_date - start_date).days
        print("\n" + config.HIGHTLIGHT_STYLE + "Found " + config.HEADER_STYLE + str(all_times_found) + config.HIGHTLIGHT_STYLE + " results in " + config.HEADER_STYLE + str(day_range - invalid_files) + config.HIGHTLIGHT_STYLE + " files out of " + config.HEADER_STYLE + str(day_range - no_written_files) + config.HIGHTLIGHT_STYLE + " written files in range of " + config.HEADER_STYLE + str(day_range) + config.HIGHTLIGHT_STYLE + " days in " + config.HEADER_STYLE + time_taken_str + "\n")
