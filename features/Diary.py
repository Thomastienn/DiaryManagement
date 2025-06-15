import os, utils.config, calendar, time, storage, dbop, cv2
from datetime import datetime, timedelta
from Feature import Feature
from utils.TextFile import TextFile
from unidecode import unidecode
import matplotlib.pyplot as plt
# from Milestone import Milestone

class Diary(Feature):
    def __init__(self, dir: str) -> None:
        super().__init__(dir)
        
    def get_menu(self):
        return config.DIARY_MENU
    
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
                if(unknown_words):
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
                            config.classifying_mode = False
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
                storage.update_latest()
            else:
                self.printTitle(date_title, style=config.DAYTIME_STYLE)
                self.__print_note(cur_today.strftime("%d-%m-20%y"))
                decrypted_message = cur_today_file.decrypt_file()
                processed_txt = self.iterate_txt(decrypted_message)
                text = processed_txt["content"]
                if(text):
                    print(text + "\n")
                    
                total_str = (config.HIGHTLIGHT_STYLE + " = " + config.HEADER_STYLE + str(sum(processed_txt["n_words"])) if processed_txt["previous_content"] else "")
                
                print(config.HIGHTLIGHT_STYLE + "Words: " + config.HEADER_STYLE + (" | ".join(map(lambda x: str(x), processed_txt["n_words"]))) + total_str)
                print(config.HIGHTLIGHT_STYLE + "Previous days: " + config.HEADER_STYLE + str(processed_txt["previous_content"]))

            if(config.classifying_mode):
                os.system("cls")
                self.printTitle(date_title, style=config.DAYTIME_STYLE)
            
            cur_td_str = cur_today.strftime("%d-%m") 
            TODAY_IMAGE_DIR = f"{config.DIARY_DIR}\\{config.current_year}\\Images\\{cur_td_str}"
            files = []
            if(os.path.exists(TODAY_IMAGE_DIR)):
                files = os.listdir(TODAY_IMAGE_DIR)
            print(config.HIGHTLIGHT_STYLE + "Images: " + config.HEADER_STYLE + str(len(files)) + "\n")
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
            elif(user_choose == "ms"):
                print()
                for milestone_category in config.MILESTONE_SUB_MENU:
                    file_name = milestone_category.replace(" ", "_")
                    file_dir = f"{config.DIARY_DIR}\\{cur_today_year}\\Milestone\\{file_name}.txt"
                    
                    file_read = TextFile(full_dir = file_dir)
                    
                    hl_text = config.highlight_text
                    config.highlight_text = False
                    self.process_find_in_text_file(
                        find_file=file_read,
                        search_str= [f"{cur_today_day_month}-{cur_today_year}".replace("-", "/")],
                        accent_mark=True,
                        case_sensitive=True,
                        title=f"{milestone_category}",
                        normalization=False,
                        whole_word=False,
                        display_none= False,
                        highlight_found=False
                    )
                    config.highlight_text = hl_text
                    
                input(config.HIGHTLIGHT_STYLE +  "\nFINISHED")
            elif(user_choose == "note"):
                note_content = input("Note something: ")
                timestamp = datetime.now().strftime("[%d/%m/20%y %H:%M:%S]") + ": "
                encrypted_content = TextFile.encrypt_mes(timestamp + note_content)
                
                note_db = dbop.get_database(config.NOTES_DB)
                cur_date = cur_today.strftime("%d-%m-20%y")
                
                if(cur_date not in note_db):
                    note_db[cur_date] = [encrypted_content]
                else:
                    note_db[cur_date] += [encrypted_content]
                    
                dbop.write_database(note_db, config.NOTES_DB)
            elif(user_choose == "img"):
                for i, f in enumerate(files):
                    img = TextFile.decrypt_image(path=TODAY_IMAGE_DIR, name=f)
                    np_img = TextFile.process_img(img)
                    cv2.imshow(f"{i+1}/{len(files)}", np_img)
                        
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            elif(user_choose == "srch"):
                find_txt = input("What you wanna find?: " + config.HEADER_STYLE)
                today_date = cur_today.strftime("%d-%m-20%y")
                today_range = today_date + " " + today_date
                self.find(find_txt, exact=False, case_sensitive=False, accent_mark=False, normalization=False, whole_word=False, day_range=today_range, show_stats=False, show_details=False)
                
                input("\nFinished")
            elif(user_choose == "hl"):
                config.highlight_text = not config.highlight_text
            elif(user_choose == "bs"):
                config.break_sentence = not config.break_sentence
            elif(user_choose == "help"):
                self.print_full_guide()
            else:
                try:
                    cur_today = datetime.strptime(self.__to_format_datetime(user_choose), "%d-%m-%y")
                except ValueError:
                    break
    
    def __print_note(self, date_str) -> None:
        note_db = dbop.get_database(config.NOTES_DB)
        if(date_str not in note_db):
            return
        
        self.printTitle(mes="NOTE", style=config.DAYTIME_STYLE)
        note_content = note_db[date_str]
        for content in note_content:
            print("-", TextFile.decrypt_mes(content))
        print()
    
    def __list_unknown_capital_words(self, text_file: TextFile) -> list:
        storage.update_latest()
        
        decrypted_message = text_file.decrypt_file()
        if(not decrypted_message):
            return
        
        res = []
        first_word_line = False
        is_time_stamp = False
        
        for word in decrypted_message.split(" "):
            if(not word):
                continue
            
            if(is_time_stamp and ("[" not in word and "]" not in word)):
                first_word_line = True
                
            is_time_stamp = False
            
            if("[" in word or "]" in word):
                is_time_stamp = True
                
            if(word[0].isupper() and not is_time_stamp and not first_word_line):
                if(unidecode(word.lower()) not in storage.people and unidecode(word.lower()) not in storage.places and word not in storage.people and word not in storage.places):
                    res.append(word)

            if(first_word_line):
                first_word_line = False
            
        return res
                
    
    def __datetime_to_month_year(self, date_time: datetime):
        return (date_time.strftime("%d-%m"), date_time.strftime("20%y"))
    
    def __to_format_datetime(self, string_datetime: str) -> str:
        return string_datetime[:-5] + "-" + string_datetime[-2:]
    
    def find(self, find_str: str, exact: bool, case_sensitive: bool, accent_mark: bool, normalization: bool, whole_word: bool, day_range:str = None, show_stats: bool = True, show_details: bool = True, same_date: bool = False) -> None:
        if(show_details):
            self.printHeader(config.MENU_WIDTH)
        
        user_range = day_range
        if(not day_range):
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
                end_date = datetime(day=1, month=1, year=int(int(end[1:]) + 1))
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
        
        # Counting
        all_times_found = 0
        invalid_files = 0
        no_written_files = 0
        start_time = time.time()
        
        # Plotting purposes
        days_range = []
        words_frequency = []
        write_frequency = []
        each_word_frequency = {}
        
        while current_date != end_date:
            days_range.append(current_date)
            cur_today_day_month, cur_today_year = self.__datetime_to_month_year(current_date)
            cur_today_file_upper_dir = config.DIARY_DIR + "\\" + cur_today_year
            current_date_file = TextFile(upper_dir=cur_today_file_upper_dir,
                                         file_name=cur_today_day_month)
            
            res_dic = self.process_find_in_text_file(
                find_file=current_date_file,
                search_str=search_str,
                accent_mark=accent_mark,
                case_sensitive=case_sensitive,
                title=f"{cur_today_day_month}-{cur_today_year}",
                normalization=normalization,
                whole_word=whole_word,
                highlight=False,
                show_details=show_details,
                same_date=same_date
            )
            times_found = res_dic["times_found"]
            is_written = res_dic["is_written"]
            word_freq = res_dic["word_freq"]
            
            for word, freq in word_freq.items():
                if word not in each_word_frequency:
                    each_word_frequency[word] = freq
                else:
                    each_word_frequency[word] += freq

            words_frequency.append(times_found)
            if(times_found):
                all_times_found += times_found
            else:
                invalid_files += 1
                
            if(not is_written):
                no_written_files +=  1
                write_frequency.append(0)
            else:
                write_frequency.append(1)
            
            current_date = current_date + timedelta(days=1)
        
        if(not show_stats):
            input()
            return
        
        end_time = time.time()
        time_taken = (end_time-start_time)*10**3
        time_taken_str = f"{time_taken:.03f}" + config.HIGHTLIGHT_STYLE + " ms"
        if(time_taken > 1000):
            time_taken_str = f"{time_taken/1000:.03f}" + config.HIGHTLIGHT_STYLE + " s"
        
        day_range = (end_date - start_date).days
        print("\n" + config.HIGHTLIGHT_STYLE + "Found " + config.HEADER_STYLE + str(all_times_found) + config.HIGHTLIGHT_STYLE + " results in " + config.HEADER_STYLE + str(day_range - invalid_files) + config.HIGHTLIGHT_STYLE + " files out of " + config.HEADER_STYLE + str(day_range - no_written_files) + config.HIGHTLIGHT_STYLE + " written files in range of " + config.HEADER_STYLE + str(day_range) + config.HIGHTLIGHT_STYLE + " days in " + config.HEADER_STYLE + time_taken_str + "\n")
        
        print(config.HIGHTLIGHT_STYLE + "Word Map")
        for word,freq in each_word_frequency.items():
            print(config.HIGHTLIGHT_STYLE + word + " | " + config.HEADER_STYLE + str(freq))
        print()
        
        try:
            print(config.HIGHTLIGHT_STYLE + "Completed days is " + config.HEADER_STYLE + str(round((day_range - no_written_files)/(day_range)*10000)/100) + "%")
        except ZeroDivisionError:
            pass
            
        try:
            print(config.HIGHTLIGHT_STYLE + "Chance occurs in a day is " + config.HEADER_STYLE + str(round((day_range - invalid_files)/(day_range - no_written_files)*10000)/100) + "%")
        except ZeroDivisionError:
            pass
            
        try:
            print(config.HIGHTLIGHT_STYLE + "Average words in day is " + config.HEADER_STYLE + str(round((all_times_found)/(day_range - invalid_files)*10)/10) + config.HIGHTLIGHT_STYLE  + " words")
        except ZeroDivisionError:
            pass
            
        try:
            print(config.HIGHTLIGHT_STYLE + "Search speed is " + config.HEADER_STYLE + str(round((time_taken/1000)/(day_range - no_written_files)*1000)/1000) + config.HIGHTLIGHT_STYLE  + " s/day")
        except ZeroDivisionError:
            pass
        
        fig, axes = plt.subplots(2, sharex=True)
        fig.supxlabel("Date")
        
        axes[0].step(days_range, words_frequency) 
        axes[0].set_ylabel("Words in a day")
        
        axes[1].step(days_range, write_frequency)
        axes[1].set_ylabel("Has written")
        
        fig.autofmt_xdate()
        fig.show()
        
        print()
    
    def valid_file(self):
        self.printHeader(config.MENU_WIDTH)
        print("DD-MM-YYYY DD-MM-YYYY")
        print(config.HEADER_STYLE + "-"*config.MENU_WIDTH)
        user_range = input("Range: ")
        
        start_end = user_range.split(" ")
        
        start_date = None
        end_date = None
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
                end_date = datetime(day=1, month=1, year=int(int(end[1:]) + 1))
            elif(end[0] == "m"):
                next_month = int(end[1:]) + 1
                if(next_month == 13):
                    next_month = 1
                end_date = datetime(day=1, month=next_month, year=int(config.current_year))
            else:
                end_date = datetime.strptime(self.__to_format_datetime(end), "%d-%m-%y")
        
        current_date = start_date
        while current_date != end_date:
            cur_today_day_month, cur_today_year = self.__datetime_to_month_year(current_date)
            cur_today_file_upper_dir = config.DIARY_DIR + "\\" + cur_today_year
            current_date_file = TextFile(upper_dir=cur_today_file_upper_dir,
                                         file_name=cur_today_day_month)
            
            all_text_day = current_date_file.decrypt_file()
            if(all_text_day == None):
                current_date = current_date + timedelta(days=1)
                continue
            title = f"{cur_today_day_month}-{cur_today_year}"
            self.printTitle(title,style=config.DAYTIME_STYLE)
            
            current_date = current_date + timedelta(days=1)
        
