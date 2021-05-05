import telebot
import json
from datetime import datetime
from datetime import timedelta
import time


file = open("api_key", 'r')
token = file.read()
file.close()
bot = telebot.TeleBot(token=token)

def make_text(year, month, day, desc, place, hour, minutes):
    text = 'Напоминаю, что необходимо подойти за 10-15 мин до начала, чтобы успеть подготовиться и размяться. Начинаем в {}:{}.\nМесто тренировки: {}.\n{}'.format(hour,
                                                                                        minutes, place, desc)
    return text


mn = 20
utc = 3
def time_1_day(fdate):  # YYYY.MM.DD.HH.MM
    try:
        now = datetime.now() + timedelta(hours=utc)
        train = datetime.strptime(fdate, '%Y.%m.%d.%H.%M')
        return (train - timedelta(days=1) - now) >= timedelta(minutes=0) and (train - timedelta(days=1) - now) <= timedelta(minutes=mn)
    except:
        print("Что то не так с датой")
        return False

def time_2_hours(fdate): # YYYY.MM.DD
    try:
        now = datetime.now() + timedelta(hours=utc)
        train = datetime.strptime(fdate, '%Y.%m.%d.%H.%M')
        return (train - timedelta(hours=2) - now) >= timedelta(minutes=0) and (train - timedelta(hours=2) - now) <= timedelta(minutes=mn)
    except:
        print("Что то не так с датой")
        return False


def check_reminder():
    print("Checking...")
    with open("trainings.json") as json_training:
        data = json.loads(json_training.read())
        now = datetime.now() + timedelta(hours=utc)
        for tr in data:
            datefun = tr["date"]["year"] + '.' + tr["date"]["month"] + '.' + tr["date"]["day"] + '.' + tr["date"]["hour"] + '.'+ tr["date"]["minutes"]
            print(datefun)
            if time_2_hours(datefun):
                print(now, '2 + ', datefun)
                for man in tr["people"]:
                    text = "Тренировка уже через ~2 часа!\n" + \
                           make_text(tr["date"]["year"], tr["date"]["month"], tr["date"]["day"], tr["description"],
                                     tr["place"], tr["date"]["hour"], tr["date"]["minutes"])
                    bot.send_message(man["id"], text)
            if time_1_day(datefun):
                print(now, '1 + ', datefun)
                for man in tr["people"]:
                    text = "Не забудь про завтрашнюю тренировку!\n" + \
                           make_text(tr["date"]["year"], tr["date"]["month"], tr["date"]["day"], tr["description"],
                                     tr["place"], tr["date"]["hour"], tr["date"]["minutes"])
                    bot.send_message(man["id"], text)



#time.sleep(2 * 60)
while True:
    check_reminder()
    time.sleep(mn * 60)