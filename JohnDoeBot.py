import telebot
import time
from pytils import numeral
from telebot import types
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# uid = os.environ["TELEGRAM_USER_ID"]
bot = telebot.TeleBot("1762482874:AAFfImdG6drqsIvTk9yjxkqU4DQAaxsDOj8")
bot.remove_webhook()
def isint(value): #проверка на целое число
    if type(value) != str:
        return False
    try:
        int(value)
        return True
    except ValueError:
        return False

@bot.message_handler(commands=['timer'])
def timer(message):
    print('e')
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    bt3 = types.KeyboardButton('Отмена')
    markup.add(bt3)
    msg = bot.reply_to(message, f'Какое напоминание хотите сделать, {message.from_user.first_name} ?(укажите текст)',
                       reply_markup=markup)
    bot.register_next_step_handler(msg, second_step)


def second_step(message):  # будем спрашивать через скок напоминание
    # здесь в message.text хранится то что он хочет напомнить
    if message.text == 'Отмена':
        kb1 = types.ReplyKeyboardRemove(selective=False)
        bot.reply_to(message, 'ГАЛЯ, Отмена!', reply_markup=kb1)
    else:  # тут нам нужно задать второй вопрос про время.
        msg = bot.reply_to(message, f'Через какое время произвести напоминание, укажите'
                                    f'в минутах?')
        bot.register_next_step_handler(msg, third_step, message.text)

def third_step(message, txt):  # будем спрашивать через скок напоминание
    # здесь в message.text хранятся часы
    if message.text == 'Отмена': #это тестовый вариант, ниже корректный
     kb1 = types.ReplyKeyboardRemove(selective=False)
     bot.reply_to(message, 'ГАЛЯ, Отмена!', reply_markup=kb1)
    elif isint(message.text): # тут нам нужно задать второй вопрос про время.
        # txt = txt
        msg = bot.reply_to(message, f'Через какое время произвести напоминание, укажите'
                                    f'в часах?')
        bot.register_next_step_handler(msg, fourth_step, message.text, txt)  # тут передаём минуты
    else: # так как не верно указал время то переспрашиваем
        msg = bot.reply_to(message, f'поц, введи нормально целое число через сколько минут напомнить: ')
        bot.register_next_step_handler(msg, third_step, txt)

    # if message.text == 'Отмена':
    #     kb1 = types.ReplyKeyboardRemove(selective=False)
    #     bot.reply_to(message, 'ГАЛЯ, Отмена!', reply_markup=kb1)
    # else:  # тут нам нужно задать второй вопрос про время.
    #     msg = bot.reply_to(message, f'Через какое время произвести напоминание, укажите'
    #                                 f'в часах?')
    #     bot.register_next_step_handler(msg, fourth_step, message.text, txt)  # тут переджаём минуты


def fourth_step(message, minutes, txt):  # будем спрашивать через скок напоминание
    # здесь в message.text хранятся минуты
    # txt = txt
    # minutes = minutes
    if message.text == 'Отмена':
        kb1 = types.ReplyKeyboardRemove(selective=False)
        bot.reply_to(message, 'ГАЛЯ, Отмена!', reply_markup=kb1)
    elif isint(message.text):  # тут нам нужно задать второй вопрос про время.
        msg = bot.reply_to(message, f'Через какое время произвести напоминание, укажите'
                                    f'в днях?')
        bot.register_next_step_handler(msg, email_step, minutes, message.text, txt)  # тут переджаём часы
    else:# так как не верно указал время то переспрашиваем
        msg = bot.reply_to(message, f'поц, введи нормально целое число через сколько часов напомнить: ')
        bot.register_next_step_handler(msg, fourth_step, minutes, txt)

def email_step(message, minutes, hour, txt):  # будем спрашивать через скок напоминание
    # здесь в message.text хранятся дни
    # txt = txt
    # minutes = minutes
    # hour = hour
    if message.text == 'Отмена':
        kb1 = types.ReplyKeyboardRemove(selective=False)
        bot.reply_to(message, 'ГАЛЯ, Отмена!', reply_markup=kb1)
    elif isint(message.text):  # тут нам нужно задать второй вопрос про время.
        msg = bot.reply_to(message, f'Куда отправить?')
        bot.register_next_step_handler(msg, send_message, hour, message.text, minutes, txt)  # тут переджаём дни
    else:# так как не верно указал время то переспрашиваем
        msg = bot.reply_to(message, f'поц, введи нормально целое число через сколько дней напомнить: ')
        bot.register_next_step_handler(msg, email_step, minutes, hour, txt)



# По команде выдавать сколько осталось времени до напоминания
# def test(message):
#     print(message.text) 86400


def send_message(message, hour, days, minutes, txt):
    # здесь в message.text хранится почта
    minutes = int(minutes)
    hour = int(hour)
    days = int(days)
    email = message.text
    t = abs(minutes) * 3 + abs(hour) * 3600 + abs(days) * 86400
    kb1 = types.ReplyKeyboardRemove(selective=False)
    rem = ("%s %s %s" % (
        numeral.get_plural(days, "день, дня, дней"),
        numeral.get_plural(hour, "час, часа, часов"),
        numeral.get_plural(minutes, "минута, минуты, минут"))
        )
    bot.reply_to(message, f'Хорошо, {message.from_user.first_name}, до напоминания: {rem}',
                 reply_markup=kb1)
    # bot.reply_to(message, f'ок, жди, {message.from_user.first_name}, напомню через {minutes} минут,'
    #                       f' {hour} часов, {days} дней.', reply_markup=kb1)
    if t >= 9223372036854775807:
        t = 3
    time.sleep(t)  # ждем заданное время
    if txt != str:
        txt = 'sosi'
    bot.reply_to(message, f'Напоминаю, {txt}')

    # create message object instance
    msg = MIMEMultipart()

    message = txt

    # setup the parameters of the message
    password = "guzyoqyhdhytfccq"
    msg['From'] = "johndaebot@yandex.ru"
    #msg['To'] = email
    msg['Subject'] = "Напоминание"

    # # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # create server
    server = smtplib.SMTP_SSL('smtp.yandex.ru:465')

    #server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)

    # send the message via the server.
    #server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()

    print("successfully sent email to %s:" % (msg['To']))


bot.enable_save_next_step_handlers(delay=100)
bot.load_next_step_handlers()
bot.polling(none_stop=True)