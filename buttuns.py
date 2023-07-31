from telebot import types

#кнопка для для отправки номера
def num_button():
    #созаем пространство для отправки
    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)

    #создаем сами кнопки
    num=types.KeyboardButton('отправит номер', request_contact=True)

    #добавляем кнопки в пространство
    kb.add(num)
    return kb


def loc_button():
    # создаем пространство для кнопки
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    #создаем самы кнопки
    loc = types.KeyboardButton('отправит локатции', request_location=True)

    # добавляем кнопки в пространство
    kb.add(loc)
    return kb

#кнопки для вывода
def main_menu_buttons(products_from_db):

    #создаем пространство для кнопки
    kb=types.InlineKeyboardMarkup(row_width=3)

    #создаем несгораемый кнопки
    cart=types.InlineKeyboardButton(text='Корзина', callback_data='cart')

    #создаем кнопки с продуктами
    all_products=[types.InlineKeyboardButton(text=f'{i[1]}', callback_data=f'{i[2]}') for i in products_from_db]

    #добавляем кнопки в пространство
    kb.row(cart)
    kb.add(*all_products)
    return kb

#функсия для скритиа кнопки
def remove():
    types.ReplyKeyboardMarkup()