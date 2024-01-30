# -*- coding: utf-8 -*-
import json

import telebot
from telebot import types
import requests


TOKEN = '6739362788:AAHCJnzZtexqEBxX9iLI7HU9OZy0PP2w-j4'
bot = telebot.TeleBot(TOKEN)

translations = {
    'english': {
        'welcome': "Welcome to Bot! 🙌\nLet's find the perfect home for you!",
        'choose_language': "Choose Language:",
        'find_apartments': "Find Apartments",
        'show_favorites': "Show Favorites",
        'change_language': "Change Language",
        'select_currency': "Select currency",
        'select_budget': "Choose your budget: (You can choose several answers)",
        'select_neighborhood': "Choose accommodation location: (You can choose several answer)",
        'select_type': "Choose accommodation type: (You can choose several answer)",
        'select_requests': "Choose additional requests: (You can choose several answer)",
        'leave_review': "Leave a Review",
        'cancel': "Cancel",
        'next': "Next",
        'cancel_text': "Action cancelled! To start over, send the message - /start",
        'rental_period': "Please answer the questions so we can find the best rental options for you "
                         "🏡\n\nRental period:",
        'day': "Daily",
        'search': "Search",
        'month': "Monthly",
        'year': "Yearly",
        'back': "Back",
        'dollars': "USD",
        'rupiahs': "Rupiah"
    },
    'russian': {
        'welcome': "Привет! Добро пожаловать в RenteeBot! 🙌\nДавайте найдем подходящее жилье для вас!",
        'choose_language': "Выбирите Язык:",
        'find_apartments': "Найти апартаменты",
        'show_favorites': "Показать избранное",
        'change_language': "Изменить язык",
        'select_currency': "Выберите валюту",
        'select_budget': "Выберите ваш бюджет: (Вы можете выбрать несколько вариантов)",
        'select_neighborhood': "Выберите подходящий район: (Вы можете выбрать несколько вариантов)",
        'select_type': "Выберите тип недвижимости: (Вы можете выбрать несколько вариантов)",
        'select_requests': "Выберите необходимые удобства: (Вы можете выбрать несколько вариантов)",
        'leave_review': "Оставить отзыв",
        'cancel': "Отмена",
        'search': "Поиск",
        'next': "Дальше",
        'cancel_text': "Действие отменено! Чтобы начать заново, отправьте сообщение - /start",
        'rental_period': "Пожалуйста, ответьте на вопросы, чтобы мы смогли подобрать для вас лучшие "
                         "варианты жилья для аренды ""🏡\n\nПериод аренды:",
        'day': "День",
        'month': "Месяц",
        'year': "Год",
        'back': "Назад",
        'dollars': "Доллары",
        'rupiahs': "Рупии"
    }
}

user_languages = {}
user_currencies = {}
user_rental_periods = {}
user_budgets = {}
user_neighborhood = {}
user_types = {}
user_requests = {}


prices1 = {
    'dollars': {
        'Day': {
            '1': "less than 20$",
            '2': "20 - 50$",
            '3': "50 - 70$",
            '4': "70 - 100$",
            '5': "100 - 140$",
            '6': "more than 140$",
        },
        'Month': {
            '1': "less than 650$",
            '2': "650 - 1300$",
            '3': "1300 - 1950$",
            '4': "1950 - 2600$",
            '5': "2600 - 3250$",
            '6': "more than 3250$",
        },
        'Year': {
            '1': "less than 8000$",
            '2': "8000 - 16000$",
            '3': "16000 - 24000$",
            '4': "24000 - 32000$",
            '5': "32000 - 40000$",
            '6': "more than 40000$",
        }
    },
    'rupiahs': {
        'Day': {
            '1': "less than 300k",
            '2': "300k - 700k",
            '3': "700k - 1mln",
            '4': "1mln - 1.5mln",
            '5': "1.5mln - 2mln",
            '6': "more than 2mln",
        },
        'Month': {
            '1': "less than 10 mln",
            '2': "10 mln - 20 mln",
            '3': "20 mln - 30 mln",
            '4': "30 mln - 40 mln",
            '5': "40 mln - 50 mln",
            '6': "more than 50 mln",
        },
        'Year': {
            '1': "less than 120 mln",
            '2': "120 mln - 240 mln",
            '3': "240 mln - 360 mln",
            '4': "360 mln - 480 mln",
            '5': "480 mln - 600 mln",
            '6': "more than 600 mln"
        }
    }
}
selected_prices = {}

