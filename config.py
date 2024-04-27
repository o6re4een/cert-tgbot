from enum import Enum
import os

token=os.environ['BOT_TOKEN']
db_file = "database.vdb"

class States(Enum):
    S_START = "0"  # Начало нового диалога
    S_ENTER_NAME = "1" #Ввод имени и фамлии
    S_ENTER_SCORE = "2" #Количество баллов
    S_ENTER_DATE = "3" #Дата проведения
    S_ENTER_CONG = "4" #Успех
    S_SEND_DOCS = "5" #Отправка файла