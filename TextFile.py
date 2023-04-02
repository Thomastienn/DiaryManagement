import rsa, ast, os
import config
from pathlib import Path

class TextFile:
    def __init__(self, upper_dir: str = None, file_name: str = None, full_dir: str = None) -> None:
        if full_dir:
            self.dir = full_dir
            return
        if(not upper_dir or not file_name):
            raise TypeError("Insufficient parameters") 
        file_name = file_name
        self.dir = upper_dir + "\\" + file_name + ".txt"

    def decrypt_file(self) -> str:
        # Get private key
        with open(config.PRIVATE_KEYS_DIR, 'rb') as key_file:
            private_key = rsa.PrivateKey.load_pkcs1(key_file.read())

        # If there is the file
        try:
            with open(self.dir, 'rb') as f:
                ciphertext = f.read()
                list_of_lines = ciphertext.decode("utf-8").split("\n")

                return self.__decrypt_lines_text(lines=list_of_lines, private_key=private_key)
            
        except (FileNotFoundError, FileExistsError):
            return None
        
    def write_file(self, text: str) -> None:
        upper_path = os.path.dirname(Path(self.dir))
        if(not os.path.exists(upper_path)):
            os.mkdir(upper_path)
        
        # Get public key
        with open(config.PUBLIC_KEYS_DIR, "rb") as key_file:
            public_key = rsa.PublicKey.load_pkcs1(key_file.read())

        for piece in self.__break_long_string_into_list(text):
            # piece: string -> into message: byte
            message = piece.encode("utf-8")
            encrypted_text = rsa.encrypt(message, public_key)

            # Create a new file if it's not existed
            mode = "a" if os.path.exists(self.dir) else "w"

            # Write the string representation of the byte
            with open(self.dir, mode, encoding="utf-8") as file:
                file.write(str(encrypted_text) + "\n")
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

        MAX_BYTES = 240
        
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