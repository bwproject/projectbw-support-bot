import telebot

from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message

from config.settings import TG_TOKEN, TG_CHAT

from message.message import MESSAGE_START, MESSAGE_FAQ, MESSAGE_SUPPORT, MESSAGE_BOT

from message.button import BUT_FAQ, BUT_SUPPORT, BUT_BACK, BUT_MENU, BUT_BOT

from message.faq import FAQ_1, FAQ_1_1, FAQ_2, FAQ_2_1, FAQ_3, FAQ_3_1, FAQ_ALL, FAQ_ALL_1

print("Projectbw-bot")
print("https://github.com/bwproject/projectbw-support-bot")

# set the username or ID of the channel you want to get the ID for
target_chat_id = int(TG_CHAT)

# replace the token with your bot's token
bot = telebot.TeleBot(TG_TOKEN)

# define the custom keyboard
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
@bot.message_handler(commands=['start'])
def start_message(message):
    # set the welcome message adn the main menu keyboard
    bot.send_message(chat_id=message.chat.id, text=MESSAGE_START, reply_markup=keyboard_main, parse_mode='Markdown')

# define the message handler for the restart command
@bot.message_handler(commands=['restart'])
def handle_restart(message):    
    # set the welcome message adn the main menu keyboard
    bot.send_message(chat_id=message.chat.id, text=MESSAGE_START, reply_markup=keyboard_main, parse_mode='Markdown')

# define the message handler for the "FAQ" message
@bot.message_handler(func=lambda message: message.text == BUT_FAQ)
def handle_faq_option(message):
    bot.send_message(chat_id=message.chat.id, text=MESSAGE_FAQ, reply_markup=keyboard_faq, parse_mode='Markdown')

# define the message handler for the "FAQ#1" command
@bot.message_handler(func=lambda message: message.text == FAQ_1)
def faq_message(message):
    bot.reply_to(message,FAQ_1_1, reply_markup=keyboard_back, parse_mode='Markdown')

# define the message handler for the "FAQ#2" command
@bot.message_handler(func=lambda message: message.text == FAQ_2)
def faq_message(message):
    bot.reply_to(message, FAQ_2_1, reply_markup=keyboard_back, parse_mode='Markdown')    

# define the message handler for the "FAQ#3" command
@bot.message_handler(func=lambda message: message.text == FAQ_3)
def faq_message(message):
    bot.reply_to(message, FAQ_3_1, reply_markup=keyboard_back, parse_mode='Markdown')
    
# define the message handler for the "FAQ_ALL" command
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
    bot.send_message(chat_id=message.chat.id, text=MESSAGE_BOT, reply_markup=keyboard_main, parse_mode='Markdown')

# define the message handler for the "Support" message
@bot.message_handler(func=lambda message: message.text == BUT_SUPPORT)
def handle_support_option(message):
    bot.send_message(chat_id=message.chat.id, text=MESSAGE_SUPPORT, reply_markup=keyboard_back, parse_mode='Markdown')

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
