from enum import Enum
import os

token=os.environ['BOT_TOKEN']
db_file = "database.vdb"

class States(Enum):
    S_START = "0"  # Начало нового диалога
    S_ENTER_NAME = "1" #Ввод имени и фамлии
    S_ENTER_TITLE = "2" #Название мероприятия 
    S_ENTER_DATE = "3" #Дата проведения
    S_ENTER_CONG = "4" #Успех
    S_SEND_DOCS = "5" #Отправка файла


# class User():
#     def __init__(self):
#         self.name = ""
#         self.score = ""
#         self.date = ""
    
#     def set_state(self, value):
#         self.state = value
    
# user = User("sdds", "dsads", "sdasd")
# user.name = "sdad"