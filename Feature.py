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
    def find(self, find_str, exact, case_sensitive, accent_mark, normalization) -> None:
        pass
    
    def find_all(self, origin: str, list_sub: list) -> list:
        all_occurences = set()
        words = []
        
        for sub in list_sub:
            start = 0
            while True:
                index = origin.find(sub, start)
                if index == -1:
                    break
                
                if(index not in all_occurences):
                    words.append(sub)
                all_occurences.add(index)
                start = index + 1
        return list((list(all_occurences), words))
    
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
    
    def iterate_txt(self, text: str, normalize: bool = False, highlight: bool = True) -> str: 
        final = []
        for word in text.split(" "):
            res = word
            processed = False
            
            if("[" in word):
                for idx, character in enumerate(word):
                    if(character == "]"):
                        # 2 is ] and :
                        res = config.TIMESTAMP_STYLE + word[:idx + 2] + config.DEFAULT_STYLE
                        processed = True
                        break
                res = config.TIMESTAMP_STYLE + word + config.DEFAULT_STYLE
                
            if("]" in word and (not processed)):
                res = config.TIMESTAMP_STYLE + word + config.DEFAULT_STYLE
            
            if(normalize):
                res = self.__normalize_text(word)
            elif(highlight):
                if(self.__normalize_text(word, annotate=False) in storage.people or
                    unidecode(word.lower()) in storage.people):
                    res = config.PEOPLE_STYLE + word + config.DEFAULT_STYLE
                  
            final.append(res)
        
        return " ".join(final)
    
    def __normalize_text(self, word: str, annotate: bool = True) -> str:
        if not annotate:
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
            cur_str = ""
            for c in find_str:
                if(c == " " or c == ")"):
                    search_str.append(cur_str)
                    cur_str = ""
                elif(c != "("):
                    cur_str += c
                    
        else:
            search_str.append(find_str)
            
        return search_str
       
    # Return
    # First in the set is TIMES_FOUND
    # Second is the boolean if there is a file
    
    def process_find_in_text_file(self, find_file: TextFile, search_str, accent_mark, case_sensitive, title, normalization) -> set:
        all_text_day = find_file.decrypt_file()
        if(not all_text_day):
            return (0, False)
        if(normalization):
            all_text_day = " ".join([self.__normalize_text(word, annotate=False) for word in all_text_day.split(" ")])
        
        immutable_all_text_day = all_text_day
        if(not accent_mark):
            all_text_day = unidecode(all_text_day)
        
        if(not case_sensitive):
            all_text_day = all_text_day.lower()
            
        found, words = self.find_all(all_text_day, search_str)
        
        times_found = 0
        if(len(found) != 0):
            all_lines_found = self.index_occ_to_start_line(immutable_all_text_day, found, words)
            self.printTitle(title, style=config.DAYTIME_STYLE)
            print(self.iterate_txt("".join(all_lines_found)))
            times_found += len(found)
        else:
            print(config.NONE_STYLE + title + " NONE")
            
        return (times_found, True)
        
    def index_occ_to_start_line(self, text: str, occurences: list, words: list) -> list:
        start_lines = []
        end_lines = []
        for occ in occurences:
            start_line_index = occ
            end_line_index = occ
            
            while(text[start_line_index] != "["):
                start_line_index -= 1
                
            try:
                while(text[end_line_index] != "["):
                    end_line_index += 1    
            except IndexError:
                end_line_index -= 1    
                
            start_lines.append(start_line_index)
            end_lines.append(end_line_index)
        
        res = set()
        for start, end, occ, word in zip(start_lines, end_lines, occurences, words):
            res.add(text[start:occ] + config.FOUND_STYLE + text[occ:occ + len(word)] + config.DEFAULT_STYLE + text[occ + len(word): end])
            
        return list(res)
        
    