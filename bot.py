#! /usr/bin/env python
# -*- coding: utf-8 -*-


import telebot
from telebot import types
import json
from datetime import datetime
from datetime import timedelta
from datetime import date
import time
import pytz


def to_log(text, message):
    ct = datetime.now().time()
    cd = date.today()
    today = "{}-{}-{} {}:{}:{}".format(cd.year, cd.month, cd.day, ct.hour, ct.minute, ct.second)
    text = today + ' : ' + str(message.from_user.username) + ' - ' + str(
        message.from_user.id) + ' : ' + message.text + ' - ' + text + '\n'
    with open('log.txt', 'a') as log:
        log.write(text)


def good_date(date):  # DD.MM.YYYY
    try:
        datetime.strptime(date, '%d.%m.%Y').date()
    except:
        return False
    return True


def time_7_days(date):  # DD.MM.YYYY
    try:
        print(datetime.now(pytz.timezone( 'Europe/Moscow' )).date(), datetime.now(pytz.timezone( 'Europe/Moscow' )).date() + timedelta(days=7), datetime.strptime(date,
                                                                                '%Y.%m.%d').date())
        return datetime.now(pytz.timezone( 'Europe/Moscow' )).date() + timedelta(days=7) >= datetime.strptime(date,
                                                                                '%Y.%m.%d').date() >= datetime.now(pytz.timezone( 'Europe/Moscow' )).date()
    except:
        return False


file = open("api_key", 'r')
token = file.read()
file.close()
bot = telebot.TeleBot(token=token)

vk = types.KeyboardButton('Мы в ВКонтакте')
insta = types.KeyboardButton('Мы в Instagram')
register = types.KeyboardButton('Регистрация на Гонку Героев')
training_register = types.KeyboardButton('Регистрация на подготовку')
about = types.KeyboardButton('О Гонке Героев')
admin = types.KeyboardButton('Панель админа')
main_markup = types.ReplyKeyboardMarkup(True)
main_markup.row(register, training_register)
main_markup.row(about)
main_markup.row(vk, insta)
main_markup.row(admin)
hide = types.ReplyKeyboardRemove()
back = types.KeyboardButton('Назад')
back_markup = types.ReplyKeyboardMarkup(True)
back_markup.row(back)


@bot.message_handler(commands=['start'])
def main_start(message):
    to_log("main_start", message)
    bot.send_message(message.chat.id,
                     'Привет! Это бот Гонки Героев Казань! \nЕсли я долго не отвечаю - попробуй нажать /start',
                     reply_markup=main_markup)
    bot.register_next_step_handler(message, main_choose)
    return


@bot.message_handler(content_types=['text'])
def start(message):
    to_log("start", message)
    bot.send_message(message.chat.id, 'Если вдруг я не отвечаю, нажми /start!', reply_markup=main_markup)


def main(message):
    to_log("main", message)
    bot.send_message(message.chat.id, 'Что ты хочешь сделать?', reply_markup=main_markup)
    bot.register_next_step_handler(message, main_choose)


def main_choose(message):
    to_log("main_choose", message)
    if message.text == 'Мы в ВКонтакте':
        bot.send_message(message.chat.id, 'Мы в Вконтакте: \nhttps://vk.com/gonkageroevkazan')
        main(message)
    elif message.text == 'Регистрация на Гонку Героев':
        bot.send_message(message.chat.id, 'Лови ссылку для регистрации!\nhttps://heroleague.ru/race/')
        main(message)
    elif message.text == 'Регистрация на подготовку':
        training_show(message)
    elif message.text == 'О Гонке Героев':
        bot.send_message(message.chat.id,
                         '"Гонка Героев” - это серия драйвовых забегов с препятствиями.\nУчастники мероприятия преодолевают полосу препятствий, разработанную профессиональными инженерами и опытными инструкторами. \nРукоходы и переправы, рвы и поля с колючей проволокой, достойная награда и чувство гордости на финише - и это только часть твоего незабываемого приключения.\nПодробнее можешь почитать на https://heroleague.ru/race/')
        main(message)
    elif message.text == 'Панель админа':
        admin(message)
    elif message.text == 'Мы в Instagram':
        bot.send_message(message.chat.id, 'Мы в Instagram: \nhttps://www.instagram.com/heroleaguetraining_kzn/')
        main(message)
    else:
        bot.send_message(message.chat.id,
                         'Я не понимаю твой запрос( Если ты уверен, что все правильно, напиши сюда @Ninevskiy')
        main(message)


