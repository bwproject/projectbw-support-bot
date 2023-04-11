import telebot

from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message

from config.settings import TG_TOKEN, TG_CHAT

from message.message import MESSAGE_START


print("Projectbw-bot")

# set the username or ID of the channel you want to get the ID for
target_chat_id = int(TG_CHAT)

# replace the token with your bot's token
bot = telebot.TeleBot(TG_TOKEN)

# define the custom keyboard
keyboard_main = ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
faq_button = KeyboardButton('F.A.Q – «часто задаваемые вопросы»')
support_button = KeyboardButton('Задать вопрос')
keyboard_main.add(faq_button, support_button)

keyboard_faq = ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)
faq1_button = KeyboardButton('Забыли свой Пароль')
faq2_button = KeyboardButton('Вопрос 2?')
faq3_button = KeyboardButton('Вопрос 3?')
main_menu_button = KeyboardButton('Главное меню')
keyboard_faq.add(faq1_button, faq2_button, faq3_button, main_menu_button)

keyboard_back = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
back_button = KeyboardButton('Назад')
keyboard_back.add(back_button, main_menu_button)

# define a handler for the /start command
@bot.message_handler(commands=['start'])
def start_message(message):
    # set the welcome message adn the main menu keyboard
    bot.send_message(chat_id=message.chat.id, text=MESSAGE_START,reply_markup=keyboard_main)

# define the message handler for the restart command
@bot.message_handler(commands=['restart'])
def handle_restart(message):    
    # set the welcome message adn the main menu keyboard
    bot.send_message(chat_id=message.chat.id, text=MESSAGE_START,reply_markup=keyboard_main)

# define the message handler for the "FAQ" message
@bot.message_handler(func=lambda message: message.text == 'F.A.Q – «часто задаваемые вопросы»')
def handle_faq_option(message):
    bot.send_message(chat_id=message.chat.id, text="Выберите один из часто задаваемых вопросов ниже, чтобы узнать больше.", reply_markup=keyboard_faq)

# define the message handler for the "FAQ#1" command
@bot.message_handler(func=lambda message: message.text == 'Забыли свой Пароль')
def faq_message(message):
    bot.reply_to(message, """\
Если вы забыли свой пароль используйте Раздел Забыли свой пароль
на wiki.projectbw.ru 
https://wiki.projectbw.ru/faq/#%D0%B7%D0%B0%D0%B1%D1%8B%D0%BB%D0%B8-%D0%BF%D0%B0%D1%80%D0%BE%D0%BB%D1%8C\
""", reply_markup=keyboard_back)

# define the message handler for the "FAQ#2" command
@bot.message_handler(func=lambda message: message.text == 'How to create a new strategy?')
def faq_message(message):
    bot.reply_to(message, "Answer 2.", reply_markup=keyboard_back)    

# define the message handler for the "FAQ#3" command
@bot.message_handler(func=lambda message: message.text == 'How to create a new order?')
def faq_message(message):
    bot.reply_to(message, "Answer 3.", reply_markup=keyboard_back)

@bot.message_handler(func=lambda message: message.text == 'Назад')
def handle_back_option(message):
    bot.send_message(chat_id=message.chat.id, text="Выберите один из часто задаваемых вопросов ниже, чтобы узнать больше.", reply_markup=keyboard_faq)

@bot.message_handler(func=lambda message: message.text == 'Главное меню')
def handle_main_menu_option(message):
    bot.send_message(chat_id=message.chat.id, text="""\
Здравствуйте, добро пожаловать в чат-бот службы поддержки ProjectBW! 
Пожалуйста, выберите один из вариантов ниже.\
""", reply_markup=keyboard_main)

# define the message handler for the "Support" message
@bot.message_handler(func=lambda message: message.text == 'Задать вопрос')
def handle_support_option(message):
    bot.send_message(chat_id=message.chat.id, text='Напишите свое сообщение прямо в чате.', reply_markup=keyboard_back)

@bot.message_handler(chat_types=["private"])
def forward_message(message: Message):
    # forward the message to the channel
    bot.forward_message(target_chat_id, message.chat.id, message.message_id)

# create a handler function to receive responses from the channel
@bot.message_handler(chat_types=["group"], func=lambda message: message.chat.id == target_chat_id)
def forward_response(message: Message):
    # check if the message was a reply to a message forwarded by the bot
    if message.reply_to_message and message.reply_to_message.forward_from:
        # get the ID of the user who sent the original message
        user_id = message.reply_to_message.forward_from.id
        # send the response back to the user
        bot.send_message(user_id, message.text)

# start the bot
bot.polling()
