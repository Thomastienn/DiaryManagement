import os
import config
from abc import abstractmethod
from TextFile import TextFile
from unidecode import unidecode
import storage
from autocorrect import Speller
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
    def find(self, find_str, exact, case_sensitive, accent_mark, normalization, whole_word, same_date) -> None:
        pass
    
    def find_all(self, origin: str, list_sub: list, whole_word: bool) -> dict:
        all_occurences = {}
        
        for sub in list_sub:
            start = 0
            while True:
                index = origin.find(sub, start)
                if index == -1:
                    break
                if(whole_word):
                    if((index-1 < 0 or origin[index-1] in {" ", "\n"}) and \
                       (index+1 >= len(origin) or origin[index + len(sub)] in {" ", "\n"})):
                            all_occurences[index] = sub
                else:
                    all_occurences[index] = sub
                
                start = index + 1
                
        return all_occurences
    
    def printMenu(self, menu: list) -> None:
        width = config.MENU_WIDTH
        self.printHeader(width)
        print(config.select_valid_header_style() + "0 |" + config.FUNCTION_STYLE + " Exit")
        for i in range(len(menu)):
            print(config.select_valid_header_style() + str(i+1) + (" " if (i+1) < 10 else "") + "| " + config.FUNCTION_STYLE + menu[i])
        print(config.select_valid_header_style() + "-"*width)

    def printTitle(self, mes: str, style=config.DEFAULT_STYLE) -> None:
        width = config.TITLE_WIDTH
        print(style + "-"*width)
        print(style + str(mes).center(width, " "))
        print(style + "-"*width)
        
    def printHeader(self, width):
        print(config.select_valid_header_style() + self.__class__.__name__.center(width, "-"))
    
    def iterate_txt(self, text: str) -> str: 
        if(not text):
            return {
                "content": "",
                "n_words": [0],
                "previous_content": False
            }
        final = []
        start_line = False
        num_words = 0
        num_words_l = []
        has_many_days_content = False
        for word in text.split(" "):
            if(not word):
                continue
            res = word
            processed = False
            is_time_stamp = True
            
            if(config.use_normalize_text):
                res = self.__normalize_text(word)
            
            if(config.break_sentence and "." in word):
                res += "\n"
            
            if("[" in word and config.DEFAULT_STYLE not in word
               and config.FOUND_STYLE not in word):
                for idx, character in enumerate(word):
                    if(character == "]"):
                        # 2 is ] and :
                        res = config.TIMESTAMP_STYLE + word[:idx + 2] + config.DEFAULT_STYLE
                        processed = True
                        break
                res = config.TIMESTAMP_STYLE + word + config.DEFAULT_STYLE
                
            if("]" in word and config.DEFAULT_STYLE not in word):
                start_line = True
                if(not processed):
                    res = config.TIMESTAMP_STYLE + word + config.DEFAULT_STYLE
            else:
                is_time_stamp = False
                num_words += 1
            
            findRes = word.find("\n")
            addition_word = ""
            if(("[" not in word and "]" not in word) and findRes != -1):
                res = res[:findRes] + res[findRes+1:]
            elif(("[" in word or "]" in word) and findRes != -1):
                splited = word.split("\n")
                if(splited[0]):
                    num_words += 1
                    res = word[:findRes]
                    addition_word = "\n" + config.TIMESTAMP_STYLE + word[findRes+1:] + config.DEFAULT_STYLE
            
            if(config.highlight_text):
                if(self.__normalize_text(word) in storage.people or
                    unidecode(word.lower()) in storage.people):
                    res = config.PEOPLE_STYLE + word + config.DEFAULT_STYLE
                elif(self.__normalize_text(word) in storage.places or
                    unidecode(word.lower()) in storage.places):
                    res = config.PLACES_STYLE + word + config.DEFAULT_STYLE
                elif(word.isdigit()):
                    res = config.NUMBERIC_STYLE + word + config.DEFAULT_STYLE
                elif(word[0].isupper() and not start_line):
                    if(self.__normalize_text(word) in storage.capital_people or
                    unidecode(word.lower()) in storage.capital_people):
                        res = config.PEOPLE_STYLE + word + config.DEFAULT_STYLE
                    else:
                        res = config.UNCERTAIN_STYLE + res + config.DEFAULT_STYLE
            
            if(not is_time_stamp):
                start_line = False 
                
            if("---" in word):
                res = config.TIMESTAMP_STYLE + word + config.DEFAULT_STYLE
                has_many_days_content = True
                num_words_l.append(num_words)
                num_words = 0
             
            final.append(res)
            if(addition_word):
                final.append(addition_word)
        
        num_words_l.append(num_words)
        return {
            "content": (" ".join(final)),
            "n_words": num_words_l,
            "previous_content": has_many_days_content
        }
    
    def __normalize_text(self, word: str) -> str:
        if not config.use_annotate_normalize:
            new_text = storage.normalize_language_with_accent_mark.get(word.lower(), word)
            res_text = storage.normalize_language_no_accent_mark.get(unidecode(new_text).lower(), new_text)
            
            return res_text
        
        res = storage.normalize_language_with_accent_mark.get(word.lower())
        if(res is None):
            res = storage.normalize_language_no_accent_mark.get(unidecode(word).lower())

            res = (config.TRUE_STYLE + res + config.FALSE_STYLE + "(" + word + ")") if res is not None else (config.DEFAULT_STYLE + word)
        else:
            res = config.TRUE_STYLE + storage.normalize_language_no_accent_mark.get(unidecode(res).lower() , res) + config.FALSE_STYLE + "(" + word + ")"
        
        return res
              
    def process_wrapping(self, search_str: list) -> str:
        res = []
        i = 0
        while i < len(search_str):
            t = search_str[i]
            
            if("(" in t):
                full_str = t[1:]
                if(")" in t):
                    full_str = full_str[:-1]
                else:
                    for j in range(i+1, len(search_str)):
                        t_1 = search_str[j]
                        if(")" in t_1):
                            full_str += " " + t_1[:-1]
                            i = j
                            break
                        else:
                            full_str += " " + t_1
                res.append(full_str)
            else:
                
                res.append(t)
                        
            i+=1
        return res
    
    def preprocess_find_str(self, find_str, case_sensitive, accent_mark, exact) -> list:
        if(not case_sensitive):
            find_str = find_str.lower()
        if(not accent_mark):
            find_str = unidecode(find_str)
        search_str = []
        if(not exact):
            search_str = find_str.strip().split(" ")
            search_str = self.process_wrapping(search_str)
        else:
            search_str.append(find_str)
            
        return search_str
       
    # Return
    # First in the set is TIMES_FOUND
    # Second is the boolean if there is a file
    
    def process_find_in_text_file(self, find_file: TextFile, search_str, accent_mark, case_sensitive, title, normalization, whole_word, display_none = True, highlight = True, highlight_found = True, show_details: bool = True, same_date: bool = False) -> set:
        all_text_day = find_file.decrypt_file()
        if(not all_text_day):
            return {
                "times_found": 0,
                "is_written": False,
                "word_freq": {}
            }
        if(normalization):
            all_text_day = " ".join([self.__normalize_text(word) for word in all_text_day.split(" ")])
        
        immutable_all_text_day = all_text_day
        if(not accent_mark):
            all_text_day = unidecode(all_text_day)
        
        if(not case_sensitive):
            all_text_day = all_text_day.lower()
            
        found_dict = self.find_all(all_text_day, search_str, whole_word)
        
        all_find_str_in_same_date = True
        if(same_date):
            for find_str in search_str:
                if find_str not in found_dict.values():
                    all_find_str_in_same_date = False
                    
        times_found = 0
        word_freq = {}
        if(len(found_dict) != 0 and ((same_date and all_find_str_in_same_date) or (not same_date))):
            for word_found in found_dict.values():
                if word_found not in word_freq:
                    word_freq[word_found] = 1
                else:
                    word_freq[word_found] += 1
                
            all_lines_found = self.index_occ_to_start_line(immutable_all_text_day, found_dict, highlight_found=highlight_found)
            if(show_details):
                self.printTitle(title, style=config.DAYTIME_STYLE)
            res = self.iterate_txt("".join(all_lines_found))
            print(res["content"])
            times_found += len(found_dict)
        else:
            if(display_none):
                print(config.NONE_STYLE + title + " NONE")
            
        return {
            "times_found": times_found,
            "is_written": True,
            "word_freq": word_freq,
        }
        
    def index_occ_to_start_line(self, text: str, occ_dict: dict, highlight_found = True) -> list:
        pos_dic = {}
        for occ in occ_dict.keys():
            start_line_index = occ
            end_line_index = occ
            
            while(text[start_line_index] != "["):
                start_line_index -= 1
                
            try:
                while(text[end_line_index] != "["):
                    end_line_index += 1    
            except IndexError:
                end_line_index -= 1    
                
            if((start_line_index, end_line_index) in pos_dic):
                pos_dic[(start_line_index, end_line_index)] += [(occ, occ_dict[occ])]
            else:
                pos_dic[(start_line_index, end_line_index)] = [(occ, occ_dict[occ])]
            
        
        res = []
        
        for key in pos_dic.keys():
            start, end = key
            l_occ_word = pos_dic[key]
            final = ""
            prev_occ = start
            for occ_word in l_occ_word:
                occ, word = occ_word
                if(highlight_found):
                    final += text[prev_occ:occ] + config.FOUND_STYLE + text[occ:occ + len(word)] + config.DEFAULT_STYLE
                else:
                    final += text[prev_occ:occ + len(word)]
                
                prev_occ = occ + len(word)
            
            final += text[prev_occ: end]
            res.append(final)
            
        return res
        
    def print_full_guide(self):
        os.system("cls")
        MAX_WIDTH = 12
        
        def print_header(header):
            print(config.HEADER_STYLE + header)
        
        def print_guide(button, desc, style=config.HIGHTLIGHT_STYLE):
            print(style + button + (" "*(MAX_WIDTH-len(button))) + config.DEFAULT_STYLE + desc)
            
        print_header("NAV Guide")
        print_guide("a", "Shift the date back 1 day")
        print_guide("d", "Shift the date forward 1 day")
        print_guide("%d-%m-%y", "Switch to specific date")
        print_guide("anno", "Toggle annotation for normalization")
        print_guide("nor", "Toggle normalization")
        print_guide("hl", "Toggle highlighting text")
        print_guide("bs", "Toggle breaking sentences")
        print_guide("csf", "Toggle classifying mode (Classify into databases)")
        print_guide("ms", "Milestones in the current date")
        print_guide("note", "Add something to the note")
        print_guide("img", "Open images same date")
        print_guide("srch", "Search in same date")
        print_guide("help", "Display this guide")
        print()
        
        print_header("Classify Guide")
        print_guide("pe", "Classify into people database")
        print_guide("pl", "Classify into places database")
        print_guide("b", "Exit to NAV mode")
        print()
        
        print_header("Find Guide")
        print_guide("Set: 0", "Start finding")
        print_guide("Set: #", "Toggle setting on/off")
        print_guide("()", "Wrapping combined words (Exact must be false)")
        print()
        
        print_header("Range Shorcuts")
        print_guide("s", "The initial date of this diary")
        print_guide("td", "The date of today")
        print_guide("sy", "The first date of this year")
        print_guide("sm", "The first date of this month")
        print_guide("m#", "The first date of # month or #+1 month (depends on start or end range)")
        print_guide("y#", "The first date of # year or #+1 year (same as above)")
        print()
        
        print_header("Color Guide")
        print_guide("Color", "People", (config.PEOPLE_STYLE))
        print_guide("Color", "Places", (config.PLACES_STYLE))
        print_guide("Color", "Names", (config.UNCERTAIN_STYLE))
        print_guide("Color", "Numbers", (config.NUMBERIC_STYLE))
        print()
        
        print_header("Implicit Structure")
        print_guide("---", "Divide the days if you wanna write yesterday diary and then seperate from today diary")
        print_guide("Capital", "Mark as names")
        print()
        
        print()
        input("Press to continue...")