locations = ['Canggu', 'Ubud', 'Kerobokan', 'Umalas', 'Seminyak', 'Pererenan', 'Jimbaran', 'Nusa Dua', 'Sanur',
             'Denpasar', 'Ungasan', 'Bukit', 'Sukawati', 'Kuta', 'Silakarang', 'Lovina', 'Uluwatu', 'Tanah Lot']
selected_locations = {}

typesh = ['Villa Entirely', 'Room in a shared villa', 'Apartments', 'Guesthouse']
selected_types = {}

requestions = ['Kitchen', 'AC', 'Private pool', 'Shared pool', 'Wi-Fi', 'Shower', 'Bathtub', 'Cleaning service', 'TV',
               'Parking area']
selected_requestions = {}

state_history = {}

currency = 'dollars'
rental_period = 'day'


def generate_keyboard(user_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = []
    for location in locations:
        text = location
        if location in selected_locations.get(user_id, []):
            text += " ✅"
        buttons.append(types.InlineKeyboardButton(text, callback_data=f'find_{location}'))
    keyboard.add(*buttons)
    button7 = types.InlineKeyboardButton(translations[user_languages[user_id]]['back'], callback_data='back')
    button8 = types.InlineKeyboardButton(translations[user_languages[user_id]]['next'], callback_data='next')
    button9 = types.InlineKeyboardButton(translations[user_languages[user_id]]['cancel'], callback_data='cancel')
    keyboard.row(button7, button8)
    keyboard.add(button9)
    return keyboard


def generate_keyboard_prices(user_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = []
    for price in prices1[user_currencies[user_id]][user_rental_periods[user_id]].values():
        text = price
        if price in selected_prices.get(user_id, []):
            text += " ✅"
        buttons.append(types.InlineKeyboardButton(text, callback_data=f'budget_{price}'))
    button7 = types.InlineKeyboardButton(translations[user_languages[user_id]]['back'], callback_data='back')
    button8 = types.InlineKeyboardButton(translations[user_languages[user_id]]['next'], callback_data='next')
    button9 = types.InlineKeyboardButton(translations[user_languages[user_id]]['cancel'], callback_data='cancel')
    keyboard.add(*buttons)
    keyboard.row(button7, button8)
    keyboard.add(button9)
    return keyboard


def generate_keyboard_typesh(user_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = []
    for typeh in typesh:
        text = typeh
        if typeh in selected_types.get(user_id, []):
            text += " ✅"
        buttons.append(types.InlineKeyboardButton(text, callback_data=f'type_{typeh}'))
    button7 = types.InlineKeyboardButton(translations[user_languages[user_id]]['back'], callback_data='back')
    button8 = types.InlineKeyboardButton(translations[user_languages[user_id]]['next'], callback_data='next')
    button9 = types.InlineKeyboardButton(translations[user_languages[user_id]]['cancel'], callback_data='cancel')
    keyboard.add(*buttons)
    keyboard.row(button7, button8)
    keyboard.add(button9)
    return keyboard


def generate_keyboard_requestions(user_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = []
    for requestion in requestions:
        text = requestion
        if requestion in selected_requestions.get(user_id, []):
            text += " ✅"
        buttons.append(types.InlineKeyboardButton(text, callback_data=f'requestion_{requestion}'))
    keyboard.add(*buttons)
    button7 = types.InlineKeyboardButton(translations[user_languages[user_id]]['back'], callback_data='back')
    button8 = types.InlineKeyboardButton(translations[user_languages[user_id]]['next'], callback_data='next')
    button9 = types.InlineKeyboardButton(translations[user_languages[user_id]]['cancel'], callback_data='cancel')
    keyboard.row(button7, button8)
    keyboard.add(button9)
    return keyboard


@bot.message_handler(commands=['start'])
def start(message):
    global user_language
    user_id = message.chat.id
    if user_id not in state_history:
        user_languages[user_id] = 'english'
    user_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(translations[user_languages[user_id]]['find_apartments'],
                                         callback_data='find_apartments')
    button2 = types.InlineKeyboardButton(translations[user_languages[user_id]]['show_favorites'],
                                         callback_data='show_favorites')
    button3 = types.InlineKeyboardButton(translations[user_languages[user_id]]['change_language'],
                                         callback_data='change_language')
    button4 = types.InlineKeyboardButton(translations[user_languages[user_id]]['leave_review'],
                                         callback_data='leave_review')
    keyboard.add(button1)
    keyboard.add(button2)
    keyboard.add(button3)
    keyboard.add(button4)
    bot.send_message(message.chat.id,
                     f"{message.from_user.first_name}, {translations[user_languages[user_id]]['welcome']}",
                     reply_markup=keyboard)





def next_result(call):
    user_id = call.message.chat.id
    state_history[user_id] = 'result'
    if user_languages[user_id] == 'russian':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"Пожалуйста, проверьте ваш запрос:\n\nПериод: {user_rental_periods[user_id]}\nБюджет: {', '.join(selected_prices[user_id])}\nЛокация: {', '.join(selected_locations[user_id])}\nТип недвижимости: {', '.join(selected_types[user_id])}\nУдобства: {', '.join(selected_requestions[user_id])}",
                          disable_web_page_preview=True)
    else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"Please, check your request::\n\nRental period: {user_rental_periods[user_id]}\nBudget: {', '.join(selected_prices[user_id])}\nLocations: {', '.join(selected_locations[user_id])}\nAccommodation types: {', '.join(selected_types[user_id])}\nAmenities: {', '.join(selected_requestions[user_id])}",
                              disable_web_page_preview=True)
    keyboard = types.InlineKeyboardMarkup()
    button3 = types.InlineKeyboardButton(translations[user_languages[user_id]]['search'], callback_data='search')
    button4 = types.InlineKeyboardButton(translations[user_languages[user_id]]['back'], callback_data='back')
    button5 = types.InlineKeyboardButton(translations[user_languages[user_id]]['cancel'], callback_data='cancel')
    keyboard.add(button4)
    keyboard.add(button3)
    keyboard.add(button5)
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=keyboard)


def search(call):
    user_id = call.message.chat.id
    state_history[user_id] = 'search'
    url = 'https://api.arebali.com/catalog/0/10'
    headers = {'Content-type': 'application/json',
               'Accept': 'text/plain',
               'Content-Encoding': 'utf-8'}

    filters = {
        "minPrice": 0,
        "maxPrice": 9999,
        "countRooms": 10,
        "sleepCount": 15
    }

    response = requests.post(url, headers=headers, data=json.dumps(filters))

    data = response.json()

    if not data:
        if user_languages[user_id] != 'english':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"No matching offers found! Try to change your search options 🔎",
                                  disable_web_page_preview=True)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"Нет совпадений, попробуйте изменить настройки поиска🔎",
                                  disable_web_page_preview=True)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global user_language
    global currency
    global rental_period
    user_id = call.message.chat.id
    if user_id not in state_history:
        state_history[user_id] = []
    if call.data == 'language_russian':
        user_languages[user_id] = 'russian'
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Язык изменен! Чтобы начать заново, отправьте сообщение - /start")
    elif call.data == 'language_english':
        user_languages[user_id] = 'english'
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "The language has been changed! To start again, send a message - /start")
    if call.data == 'find_apartments':
        handle_find_apartments(call)
    elif call.data == 'change_language':
        handle_change_language(call)

    elif call.data.startswith('find_'):
        location = call.data.replace('find_', '')
        if location in selected_locations.get(user_id, []):
            selected_locations[user_id].remove(location)
        else:
            selected_locations.setdefault(user_id, []).append(location)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=translations[user_languages[user_id]]['select_neighborhood'],
                              reply_markup=generate_keyboard(user_id))

    elif call.data.startswith('budget_'):
        price = call.data.replace('budget_', '')
        if price in selected_prices.get(user_id, []):
            selected_prices[user_id].remove(price)
        else:
            selected_prices.setdefault(user_id, []).append(price)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=translations[user_languages[user_id]]['select_budget'],
                              reply_markup=generate_keyboard_prices(user_id))

    elif call.data.startswith('type_'):
        typeh = call.data.replace('type_', '')
        if typeh in selected_types.get(user_id, []):
            selected_types[user_id].remove(typeh)
        else:
            selected_types.setdefault(user_id, []).append(typeh)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=translations[user_languages[user_id]]['select_type'],
                              reply_markup=generate_keyboard_typesh(user_id))

    elif call.data.startswith('requestion_'):
        requestion = call.data.replace('requestion_', '')
        if requestion in selected_requestions.get(user_id, []):
            selected_requestions[user_id].remove(requestion)
        else:
            selected_requestions.setdefault(user_id, []).append(requestion)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=translations[user_languages[user_id]]['select_requests'],
                              reply_markup=generate_keyboard_requestions(user_id))

    elif call.data == 'rental_period_day':
        user_rental_periods[user_id] = 'Day'
        handle_rental_period(call)
    elif call.data == 'rental_period_month':
        user_rental_periods[user_id] = 'Month'
        handle_rental_period(call)
    elif call.data == 'rental_period_year':
        user_rental_periods[user_id] = 'Year'
        handle_rental_period(call)
    elif call.data == 'next':
        handle_next(call)
    elif call.data == 'cancel':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, translations[user_languages[user_id]]['cancel_text'])
    elif call.data == 'dollars':
        user_currencies[user_id] = 'dollars'
        handle_select_currency(call)
    elif call.data == 'rupiahs':
        user_currencies[user_id] = 'rupiahs'
        handle_select_currency(call)
    elif call.data == 'back':
        handle_back(call)
    elif call.data == 'search':
        search(call)