def training_show(message):
    to_log("training_show", message)
    training_markup = types.ReplyKeyboardMarkup(True)
    Finded = False
    with open("trainings.json") as json_training:
        data = json.loads(json_training.read())
        for tr in data:
            if time_7_days(tr["date"]["year"] + '.' + tr["date"]["month"] + '.' + tr["date"]["day"]):
                now = types.KeyboardButton(
                    tr["date"]["year"] + '.' + tr["date"]["month"] + '.' + tr["date"]["day"] + ' : ' + tr["place"])
                training_markup.row(now)
                Finded = True
    training_markup.row(back)
    if Finded:
        bot.send_message(message.chat.id, 'На ближайшую неделю я нашел такие тренировки. Выбери одну из них',
                         reply_markup=training_markup)
    else:
        bot.send_message(message.chat.id,
                         'Я не нашел ни одну тренировку на ближайшую неделю. Может, их еще не добавили?',
                         reply_markup=main_markup)
        main(message)
        return
    bot.register_next_step_handler(message, register_training)


registration_date = {}


def register_training(message):
    to_log("register_training", message)
    global registration_date
    if message.text == 'Назад':
        main(message)
        return
    if not time_7_days(message.text[:10] or len(message.text) < 10):
        bot.send_message(message.chat.id, 'Я не нашел такой тренировки.')
        return
    with open("trainings.json") as json_training:
        data = json.loads(json_training.read())
        for tr in data:
            if tr["date"]["year"] == message.text[0:4] and tr["date"]["month"] == message.text[5:7] and tr["date"][
                "day"] == message.text[8:10]:
                text = make_text(tr["date"]["year"], tr["date"]["month"], tr["date"]["day"], tr["description"],
                                 tr["place"],
                                 tr["date"]["hour"], tr["date"]["minutes"])
                bot.send_message(message.chat.id, text)
                bot.send_message(message.chat.id, 'Напиши свое имя и фамилию, чтобы мы записали тебя на тренировку!',
                                 reply_markup=back_markup)
                registration_date[message.chat.id] = message.text[0:10].split('.')
                bot.register_next_step_handler(message, register_end)
                return
    bot.send_message(message.chat.id, 'Я не нашел такой тренировки.')
    training_show(message)


def register_end(message):
    to_log("register_end", message)
    global registration_date
    reg_date = registration_date[message.chat.id]
    if message.text == 'Назад':
        training_show(message)
        return
    with open("trainings.json") as json_training:
        data = json.loads(json_training.read())
        for tr in data:
            if tr["date"]["year"] == reg_date[0] and tr["date"]["month"] == reg_date[1] and tr["date"]["day"] == \
                    reg_date[2]:
                new = {'name': message.text, 'username': '@' + str(message.from_user.username), 'id': message.chat.id}
                tr["people"].append(new)
                with open("trainings.json", "w") as file1:
                    json.dump(data, file1)
                bot.send_message(message.chat.id, 'Я записал тебя на эту тренировку. Не забудь прийти!')
                main(message)
                return
    bot.send_message(message.chat.id, 'Что то пошло не так( Попробуйте позже или напишите @Ninevskiy')
    main(message)


admin_markup = types.ReplyKeyboardMarkup(True)
new = types.KeyboardButton('Новая тренировка')
edit = types.KeyboardButton('Изменить тренировку')
check = types.KeyboardButton('Посмотреть тренировку')
delete = types.KeyboardButton('Удалить тренировку')
admin_markup.row(new, edit)
admin_markup.row(check, delete)
admin_markup.row(back)

edit_markup = types.ReplyKeyboardMarkup(True)
place = types.KeyboardButton("Место")
tim = types.KeyboardButton("Время")
desc = types.KeyboardButton("Описание")
ret = types.KeyboardButton("Назад")
edit_markup.row(desc, tim)
edit_markup.row(place, ret)
nothing_markup = types.ReplyKeyboardMarkup(True)
nothing_markup.row(ret)
training_date = {}
edit = {}


@bot.message_handler(commands=['admin'])
def admin(message):
    to_log("admin", message)
    bot.send_message(message.chat.id, 'Привет! Это панелька админа. Что ты хочешь сделать?', reply_markup=admin_markup)
    bot.register_next_step_handler(message, admin_choose)


