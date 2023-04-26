import config 
word = "Hi"

a = config.normalize_language_with_accent_mark.get(word.lower())

print(a)