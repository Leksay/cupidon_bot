import telebot

import requests

import sqlite3
import os
from telebot import apihelper

token = "999734121:AAHqWcK9132yCBRxBspye4K5V4nNiYEHcSo"
chat_id = "999734121"

bot = telebot.TeleBot(token)

cheked_word = 'chek'

activateModeratorWord = "make some love"

alreadyActiveMSG = "Валентинка уже активирована"
activeNewMSG = "Ваша валентинка зарегистрирована"
loverMSG = "Ваша валентинка доставлена"
moderatorAlreadyCheked = "Купидон, ты уже доставил эту валентинку ! Займись другими !"
clearWord = "/clear"

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    conn = sqlite3.connect('bd/ids.db')
    cursor = conn.cursor()
    isStart = "/start" in message.text
    if(isStart):
        afterStartString = message.text.replace("/start ", "")
        #Activate new user
        if(afterStartString.isdigit()):
            isActivated_Int = cursor.execute(('SELECT Active FROM ids WHERE id={}').format(afterStartString)).fetchone()[0]
            if(isActivated_Int == 1):
                kupidons = cursor.execute('SELECT * FROM kupidons').fetchall()
                for kupidon in kupidons:
                    myChatId = message.chat.id
                    if(str(myChatId) == kupidon[0]):
                        alreadyCheked = cursor.execute(('SELECT Cheked FROM ids WHERE id={}').format(afterStartString)).fetchone()[0]
                        if(alreadyCheked == 1):
                            bot.send_message(message.chat.id, moderatorAlreadyCheked)
                            return
                        cursor.execute('UPDATE ids SET Cheked = 1 WHERE id={}'.format(afterStartString))
                        conn.commit()
                        bot.send_message(message.chat.id, "Молодец купидон, норм так доставил")
                        lover = cursor.execute(('SELECT chat_id FROM ids WHERE id={}').format(afterStartString)).fetchone()[0]
                        bot.send_message(lover, loverMSG)
                        return
                bot.send_message(message.chat.id, alreadyActiveMSG)

            elif(isActivated_Int == 0):
                bot.send_message(message.chat.id, activeNewMSG)
                cursor.execute('UPDATE ids SET Active = 1 WHERE id={}'.format(afterStartString))
                cursor.execute('UPDATE ids SET chat_id={} WHERE id={}'.format(message.chat.id, afterStartString))
                conn.commit()

    elif (message.text == cheked_word):
        print("Cheked")
    elif (message.text == activateModeratorWord):
        cursor.execute(('INSERT INTO kupidons VALUES({})').format(message.chat.id))
        bot.send_message(message.chat.id, "Теперь вы купидон! ! !")
        conn.commit()
    elif(message.text.find(clearWord) != -1):
        clearId = message.text.replace("/clear ", "")
        if (clearId.isdigit()):
            kupidons = cursor.execute('SELECT * FROM kupidons').fetchall()
            for kupidon in kupidons:
                myChatId = message.chat.id
                if (str(myChatId) == kupidon[0]):
                    cursor.execute('UPDATE ids SET Active = 0, Cheked = 0, chat_id = 0 WHERE id={}'.format(clearId))
                    conn.commit()
                    bot.send_message(message.chat.id, "строка удалена")
        else:
            bot.send_message(message.chat.id, "Неправильно введена команда /clear, введите '/clear <id>'")


    bot.send_message(message.chat.id, message.text )



if __name__ == '__main__':
    bot.infinity_polling()




