import os

from flask import Flask

app = Flask(__name__)

import pymysql
import pymysql.cursors
import telebot

# database connection


bot = telebot.TeleBot("1304603554:AAGpGaPnl-3qOuZiKYDj0etT0SD0YZ0T3EM", parse_mode=None)  # You can set parse_mode by default. HTML or MARKDOWN

# 795460679 user.id Мой
id_tolik: int = 795460679
id_lesya = 481284777


@bot.message_handler(content_types=['text'])
def send_message(message):
    if message.from_user.id == id_tolik or message.from_user.id == id_lesya:
        connection = pymysql.connect(host="35.225.83.251", user="root", passwd="fvsltMJCqtPOntly", database="browbar",
                                     cursorclass=pymysql.cursors.DictCursor)
        bot.send_message(message.chat.id, "Введи номер телефона клиента!")
        # bot.send_message(message.chat.id,message.from_user.id)
        retrive = "Select * from customers WHERE Phone = %s ORDER BY `N` DESC LIMIT 2"
        cursor = connection.cursor()

        cursor.execute(retrive, message.text)
        rows = cursor.fetchall()

        for row in rows:
            answer = (str(row["FIO"]) + " \n " + str(row["Phone"]) + " \n " + str(row["Phone2"]) + " \n " + str(
                row["Date"]) + " \n " + str(row["Krasitel"]) + " \n " + str(row["Color"]) + " \n " + str(
                row["Color2"]) + " \n " + str(row["Oxid"]) + " \n " + str(row["Propor"]) + " \n " + str(
                row["Time"]) + " \n " + str(row["Note"]))
            bot.send_message(message.chat.id, answer)

        connection.commit()
        connection.close()


bot.polling(none_stop=True)

if __name__ == "__FindCustomers__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))