def admin_choose(message):
    to_log("admin_choose", message)
    if message.text == 'Новая тренировка':
        bot.send_message(message.chat.id, 'На какую дату ты хочешь создать тренировку? Напиши в формате DD.MM.YYYY',
                         reply_markup=nothing_markup)
        bot.register_next_step_handler(message, new_training_place)
    elif message.text == 'Изменить тренировку':
        edit_training_choose_tr(message)
    elif message.text == 'Посмотреть тренировку':
        bot.send_message(message.chat.id, 'За какую дату ты хочешь посмотреть тренировку? Напиши в формате DD.MM.YYYY',
                         reply_markup=nothing_markup)
        bot.register_next_step_handler(message, check_training)
    elif message.text == 'Удалить тренировку':
        bot.send_message(message.chat.id, 'За какую дату ты хочешь удалить тренировку? Напиши в формате DD.MM.YYYY',
                         reply_markup=nothing_markup)
        bot.register_next_step_handler(message, delete_training)
    else:
        main(message)


def make_text(year, month, day, desc, place, hour, minutes):
    return "Тренировка {0}.{1}.{2}:\nБудет проходить: {3} в {4} часов {5} минут\n{6}".format(day, month, year, place,
                                                                                             hour, minutes, desc)


def make_lst(lst):
    ls = "Список записавшихся:\n"
    for man in lst:
        ls += man["name"] + ' ' + man['username'] + '\n'
    return ls


def delete_training(message):
    to_log("delete_training", message)
    if message.text == 'Назад':
        admin(message)
        return
    date = message.text.split('.')
    with open("trainings.json") as json_training:
        data = json.loads(json_training.read())
        try:
            for i in range(len(data)):
                if data[i]["date"]["year"] == date[2] and data[i]["date"]["month"] == date[1] and data[i]["date"]["day"] == date[0]:
                    data.pop(i)
                    with open("trainings.json", "w") as file1:
                        json.dump(data, file1)
                    bot.send_message(message.chat.id, 'Я удалил тренировку!')
                    admin(message)
                    return
        except:
            bot.send_message(message.chat.id, 'Ты ввел дату тренировки не в том формате. Попробуй заново')
            admin(message)
            return
    bot.send_message(message.chat.id, 'Такой тренировки нет!', reply_markup=edit_markup)
    admin(message)


def check_training(message):
    to_log("check_training", message)
    if message.text == 'Назад':
        admin(message)
        return
    date = message.text.split('.')
    with open("trainings.json") as json_training:
        data = json.loads(json_training.read())
        for tr in data:
            try:
                if tr["date"]["year"] == date[2] and tr["date"]["month"] == date[1] and tr["date"]["day"] == date[0]:
                    text = make_text(date[2], date[1], date[0], tr["description"], tr["place"], tr["date"]["hour"],
                                     tr["date"]["minutes"])
                    bot.send_message(message.chat.id, text)
                    lst = make_lst(tr["people"])
                    if len(lst) > 0:
                        bot.send_message(message.chat.id, lst)
                    admin(message)
                    return
            except:
                bot.send_message(message.chat.id, 'Ты ввел дату тренировки не в том формате. Попробуй заново')
                admin(message)
                return
    bot.send_message(message.chat.id, 'Такой тренировки нет, но ты можешь создать ее!', reply_markup=edit_markup)
    admin(message)


def edit_training_choose_tr(message):
    to_log("edit_training_choose_tr", message)
    text = 'Введи дату тренировки, которую ты хочешь изменить, в формате DD.MM.YYYY'
    bot.send_message(message.chat.id, text, reply_markup=nothing_markup)
    bot.register_next_step_handler(message, find_training)


def find_training(message):
    to_log("find_training", message)
    if message.text == 'Назад':
        admin(message)
        return
    global training_date
    training_date[message.chat.id] = message.text.split('.')
    edit_training(message)


def edit_training(message):
    to_log("edit_training", message)
    try:
        tr = training_date[message.chat.id]
        text = tr[0] + '.' + tr[1] + '.' + tr[2]
        text = 'Что ты хочешь изменить в тренировке ' + text + '?'
        bot.send_message(message.chat.id, text, reply_markup=edit_markup)
        bot.register_next_step_handler(message, edit_training_choose)
    except:
        bot.send_message(message.chat.id, 'Ты ввел дату тренировки не в том формате. Попробуй заново',
                         reply_markup=edit_markup)
        admin(message)


def edit_training_choose(message):
    to_log("edit_training_choose", message)
    global edit
    if message.text == "Место":
        edit[message.chat.id] = 0
    elif message.text == "Время":
        edit[message.chat.id] = 1
    elif message.text == "Описание":
        edit[message.chat.id] = 2
    elif message.text == "Назад":
        admin(message)
        return
    else:
        bot.send_message(message.chat.id, 'Я не понял, повтори, пожалуйста, что ты хочешь изменить?',
                         reply_markup=edit_markup)
        bot.register_next_step_handler(message, edit_training_choose)
        return
    edit_training_final(message)


