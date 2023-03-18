from TextFile import TextFile
import config, os

dir = config.DIARY_DIR + "\\2025"
write_file = TextFile(upper_dir=dir, file_name="Test")
write_file.write_file("Hello")