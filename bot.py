import time

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import main

TOKEN = '1759264624:AAFnFtTxzDl_-UGrLZcVu3Im2GYKHCcc5jU'
bot = telebot.TeleBot(TOKEN)


class data:
    On_Off = 0
    tage_name = ''


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Да", callback_data="cb_yes"),
               InlineKeyboardButton("Нет", callback_data="cb_no"))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_yes":
        data.On_Off = 1
        check_list = []
        bot.answer_callback_query(call.id, "Мониторинг идет по слову : " + data.tage_name)
        url = 'https://freelancehunt.com/projects?name=' + data.tage_name
        while data.On_Off == 1:
            bs = main.request_site(url)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Бот парсит '
                                                                                                         'информацию об '
                                                                                                         'проектах.\n1 из '
                                                                                                         '3')
            list_name_url = main.get_name_url(bs)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Бот парсит '
                                                                                                         'информацию об '
                                                                                                         'проектах.\n2 из '
                                                                                                         '3')
            list_time = main.get_time(bs)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Бот парсит '
                                                                                                         'информацию об '
                                                                                                         'проектах.\n3 из '
                                                                                                         '3')
            list_worker_type = main.get_cout_type(bs)
            for i in range(len(list_name_url[0])):
                if list_name_url[0][i] not in check_list:
                    kb = InlineKeyboardMarkup()
                    url_button = InlineKeyboardButton(text='Перейти на проект', url=list_name_url[1][i])
                    kb.add(url_button)
                    bot.send_message(call.message.chat.id,
                                     'Названия проекта: ' + list_name_url[0][i] + '\n\nКатегории: ' +
                                     list_worker_type[1][
                                         i] + '\n\nСтавок: ' + list_worker_type[0][i] + '\n\nДата выставленния: ' +
                                     list_time[i], reply_markup=kb)
                    check_list.append(list_name_url[0][i])
                    if i == len(list_name_url[0]) - 1:
                        kb2 = InlineKeyboardMarkup()
                        cancel = InlineKeyboardButton("Отменить мониторинг", callback_data="cancel")
                        pars_page = InlineKeyboardButton("Спарсить страницу", callback_data="pars_page")
                        kb2.add(pars_page, cancel)
                        bot.send_message(call.message.chat.id, 'Вспомогательное меню', reply_markup=kb2)
            time.sleep(10)
    elif call.data == "cb_no":
        bot.answer_callback_query(call.id, "Бот афк.")
    if call.data == 'cancel':
        data.On_Off = 0
        bot.answer_callback_query(call.id, "Мониторинг отключен.")
        kb = InlineKeyboardMarkup()
        start = InlineKeyboardButton("Начать", callback_data="cb_yes")
        kb.add(start)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Начать мониторинг?', reply_markup=kb)


@bot.message_handler(commands=["edit"])
def message_handler(message):
    data.On_Off = 0
    bot.send_message(message.chat.id, 'Введите слово для поиска проекта: ')
    bot.register_next_step_handler(message, start)


@bot.message_handler(commands=["start"])
def message_handler(message):
    if data.tage_name == '':
        bot.send_message(message.chat.id, 'Введите слово для поиска проекта: ')
        bot.register_next_step_handler(message, start)


def start(message):
    data.tage_name = message.text
    bot.send_message(message.chat.id, "Мониторить новые проекты на FREELANCEHUNT?", reply_markup=gen_markup())


bot.polling(none_stop=True)
