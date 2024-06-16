import telebot
from cert_builder import process_create_certificate,create_custom_cert
import config
import dbworker
import os
import uuid

SAVE_DIR = 'pdfs'
SAVE_TXTS_DIR = 'txts' 
SAVE_TEMPLATE_DIR = 'templates'
output_dir = "certificates"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

if not os.path.exists(SAVE_TXTS_DIR):
    os.makedirs(SAVE_TXTS_DIR)
    

bot = telebot.TeleBot(config.token)


user_data: dict[str, dict[str, str]] = dict()

@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.send_message(message.chat.id, "Привет я бот для создания сертификатов введите имя участника или пришлите данные в формате \n name title date \n name title date")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_NAME.value)
    print(message.text)

@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Данные сброшены, давайте заново введите имя участника или пришлите данные в формате \n name title date \n name title date")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_NAME.value)
    print(message.text)
    print("SSSDSADASD")
  
@bot.message_handler(commands=["sender"])
def start_sender(message):
    bot.send_message(message.chat.id, "Давай пдфочку")


@bot.message_handler(commands=["custom"])
def process_custom_cert(message):
    dbworker.set_state(message.chat.id, config.States.S_CUSTOM_CERT_WAIT_FOR_TEMPLATE.value)
    bot.send_message(message.chat.id, "Вы приступили к созданию уникального сертификата \n В процессе создания сертификата нужно будет отправить шаблон, затем отправить шаблонные выражения которые нужно заменить, затем отправить замену, \b разделение через  ; \b  \b \n Количество шаблонов и замен должно быть одинаково \n \b Для начала отправьте шаблон в формате фотографии  \n")



@bot.message_handler(func = lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_CUSTOM_CERT_WAIT_FOR_TEMPLATE.value, content_types=['photo'])
def handle_custom_certificate_template(message):
    # Check if the document is present in the message
    if message.photo is not None:
        # Get information about the photo
        file_info = bot.get_file(message.photo[-1].file_id)
       

        # Download the document
        
        downloaded_file = bot.download_file(file_info.file_path)

        # Generate a unique filename for the document
        unique_filename = str(uuid.uuid4()) + '_' + 'custom_cert_template.jpg'

        file_path = os.path.join(SAVE_TEMPLATE_DIR, unique_filename)
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        user_data.get(str(message.chat.id))
        if(str(message.chat.id) not in user_data):
            user_data[str(message.chat.id)] = dict()
        user_data[str(message.chat.id)]['custom_cert_template_path'] = file_path
        dbworker.set_state(message.chat.id, config.States.S_CUSTOM_CERT_WAIT_FOR_TEMPLATE_STR.value)
        bot.send_message(message.chat.id, "Отлично, теперь введите шаблонные выражения, разделенные ; ")
    else:
        bot.send_message(message.chat.id, "Вы не прислали шаблон в формате фотографии, попробуйте отправить еще раз")

@bot.message_handler(func = lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_CUSTOM_CERT_WAIT_FOR_TEMPLATE_STR.value, content_types=['text'])
def handle_custom_certificate_template_str(message):
    user_data[str(message.chat.id)]['custom_cert_template_str'] = message.text
    dbworker.set_state(message.chat.id, config.States.S_CUSTOM_CERT_WAIT_FOR_REPLACEMENT_STR.value)
    bot.send_message(message.chat.id, "Отлично, теперь введите замены, разделенные ; ")


@bot.message_handler(func = lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_CUSTOM_CERT_WAIT_FOR_REPLACEMENT_STR.value, content_types=['text'])
def handle_custom_certificate_replacement_str_generate_cert(message):
    user_data[str(message.chat.id)]['custom_cert_replacement_str'] = message.text
    
    bot.send_message(message.chat.id, "Отлично, приступаем к генерации сертификатов, ожидайте ...")
    custom_template_path = user_data[str(message.chat.id)]['custom_cert_template_path']
    custom_template_str = user_data[str(message.chat.id)]['custom_cert_template_str']
    custom_replacement_str = user_data[str(message.chat.id)]['custom_cert_replacement_str']

    unique_filename = str(uuid.uuid4()) + '_' + 'AAAAAAAAAAAAAAAAA'
    output_pdf_path = os.path.join(output_dir, f"{unique_filename}_certificate.pdf")
    cert_path = create_custom_cert(
        custom_data_text=custom_replacement_str,
        custom_search_text=custom_template_str,
        custom_template_path=custom_template_path,
        output_path=output_pdf_path
    )
    send_cert([cert_path], message)
    reset_state(message)
   

#Обработка тексовых докуметов (batch processing) 
@bot.message_handler(func = lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_NAME.value, content_types=['document'])
def handle_user_document_names(message):
    # Check if the document is present in the message
    if message.document is not None:
        # Get information about the document
        document_id = message.document.file_id
        file_name = message.document.file_name
        file_size = message.document.file_size

        # Download the document
        file_info = bot.get_file(document_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Generate a unique filename for the document
        unique_filename = str(uuid.uuid4()) + '_' + file_name

        # Save the document with the unique filename
        file_path = os.path.join(SAVE_TXTS_DIR, unique_filename)
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        user_cert_datas = read_txt_file(file_path)

        
        cert_paths_array = process_create_certificate(user_cert_datas)
        
        #function to read txt file with name title date
        
        

        # Respond to the user
        bot.reply_to(message, f"Document '{file_name}' ({file_size} bytes) received and saved with unique filename: {unique_filename}, certs will send to u")

        send_cert(cert_paths_array, message)
        reset_state(message)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_NAME.value)
def user_entering_score(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Вы указали имя давайте перейдем к названию мероприятия ")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_TITLE.value)
    user_data.get(str(message.chat.id))
    if(str(message.chat.id) not in user_data):
        user_data[str(message.chat.id)] = dict()
    user_data[str(message.chat.id)]['name'] = message.text
    # print(message.text)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_TITLE.value)
def user_entering_date(message):
    bot.send_message(message.chat.id, "Вы указали название введите дату мероприятия ")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_DATE.value)

    user_data[str(message.chat.id)]['title'] = message.text
    


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_DATE.value)
def user_entering_win(message):
    bot.send_message(message.chat.id, "Успех!")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_CONG.value)
    user_data[str(message.chat.id)]['date'] = message.text
    pdf_sender_to(message)
    # print(message.text)

# @bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_CONG.value)
def pdf_sender_to(message):
    bot.send_message(message.chat.id, "Files incoming")
    # data = dbworker.get_current_state(message.chat.id)

    user_data = get_user_data(message.chat.id)
    
    certs = process_create_certificate([user_data])
    send_cert(certs, message)
    
    
    # document_path='367289300_860.pdf'
    
   

    reset_state(message)

def send_cert(cets_path_array: list[str], message)->None:
    try:
        for cert in cets_path_array:
            with open(cert, 'rb') as document:
                bot.send_document(message.chat.id, document)
    except Exception as e:
        print(e)

def reset_state(message):
    bot.send_message(message.chat.id, "Готово, вы вернулись в начало")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_NAME.value)
    
    
def read_txt_file(file_path):
    user_cert_datas = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            data_list = line.split(";")
            name = data_list[0].strip()
            title = data_list[1].strip()
            date = data_list[2].strip()
            user_cert_datas.append({
                'name': name,
                'title': title,
                'date': date
            })

    return user_cert_datas
        


def get_user_data(chat_id):
    return user_data.get(str(chat_id))



bot.infinity_polling()
