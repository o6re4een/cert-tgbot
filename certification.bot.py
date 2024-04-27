import telebot
import config
import dbworker
import os
import uuid

SAVE_DIR = 'pdfs'
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.send_message(message.chat.id, "Привет я бот для создания сертификатов введите имя участника")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_NAME.value)
    print(message.text)

bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Вы в чем-то ошибилсь давайте заново введем")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_NAME.value)
    print(message.text)
    
@bot.message_handler(commands=["sender"])
def start_sender(message):
    bot.send_message(message.chat.id, "Давай пдфочку")
@bot.message_handler(content_types=['document'])
def handle_document(message):
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
        file_path = os.path.join(SAVE_DIR, unique_filename)
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Respond to the user
        bot.reply_to(message, f"Document '{file_name}' ({file_size} bytes) received and saved with unique filename: {unique_filename}")

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_NAME.value)
def user_entering_score(message):
    bot.send_message(message.chat.id, "Вы указали имя давайте перейдем к баллам за олимпиаду ")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_SCORE.value)
    print(message.text)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_SCORE.value)
def user_entering_date(message):
    bot.send_message(message.chat.id, "Вы указали баллы введите дату мероприятия ")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_DATE.value)
    print(message.text)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_DATE.value)
def user_entering_win(message):
    bot.send_message(message.chat.id, "Успех!")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_CONG.value)
    print(message.text)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_CONG.value)
def pdf_sender_to(message):
    bot.send_message(message.chat.id, "Files incoming")
    document_path='367289300_860.pdf'
    with open(document_path, 'rb') as document:
        bot.send_document(message.chat.id, document)

bot.infinity_polling()