def handle_next(call):
    user_id = call.message.chat.id
    if state_history.get(user_id):
        last_state = state_history[user_id]
        if last_state == 'select_currency':
            next_budget(call)
        elif last_state == 'rental_period':
            handle_find_apartments(call)
        elif last_state == 'select_neighborhood':
            if not user_neighborhood:
                if user_languages[user_id] == 'russian':
                    bot.answer_callback_query(call.id, "Выбирете хотябы одну локацию", show_alert=True)
                else:
                    bot.answer_callback_query(call.id, "Choose at least one location", show_alert=True)
            else:
                next_types(call)
        elif last_state == 'select_types':
            next_requests(call)
        elif last_state == 'select_requests':
            next_result(call)


def next_requests(call):
    user_id = call.message.chat.id
    state_history[user_id] = 'select_requests'
    if not selected_requestions.get(user_id, []):
        selected_requestions[user_id] = ["Whatever"]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=translations[user_languages[user_id]]['select_requests'],
                          disable_web_page_preview=True)
    keyboard = generate_keyboard_requestions(user_id)
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=keyboard)


def next_types(call):
    user_id = call.message.chat.id
    state_history[user_id] = 'select_types'
    if not selected_types.get(user_id, []):
        selected_types[user_id] = ["Whatever"]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=translations[user_languages[user_id]]['select_type'],
                          disable_web_page_preview=True)
    keyboard = generate_keyboard_typesh(user_id)
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=keyboard)


