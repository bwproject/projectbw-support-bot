import telebot
import logging

from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message

from config.settings import TG_TOKEN, TG_CHAT

from message.message import MESSAGE_START, MESSAGE_FAQ, MESSAGE_SUPPORT, MESSAGE_BOT

from message.button import BUT_FAQ, BUT_SUPPORT, BUT_BACK, BUT_MENU, BUT_BOT

from message.faq import FAQ_1, FAQ_1_1, FAQ_2, FAQ_2_1, FAQ_3, FAQ_3_1, FAQ_ALL, FAQ_ALL_1




#photo1 = open('img/5726DD2C-E438-4FD0-A371-0CE0CE6C4659.jpeg', 'rb')

print("Projectbw-bot")
print("https://github.com/bwproject/projectbw-support-bot")


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

# set the username or ID of the channel you want to get the ID for
# установите имя пользователя или идентификатор канала, для которого вы хотите получить идентификатор
target_chat_id = int(TG_CHAT)

# replace the token with your bot's token
# замените токен на токен вашего бота
bot = telebot.TeleBot(TG_TOKEN)

# define the custom keyboard
# определить пользовательскую клавиатуру
keyboard_main = ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
faq_button = KeyboardButton(BUT_FAQ)
support_button = KeyboardButton(BUT_SUPPORT)
bot_button = KeyboardButton(BUT_BOT)
keyboard_main.add(faq_button, support_button, bot_button)

keyboard_faq = ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)
faq1_button = KeyboardButton(FAQ_1)
faq2_button = KeyboardButton(FAQ_2)
faq3_button = KeyboardButton(FAQ_3)
faqall_button = KeyboardButton(FAQ_ALL)
main_menu_button = KeyboardButton(BUT_MENU)
keyboard_faq.add(faq1_button, faq2_button, faq3_button,faqall_button, main_menu_button)

keyboard_back = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
back_button = KeyboardButton(BUT_BACK)
keyboard_back.add(back_button, main_menu_button)

# define a handler for the /start command
# определяем обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    # set the welcome message adn the main menu keyboard
    bot.send_message(chat_id=message.chat.id, text=MESSAGE_START, reply_markup=keyboard_main, parse_mode='Markdown')

# define the message handler for the restart command
# определяем обработчик сообщений для команды перезапуска
@bot.message_handler(commands=['restart'])
def handle_restart(message):    
    # set the welcome message adn the main menu keyboard
    # установить приветственное сообщение и клавиатуру главного меню
    bot.send_message(chat_id=message.chat.id, text=MESSAGE_START, reply_markup=keyboard_main, parse_mode='Markdown')

# define the message handler for the "FAQ" message
# определяем обработчик сообщения "FAQ"
@bot.message_handler(func=lambda message: message.text == BUT_FAQ)
def handle_faq_option(message):
    bot.send_message(chat_id=message.chat.id, text=MESSAGE_FAQ, reply_markup=keyboard_faq, parse_mode='Markdown')

# define the message handler for the "FAQ#1" command
# определяем обработчик сообщений для команды "FAQ#1"
@bot.message_handler(func=lambda message: message.text == FAQ_1)
def faq_message(message):
    bot.reply_to(message,FAQ_1_1, reply_markup=keyboard_back, parse_mode='Markdown')

# define the message handler for the "FAQ#2" command
# определяем обработчик сообщений для команды "FAQ#2"
@bot.message_handler(func=lambda message: message.text == FAQ_2)
def faq_message(message):
    bot.reply_to(message, FAQ_2_1, reply_markup=keyboard_back, parse_mode='Markdown')    

# define the message handler for the "FAQ#3" command
# определяем обработчик сообщений для команды "FAQ#2"
@bot.message_handler(func=lambda message: message.text == FAQ_3)
def faq_message(message):
    bot.reply_to(message, FAQ_3_1, reply_markup=keyboard_back, parse_mode='Markdown')
    
# define the message handler for the "FAQ_ALL" command
# определяем обработчик сообщений для команды "FAQ ALL"
@bot.message_handler(func=lambda message: message.text == FAQ_ALL)
def faq_message(message):
    bot.reply_to(message, FAQ_ALL_1, reply_markup=keyboard_back, parse_mode='Markdown')   

@bot.message_handler(func=lambda message: message.text == BUT_BACK)
def handle_back_option(message):
    bot.send_message(chat_id=message.chat.id, text=MESSAGE_FAQ, reply_markup=keyboard_faq, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == BUT_MENU)
def handle_main_menu_option(message):
    bot.send_message(chat_id=message.chat.id, text=MESSAGE_START, reply_markup=keyboard_main, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == BUT_BOT)
def handle_main_menu_option(message):
    #bot.send_photo(chat_id=message.chat.id, photo=photo1, text=MESSAGE_BOT, reply_markup=keyboard_main, parse_mode='Markdown')  
    bot.send_message(chat_id=message.chat.id, text=MESSAGE_BOT, reply_markup=keyboard_main, parse_mode='Markdown')

# define the message handler for the "Support" message
# определяем обработчик сообщения "Поддержка"
@bot.message_handler(func=lambda message: message.text == BUT_SUPPORT)
def handle_support_option(message):
    bot.send_message(chat_id=message.chat.id, text=MESSAGE_SUPPORT, reply_markup=keyboard_back, parse_mode='Markdown')

##@bot.message_handler(chat_types=["private"])
@bot.message_handler(func=lambda message: message.chat.type == 'private', content_types=['text', 'photo', 'document'])
def forward_message(message: Message):
    # forward the message to the channel
    # переслать сообщение на канал
    bot.forward_message(target_chat_id, message.chat.id, message.message_id)

# create a handler function to receive responses from the channel
# создаем функцию-обработчик для получения ответов от канала
##@bot.message_handler(chat_types=["group"], func=lambda message: message.chat.id == target_chat_id)
@bot.message_handler(func=lambda message: message.chat.id == target_chat_id, content_types=['text', 'photo', 'document'])
def forward_response(message: Message):
    # check if the message was a reply to a message forwarded by the bot
    # проверить, было ли сообщение ответом на сообщение, отправленное ботом    
    if message.reply_to_message and message.reply_to_message.forward_from:
        # get the ID of the user who sent the original message
        # получаем ID пользователя, отправившего исходное сообщение
        user_id = message.reply_to_message.forward_from.id
        # send the response back to the user
        # отправить ответ обратно пользователю
        bot.send_message(user_id, message.text)

# start the bot
# запускаем бота
bot.polling()
