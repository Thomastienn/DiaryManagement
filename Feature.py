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
    def find(self, find_str, exact, case_sensitive, accent_mark, normalization, whole_word) -> None:
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
    
    def iterate_txt(self, text: str, highlight: bool = True) -> str: 
        final = []
        start_line = False
        for word in text.split(" "):
            if(not word):
                continue
            res = word
            processed = False
            is_time_stamp = True
            
            if(config.use_normalize_text):
                res = self.__normalize_text(word)
            
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
            
            findRes = word.find("\n")
            addition_word = ""
            if(("[" not in word and "]" not in word) and findRes != -1):
                res = res[:findRes] + res[findRes+1:]
            elif(("[" in word or "]" in word) and findRes != -1):
                splited = word.split("\n")
                if(splited[0]):
                    res = word[:findRes]
                    addition_word = "\n" + config.TIMESTAMP_STYLE + word[findRes+1:] + config.DEFAULT_STYLE
            
            if(highlight):
                if(self.__normalize_text(word) in storage.people or
                    unidecode(word.lower()) in storage.people):
                    res = config.PEOPLE_STYLE + word + config.DEFAULT_STYLE
                elif(self.__normalize_text(word) in storage.places or
                    unidecode(word.lower()) in storage.places):
                    res = config.PLACES_STYLE + word + config.DEFAULT_STYLE
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
                
            final.append(res)
            if(addition_word):
                final.append(addition_word)
        
        return " ".join(final)
    
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
                
    
    def preprocess_find_str(self, find_str, case_sensitive, accent_mark, exact) -> list:
        if(not case_sensitive):
            find_str = find_str.lower()
        if(not accent_mark):
            find_str = unidecode(find_str)
        search_str = []
        if(not exact):
            search_str = find_str.split(" ")

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
            
            search_str = res
        else:
            search_str.append(find_str)
            
        return search_str
       
    # Return
    # First in the set is TIMES_FOUND
    # Second is the boolean if there is a file
    
    def process_find_in_text_file(self, find_file: TextFile, search_str, accent_mark, case_sensitive, title, normalization, whole_word, display_none: True) -> set:
        all_text_day = find_file.decrypt_file()
        if(not all_text_day):
            return (0, False)
        if(normalization):
            all_text_day = " ".join([self.__normalize_text(word) for word in all_text_day.split(" ")])
        
        immutable_all_text_day = all_text_day
        if(not accent_mark):
            all_text_day = unidecode(all_text_day)
        
        if(not case_sensitive):
            all_text_day = all_text_day.lower()
            
        found_dict = self.find_all(all_text_day, search_str, whole_word)
        
        times_found = 0
        if(len(found_dict) != 0):
            all_lines_found = self.index_occ_to_start_line(immutable_all_text_day, found_dict)
            self.printTitle(title, style=config.DAYTIME_STYLE)
            print(self.iterate_txt("".join(all_lines_found)))
            times_found += len(found_dict)
        else:
            if(display_none):
                print(config.NONE_STYLE + title + " NONE")
            
        return (times_found, True)
        
    def index_occ_to_start_line(self, text: str, occ_dict: dict) -> list:
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
                final += text[prev_occ:occ] + config.FOUND_STYLE + text[occ:occ + len(word)] + config.DEFAULT_STYLE
                
                prev_occ = occ + len(word)
            
            final += text[prev_occ: end]
            res.append(final)
            
        return res
        
    