# 1304603554:AAGpGaPnl-3qOuZiKYDj0etT0SD0YZ0T3EM - DTestAGBot
#1390835335:AAHbD5CDwwIWs_OZDhiH4W131W0in3nticM - BrowBar

# -*- coding: utf-8 -*-
"""
This Example will show you how to use register_next_step handler.
"""

import telebot
from telebot import types
import pymysql
import pymysql.cursors
from pymysql import Error
from telebot.types import KeyboardButton

API_TOKEN = '1390835335:AAHbD5CDwwIWs_OZDhiH4W131W0in3nticM'

bot = telebot.TeleBot(API_TOKEN)
id_tolik: int = 795460679
id_lesya = 481284777
user_dict = {}


class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.sex = None


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Поиск', 'Добавление')  # Имена кнопок
    msg = bot.reply_to(message, 'Выбирите нужное действие', reply_markup=markup)
    bot.register_next_step_handler(msg, process_step)


# кнопки с выбором что делать
def process_step(message):
    chat_id = message.chat.id

    if message.text == 'Поиск':
        #bot.send_message(message.chat.id, "Поиск клиента")
        msg = bot.reply_to(message, 'Введите номер телефона?')
        bot.register_next_step_handler(msg, process_search_step)
    else:
        #bot.send_message(message.chat.id, "Добавление клиента")
        msg = bot.reply_to(message, 'Введите имя?')
        bot.register_next_step_handler(msg, process_name_step)


# Обработка если выбран поиск по базе клинета
def process_search_step(message):
    try:
        if message.from_user.id == id_tolik or message.from_user.id == id_lesya:
            connection_search = pymysql.connect(host="localhost", user="root", passwd="", database="goray",
                                                cursorclass=pymysql.cursors.DictCursor)
            bot.send_message(message.chat.id, "Введи номер телефона клиента!")
            # bot.send_message(message.chat.id,message.from_user.id)
            retrive = "Select * from customers WHERE Phone = %s ORDER BY `N` DESC LIMIT 2"
            cursor = connection_search.cursor()

            cursor.execute(retrive, message.text)
            rows = cursor.fetchall()

        for row in rows:
            answer = (str(row["FIO"]) + " \n " + str(row["Phone"]) + " \n " + str(row["Phone2"]) + " \n " + str(
                row["Date"]) + " \n " + str(row["Krasitel"]) + " \n " + str(row["Color"]) + " \n " + str(
                row["Color2"]) + " \n " + str(row["Oxid"]) + " \n " + str(row["Propor"]) + " \n " + str(
                row["Time"]) + " \n " + str(row["Note"]))
            bot.send_message(message.chat.id, answer)

        connection_search.commit()
        cursor.close()
        connection_search.close()
    except pymysql.Error as error:
        bot.reply_to(message, "Failed to insert into MySQL table {}".format(error))


