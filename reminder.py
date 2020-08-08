import telebot
from telebot import types
import json
from datetime import datetime
from datetime import timedelta
from datetime import date
import time

file = open("api_key", 'r')
token = file.read()
file.close()
bot = telebot.TeleBot(token=token)

def make_text(year, month, day, desc, place, hour, minutes):
    return "Тренировка {0}.{1}.{2}:\nБудет проходить: {3} в {4} часов {5} минут\n{6}".format(day, month, year, place,
                                                                                             hour, minutes, desc)


mn = 2
def time_1_day(date):  # YYYY.MM.DD.HH.MM
    return abs(datetime.now() + timedelta(days=1) - datetime.strptime(date, '%Y.%m.%d.%H.%M')) <= timedelta(minutes=mn / 2)


def time_2_hours(date): # YYYY.MM.DD
    return abs(datetime.now() + timedelta(hours=2) - datetime.strptime(date, '%Y.%m.%d.%H.%M')) <= timedelta(minutes=mn / 2)


def check_reminder():
    print("Checking...")
    with open("trainings.json") as json_training:
        data = json.loads(json_training.read())
        for tr in data:
            datefun = tr["date"]["year"] + '.' + tr["date"]["month"] + '.' + tr["date"]["day"] + '.' + tr["date"]["hour"] + '.'+ tr["date"]["minutes"]
            print(datefun)
            if time_2_hours(datefun):
                print('2 + ', datefun)
                for man in tr["people"]:
                    text = "Напоминаю про тренировку, которая начинает через ~2 часа! Не забудь прийти\n" + \
                           make_text(tr["date"]["year"], tr["date"]["month"], tr["date"]["day"], tr["description"],
                                     tr["place"], tr["date"]["hour"], tr["date"]["minutes"])
                    bot.send_message(man["id"], text)
            if time_1_day(datefun):
                print('1 + ', datefun)
                for man in tr["people"]:
                    text = "Напоминаю про завтрашнюю тренировку! Не забудь прийти\n" + \
                           make_text(tr["date"]["year"], tr["date"]["month"], tr["date"]["day"], tr["description"],
                                     tr["place"], tr["date"]["hour"], tr["date"]["minutes"])
                    bot.send_message(man["id"], text)





while True:
    time.sleep(mn * 60)
    check_reminder()