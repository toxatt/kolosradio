
from threading import Thread
from tool import getDateTimeNow
import os
from time import sleep
import telepot
import speech_recognition as sr

class Telegram (Thread):
    def __init__(self, params):
        Thread.__init__(self)
        self.tg_bot = params['tg-bot']
        self.tg_chat = params['tg-group']
        self.path = params['path-sound']

    def run(self):
        print("Telegramm start")
        #bot = telebot.TeleBot(self.tg_bot)
        bot = telepot.Bot(self.tg_bot)
        r = sr.Recognizer()
        while True:
            files = os.listdir(self.path)
            files.sort(key=lambda f: os.path.getmtime(os.path.join(self.path, f)))

            for filename in files:
                with open(os.path.join(self.path, filename), "rb") as fl:
                    try:
                        er = bot.sendVoice(self.tg_chat, fl)
                        print(er)
                        try:
                            h = sr.AudioFile(fl.name)
                            with h as source:
                                audio = r.record(source)
                            text = r.recognize_google(audio, language="ru-RU")
                            print(text)
                            er = bot.sendMessage(self.tg_chat, text)
                            print(er)
                        except:
                            print("Can't recognize ")
                        fl.close()
                        os.remove(os.path.join(self.path, filename))
                    except:
                        print("Can't send message")
            sleep(1)

         #   print("ok")

           # for file