# Обработка добавление клиента при выборе кнопки добавить
def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'Введите номер телефона?')
        bot.register_next_step_handler(msg, process_numberphone_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_numberphone_step(message):
    try:
        chat_id = message.chat.id
        nPhone = message.text
        if not nPhone.isdigit():
            msg = bot.reply_to(message, 'Это должен быть цифры. Введите номер телефона')
            bot.register_next_step_handler(msg, process_numberphone_step)
            return
        user = user_dict[chat_id]
        user.nPhone = nPhone
        msg = bot.reply_to(message, 'Введите второй номер телефона?')
        bot.register_next_step_handler(msg, process_numberphone2_step)
    except Exception as e:
        bot.reply_to(message, 'oooops -process_numberphone_step')

def process_numberphone2_step(message):
    try:
        chat_id = message.chat.id
        nPhone2 = message.text
        if not nPhone2.isdigit():
            msg = bot.reply_to(message, 'Это должен быть цифры. Введите номер телефона')
            bot.register_next_step_handler(msg, process_numberphone2_step)
            return
        user = user_dict[chat_id]
        user.nPhone2 = nPhone2
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Igora', 'BINACIL', 'Elan', 'Elan Smart', 'Thuya', 'Hair', 'Well', 'Refectocil', 'Bronsun', 'Brow', 'Henna', 'Хна')
        msg = bot.reply_to(message, 'Выбирите краситель', reply_markup=markup)
        bot.register_next_step_handler(msg, process_krasitel_step)
    except Exception as e:
        bot.reply_to(message, 'oooops -process_numberphone_step2')


def process_krasitel_step(message):
    try:
        chat_id = message.chat.id
        krasitel = message.text
        user = user_dict[chat_id]
        if (krasitel == u'Igora') or (krasitel == u'BINACIL') or (krasitel == u'Elan') or (krasitel == u'Elan Smart') or (krasitel == u'Thuya') or (krasitel == u'Hair') or (krasitel == u'Well') or (krasitel == u'Refectocil') or (krasitel == u'Bronsun') or (krasitel == u'Brow') or (krasitel == u'Henna') or (krasitel == u'Хна'):
            user.krasitel = krasitel
        else:
            raise Exception()
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('Black', 'Blue Black', 'Brown', 'Light Brown', 'Medium Brown', 'Dark Brown', 'Graphite')
        msg = bot.reply_to(message, 'Выбирите цвет', reply_markup=markup)
        bot.register_next_step_handler(msg, process_color_step)
    except Exception as e:
        bot.reply_to(message, 'oooops -process_krasitel_step')


def process_color_step(message):
    try:
        chat_id = message.chat.id
        color = message.text
        user = user_dict[chat_id]
        if (color == u'Black') or (color == u'Blue Black') or (color == u'Brown') or (color == u'Light Brown') or (color == u'Medium Brown') or (
                color == u'Dark Brown') or (
                color == u'Graphite'):
            user.color = color
        else:
            raise Exception()
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('Нет', 'Black', 'Blue Black', 'Brown', 'Light Brown', 'Medium Brown', 'Dark Brown', 'Graphite')
        msg = bot.reply_to(message, 'Выбирите второй цвет', reply_markup=markup)
        bot.register_next_step_handler(msg, process_color2_step)
    except Exception as e:
        bot.reply_to(message, 'oooops -process_color_step')

def process_color2_step(message):
    try:
        chat_id = message.chat.id
        color2 = message.text
        user = user_dict[chat_id]
        if (color2 == u'Нет')  or (color2 == u'Black') or (color2 == u'Blue Black') or (color2 == u'Brown') or (color2 == u'Light Brown') or (
                color2 == u'Medium Brown') or (
                color2 == u'Dark Brown') or (
                color2 == u'Graphite'):
            user.color2 = color2
        else:
            raise Exception()
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('Igora 6%', 'BINACIL 3%', 'Elan 3%', 'Elan Smart 3%', 'Thuya 3%', 'Hair Well 3%', 'Refectocil 3%', 'Bronsun 3%')
        msg = bot.reply_to(message, 'Выбирите окислитель', reply_markup=markup)
        bot.register_next_step_handler(msg, process_oxid_step)
    except Exception as e:
        bot.reply_to(message, 'oooops -process_color2_step')


def process_oxid_step(message):
    try:
        chat_id = message.chat.id
        oxid = message.text
        user = user_dict[chat_id]
        if (oxid == u'Igora 6%') or (oxid == u'BINACIL 3%') or (oxid == u'Elan 3%') or (oxid == u'Elan Smart 3%') or (oxid == u'Thuya 3%') or (oxid == u'Hair Well 3%') or (oxid == u'Refectocil 3%') or (oxid == u'Bronsun 3%'):
            user.oxid = oxid
        else:
            raise Exception()
        msg = bot.reply_to(message, 'Выбирите пропорцию')
        bot.register_next_step_handler(msg, process_propor_step)
    except Exception as e:
        bot.reply_to(message, 'oooops -process_oxid_step')


def process_propor_step(message):
    try:
        chat_id = message.chat.id
        propor = message.text
        user = user_dict[chat_id]
        user.propor = propor
        msg = bot.reply_to(message, 'Запишите Время')
        bot.register_next_step_handler(msg, process_time_step)
    except Exception as e:
        bot.reply_to(message, 'oooops -process_propor_step')

def process_time_step(message):
    try:
        chat_id = message.chat.id
        time = message.text
        user = user_dict[chat_id]
        user.time = time
        msg = bot.reply_to(message, 'Запишите Коментарии')
        bot.register_next_step_handler(msg, process_note_step)
    except Exception as e:
        bot.reply_to(message, 'oooops -process_time_step')

def process_note_step(message):
    try:
        chat_id = message.chat.id
        note = message.text
        user = user_dict[chat_id]
        user.note = note
        #msg = bot.reply_to(message, 'Выбирите Время')
        #bot.register_next_step_handler(msg, process_note_step)
    except Exception as e:
        bot.reply_to(message, 'oooops -process_note_step')

    #Вывод меседжа с введенными данными и коннект к базе для инсерта nPhone2
    bot.send_message(chat_id, 'Имя ' + user.name + '\n Телефон: ' + str(user.nPhone) + '\n Телефон2: ' + str(user.nPhone2) + '\n Краситель:' + user.krasitel + '\n Цвет :' + user.color + '\n Цвет2 :' + user.color2 + '\n Окислитель :' + user.oxid + '\n Пропорция :' + user.propor + '\n Время :' + user.time + '\n Коментарии :' + user.note)


    connection = pymysql.connect(host="localhost", user="root", passwd="", database="test_bot", cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    mySql_insert_query = "INSERT INTO customers_test (FIO, Phone, Phone2 , Krasitel, Date, Color, Color2, Oxid, Propor, Time, Note) VALUES (%s, %s, %s, %s, CURRENT_DATE(), %s, %s, %s, %s, %s, %s) "


    cursor.execute(mySql_insert_query, (user.name, int(user.nPhone), int(user.nPhone2), user.krasitel, user.color, user.color2, user.oxid, user.propor, user.time, user.note ))
    connection.commit()
    cursor.close()
    connection.close()
    bot.send_message(message.chat.id, "Запись успешно добавлена в базу")
# except Exception as e:
# bot.reply_to(message, 'oooops')
# читаем с базы записи
    #connection = pymysql.connect(host="localhost", user="root", passwd="", database="test_bot", cursorclass=pymysql.cursors.DictCursor)
    #cursor = connection.cursor()
    #mySql_insert_query = "SELECT * From customers_test"

# recordTuple = (user.name, user.nPhone, user.sex)

    #cursor.execute(mySql_insert_query)
    #records = cursor.fetchall()
    #for row in records:
    #   answer = (str(row["FIO"]) + " \n " + str(row["Phone"]) + " \n " + str(row["Phone2"]) + " \n " + str(
    #            row["Date"]) + " \n " + str(row["Krasitel"]) + " \n " + str(row["Color"]) + " \n " + str(
    #            row["Color2"]) + " \n " + str(row["Oxid"]) + " \n " + str(row["Propor"]) + " \n " + str(
    #            row["Time"]) + " \n " + str(row["Note"]))
    #   bot.send_message(message.chat.id, answer)
    #connection.commit()
    #cursor.close()
    #connection.close()

# читаем с базы записи
    #raise Exception()
    #except pymysql.Error as error:
    #bot.reply_to(message, "Failed to insert into MySQL table {}".format(error))


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.polling(none_stop=True)