def edit_training_final(message):
    to_log("edit_training_final", message)
    global edit, training_date
    tr_date = training_date[message.chat.id]
    with open("trainings.json") as json_training:
        data = json.loads(json_training.read())
        for tr in data:
            try:
                if tr["date"]["year"] == tr_date[2] and tr["date"]["month"] == tr_date[1] and tr["date"]["day"] == \
                        tr_date[0]:
                    if edit[message.chat.id] == 0:
                        text = "На что ты хочешь заменить " + "\'" + tr["place"] + "\'?"
                        bot.send_message(message.chat.id, text, reply_markup=nothing_markup)
                        bot.register_next_step_handler(message, edit_training_end)
                        return
                    elif edit[message.chat.id] == 1:
                        text = "На что ты хочешь заменить " + "\'" + tr["date"]["hour"] + ':' + tr["date"][
                            "minutes"] + "\'?\n Пожалуйста, пиши в формате HH:MM!"
                        bot.send_message(message.chat.id, text, reply_markup=nothing_markup)
                        bot.register_next_step_handler(message, edit_training_end)
                        return
                    elif edit[message.chat.id] == 2:
                        text = "На что ты хочешь заменить " + "\'" + tr["description"] + "\'?"
                        bot.send_message(message.chat.id, text, reply_markup=nothing_markup)
                        bot.register_next_step_handler(message, edit_training_end)
                        return
            except:
                bot.send_message(message.chat.id, 'Ты ввел дату тренировки не в том форматею Попробуй заново')
                admin(message)
                return
        bot.send_message(message.chat.id, 'Такой тренировки нет. Но ты можешь создать ее!')
        admin(message)


def edit_training_end(message):
    to_log("edit_training_end", message)
    global edit, training_date
    tr_date = training_date[message.chat.id]
    if message.text == 'Назад':
        edit_training(message)
        return
    with open("trainings.json") as json_training:
        data = json.loads(json_training.read())
        for tr in data:
            if tr["date"]["year"] == tr_date[2] and tr["date"]["month"] == tr_date[1] and tr["date"]["day"] == tr_date[0]:
                if edit[message.chat.id] == 0:
                    tr["place"] = message.text
                elif edit[message.chat.id] == 1:
                    try:
                        dt = message.text.split(':')
                        tr["date"]["hour"] = dt[0]
                        tr["date"]["minutes"] = dt[1]
                    except:
                        bot.send_message(message.chat.id, "Ты ввел время не в том формате. Попробуй заново")
                        edit_training(message)
                        return
                elif edit[message.chat.id] == 2:
                    tr["description"] = message.text
                else:
                    bot.send_message(message.chat.id, "Что то не так с edit. Напиши @Ninevskiy")
                with open("trainings.json", "w") as file1:
                    json.dump(data, file1)
                break

    bot.send_message(message.chat.id, "Успешно изменено!")
    edit_training(message)


def new_training_place(message):
    to_log("new_training_place", message)
    if message.text == 'Назад':
        admin(message)
        return
    global training_date
    if not good_date(message.text):
        bot.send_message(message.chat.id, 'Такой даты не существует. Попробуй заново')
        admin(message)
        return
    training_date[message.chat.id] = message.text.split('.')
    tr_date = training_date[message.chat.id]
    with open("trainings.json") as json_training:
        data = json.loads(json_training.read())
        for tr in data:
            try:
                if tr["date"]["year"] == tr_date[2] and tr["date"]["month"] == tr_date[1] and tr["date"]["day"] == \
                        tr_date[0]:
                    bot.send_message(message.chat.id,
                                     'Эта тренировка уже существует. \nПеревожу тебя на ee редактирование')
                    edit_training(message)
                    return
            except:
                bot.send_message(message.chat.id, 'Ты ввел дату тренировки не в том формате. Попробуй еще раз.')
                admin(message)
                return
        new_train = {"date": {
            "year": 0,
            "month": 0,
            "day": 0,
            "hour": "",
            "minutes": ""
        }, "place": "", "description": "", "people": []}
        new_train["date"]["year"] = tr_date[2]
        new_train["date"]["month"] = tr_date[1]
        new_train["date"]["day"] = tr_date[0]
        data.append(new_train)
        with open("trainings.json", "w") as file1:
            json.dump(data, file1)
    bot.send_message(message.chat.id, 'Отлично, я создал тренировку! \nПеревожу тебя на ее редактирование')
    edit_training(message)


bot.polling(none_stop=True)

