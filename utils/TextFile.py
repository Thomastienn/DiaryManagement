import rsa, ast, os, dbop, cv2
import config
from pathlib import Path
import numpy as np

class TextFile:
    def __init__(self, upper_dir: str = None, file_name: str = None, full_dir: str = None) -> None:
        if full_dir:
            self.dir = full_dir
            return
        if(not upper_dir or not file_name):
            raise TypeError("Insufficient parameters") 
        file_name = file_name
        self.dir = upper_dir + "\\" + file_name + ".txt"
    
    def decrypt_mes(encrypted_mes) -> str:
        if not config.has_valid_key:
            return ""
        with open(config.PRIVATE_KEYS_DIR, 'rb') as key_file:
            private_key = rsa.PrivateKey.load_pkcs1(key_file.read())
            
        return rsa.decrypt(ast.literal_eval(encrypted_mes), private_key).decode("utf-8")
    
    def encrypt_mes(mes) -> str:
        with open(config.PUBLIC_KEYS_DIR, "rb") as key_file:
            public_key = rsa.PublicKey.load_pkcs1(key_file.read())
        return str(rsa.encrypt(mes.encode("utf-8"), public_key))
        
    def stored_size(self):
        return os.path.getsize(self.dir)
    
    def is_existed(self) -> bool:
        try:
            with open(self.dir, "rb"):
                return True
        except (FileNotFoundError, FileExistsError):
            return False
        
    def get_image_key() -> int:
        return dbop.get_database(config.IMAGE_KEY_DIR)

    def encrypt_image(path: str, name: str, path_to: str):
        key = TextFile.get_image_key()
        
        fin = open(f"{path}\\{name}", 'rb')
        image = fin.read()
        fin.close()
        
        image = bytearray(image)
        for index, values in enumerate(image):
            image[index] = values ^ key

        fin = open(f"{path_to}\\{name}", 'wb')
        
        fin.write(image)
        fin.close()
    
    def process_img(image: bytearray):
        np_img = np.asarray(image, dtype=np.uint8)
        im = cv2.imdecode(np_img, cv2.IMREAD_COLOR) 
        
        resize_rate = config.RESOLUTION/len(im)
        w_re = int(len(im)*resize_rate)
        h_re = int(len(im[0])*resize_rate)
        im = cv2.resize(im, (h_re, w_re), interpolation=cv2.INTER_AREA)   
        
        return im
    
    def decrypt_image(path: str, name: str):
        key = TextFile.get_image_key()
        
        fin = open(f"{path}\\{name}", 'rb')

        image = fin.read()
        fin.close()
        image = bytearray(image)

        for index, values in enumerate(image):
            image[index] = values ^ key
        fin.close()
        
        return image
    
    def decrypt_file(self) -> str:
        # Get private key
        with open(config.PRIVATE_KEYS_DIR, 'rb') as key_file:
            private_key = rsa.PrivateKey.load_pkcs1(key_file.read())

        if(not self.is_existed()):
            return None
        
        with open(self.dir, 'rb') as f:
            ciphertext = f.read()
            list_of_lines = ciphertext.decode("utf-8").split("\n")

            return self.__decrypt_lines_text(lines=list_of_lines, private_key=private_key)
        
    def write_file(self, text: str, update_db = True) -> None:
        upper_path = os.path.dirname(Path(self.dir))
        if(not os.path.exists(upper_path)):
            os.mkdir(upper_path)
        
        # Get public key
        with open(config.PUBLIC_KEYS_DIR, "rb") as key_file:
            public_key = rsa.PublicKey.load_pkcs1(key_file.read())

        broken_pieces = self.__break_long_string_into_list(text)
        
        # 2: The extra length of \n and end line
        if(update_db):
            dbop.update_relative_database(config.STATS_DB, [\
            ("total_lines", len(broken_pieces)),\
            ("total_characters", len(text) + 2)])
        
        for piece in broken_pieces:
            # piece: string -> into message: byte
            message = piece.encode("utf-8")
            encrypted_text = rsa.encrypt(message, public_key)

            # Create a new file if it's not existed
            mode = "a" if os.path.exists(self.dir) else "w"

            # Write the string representation of the byte
            with open(self.dir, mode, encoding="utf-8") as file:
                file.write(str(encrypted_text) + "\n")
                if(update_db):
                    dbop.update_relative_database(config.STATS_DB, [\
                    ("total_storage", self.__utf8len(str(encrypted_text) + "\n") + 1)])
        print("Success")

    def __utf8len(self, s):
        return len(s.encode('utf-8'))

    def __decrypt_lines_text(self, lines: list, private_key) -> str:
        # Decrypt by each line
        final_text = ""
        for line in lines:
            # If the line is not empty
            if(line):
                try:
                    # line is string representation of byte
                    # Ex: b'ads\123\saf\bsbs'
                    # ast -> turns into real byte
                    plain_text = rsa.decrypt(ast.literal_eval(line), private_key)
                    final_text += plain_text.decode("utf-8") + "\n"
                except:
                    continue
        return final_text

    def __break_long_string_into_list(self, text) -> list:
        # Split text into list of words
        words_list = text.split(" ")

        MAX_BYTES = 230
        
        final_res = []
        curNumBytes = 0
        line_text = ""

        for word in words_list:
            real_word = word + " "
            curNumBytes += self.__utf8len(real_word)

            # If it exceeds MAX_BYTES then we have to break
            if(curNumBytes > MAX_BYTES):
                # Start a new string
                final_res.append(line_text)
                curNumBytes = 0
                line_text = ""
            line_text += real_word

        # There is still left in the line_text that 
        # hasn't been appended
        final_res.append(line_text)

        return final_res