def next_budget(call):
    user_id = call.message.chat.id
    state_history[user_id] = 'select_neighborhood'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=translations[user_languages[user_id]]['select_neighborhood'],
                          disable_web_page_preview=True)
    keyboard = generate_keyboard(user_id)
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=keyboard)


def handle_back(call):
    user_id = call.message.chat.id

    if state_history[user_id]:
        last_state = state_history[user_id]
        if last_state == 'find_apartments':
            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(translations[user_languages[user_id]]['find_apartments'],
                                                 callback_data='find_apartments')
            button2 = types.InlineKeyboardButton(translations[user_languages[user_id]]['show_favorites'],
                                                 callback_data='show_favorites')
            button3 = types.InlineKeyboardButton(translations[user_languages[user_id]]['change_language'],
                                                 callback_data='change_language')
            button4 = types.InlineKeyboardButton(translations[user_languages[user_id]]['leave_review'],
                                                 callback_data='leave_review')
            keyboard.add(button1)
            keyboard.add(button2)
            keyboard.add(button3)
            keyboard.add(button4)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"{call.message.from_user.first_name}, {translations[user_languages[user_id]]['welcome']}",
                                  reply_markup=keyboard)
        elif last_state == 'change_language':
            handle_change_language(call)
        elif last_state == 'rental_period':
            handle_find_apartments(call)
        elif last_state == 'select_currency':
            handle_rental_period(call)
        elif last_state == 'select_neighborhood':
            handle_select_currency(call)
        elif last_state == 'select_types':
            next_budget(call)
        elif last_state == 'select_requests':
            next_types(call)
        elif last_state == 'result':
            next_requests(call)
        elif last_state == 'search':
            next_result(call)


