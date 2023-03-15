from datetime import datetime

user_choose = ""
cur_today = datetime.strptime(user_choose[:-5] + "-" + user_choose[-2:], "%d-%m-%y")