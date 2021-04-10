import telebot
import schedule
import time
from telebot import types


#uid = os.environ["TELEGRAM_USER_ID"]
bot = telebot.TeleBot('1762482874:AAFRV7pKVcG6wq8WI4PKrKysVGJZ2K4EcO4')
bot.remove_webhook()

@bot.message_handler(commands=['timer'])
def timer(message):
    print('e')
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    bt3 = types.KeyboardButton('Отмена')
    markup.add(bt3)
    msg = bot.reply_to(message, f'Какое напоминание хотите сделать, {message.from_user.first_name} ?(укажите текст)',reply_markup=markup)
    bot.register_next_step_handler(msg,send_text)

# def textrem(message):#задаём что хотим напоминть
#     txt =

def send_text(message): #отправляем напомнинаие (тут сделать проверку текста, если отмена, то не ждать и сразу отменять.)
    if message.text.lower() == 'отмена':
        loh = types.ReplyKeyboardRemove(selective=False)
        bot.reply_to(message, 'ГАЛЯ, отмена!', reply_markup=loh)
    else:
        loh = types.ReplyKeyboardRemove(selective=False)
        bot.reply_to(message,f'ок, жди, {message.from_user.first_name}',reply_markup=loh)
        time.sleep(3)
        bot.reply_to(message, f'Напоминаю, {message.text}')

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling(none_stop=True)


# подставлять время которое введёт пользователь.