def handle_select_currency(call):
    user_id = call.message.chat.id
    state_history[user_id] = 'select_currency'
    if not selected_prices.get(user_id, []):
        selected_prices[user_id] = ["Whatever"]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=translations[user_languages[user_id]]['select_budget'],
                          disable_web_page_preview=True)
    keyboard = generate_keyboard_prices(call.message.chat.id)
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=keyboard)


def handle_rental_period(call):
    user_id = call.message.chat.id
    state_history[user_id] = 'rental_period'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=translations[user_languages[user_id]]['select_currency'],
                          disable_web_page_preview=True)
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(translations[user_languages[user_id]]['dollars'], callback_data='dollars')
    button2 = types.InlineKeyboardButton(translations[user_languages[user_id]]['rupiahs'], callback_data='rupiahs')
    button4 = types.InlineKeyboardButton(translations[user_languages[user_id]]['back'], callback_data='back')
    button5 = types.InlineKeyboardButton(translations[user_languages[user_id]]['cancel'], callback_data='cancel')
    keyboard.add(button1)
    keyboard.add(button2)
    keyboard.row(button4, button5)
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=keyboard)


def handle_change_language(call):

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=translations[user_languages[call.message.chat.id]]['choose_language'],
                          disable_web_page_preview=True)
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Русский", callback_data='language_russian')
    button2 = types.InlineKeyboardButton("English", callback_data='language_english')
    keyboard.add(button1)
    keyboard.add(button2)
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=keyboard)


def handle_find_apartments(call):
    user_id = call.message.chat.id
    state_history[user_id] = 'find_apartments'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=translations[user_languages[user_id]]['rental_period'],
                          disable_web_page_preview=True)
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(translations[user_languages[user_id]]['day'], callback_data='rental_period_day')
    button2 = types.InlineKeyboardButton(translations[user_languages[user_id]]['month'], callback_data='rental_period_month')
    button3 = types.InlineKeyboardButton(translations[user_languages[user_id]]['year'], callback_data='rental_period_year')
    button4 = types.InlineKeyboardButton(translations[user_languages[user_id]]['back'], callback_data='back')
    button5 = types.InlineKeyboardButton(translations[user_languages[user_id]]['cancel'], callback_data='cancel')
    keyboard.add(button1)
    keyboard.add(button2)
    keyboard.add(button3)
    keyboard.row(button4, button5)
    bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, reply_markup=keyboard)


bot.polling(none_stop=True)
