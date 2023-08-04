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
    all_products=[types.InlineKeyboardButton(text=f'{i[1]}', callback_data=f'{i[0]}') for i in products_from_db]

    #добавляем кнопки в пространство
    kb.row(cart)
    kb.add(*all_products)
    return kb

#функсия для скритиа кнопки
def remove():
    types.ReplyKeyboardRemove()

#knopki vibora kolichestvo tovarov
def choose_product_count(amount=1, plus_or_minus=''):
    #sozdaem prostransto dlya knopok
    kb=types.InlineKeyboardMarkup(row_width=3)
    #sozdaem sami knopki
    back=types.InlineKeyboardButton(text='назад', callback_data="back")
    plus=types.InlineKeyboardButton(text='+', callback_data='increment')
    minus=types.InlineKeyboardButton(text='-', callback_data='decrement')
    count=types.InlineKeyboardButton(text=str(amount), callback_data=str(amount))
    add_to_cart=types.InlineKeyboardButton(text='Добавит в карзину', callback_data='to_cart')

    #otslejovaniya plus i minusa
    if plus_or_minus=='increment':
        new_amount=int(amount)+1
        count = types.InlineKeyboardButton(text=str(new_amount), callback_data=str(new_amount))
    elif plus_or_minus=='decrement':
        if amount>1:
            new_amount=int(amount)-1
            count = types.InlineKeyboardButton(text=str(new_amount), callback_data=str(new_amount))

    #dobavit knopki v prostranstvo
    kb.add(minus, count, plus)
    kb.row(back)
    kb.row(add_to_cart)
    return kb

#knopki dlya karzini
def cart_buttons():
    #sozdaem prostranstvo dlya knopok
    kb=types.ReplyKeyboardMarkup(row_width=3)

    #sozdaem sami knopki
    order=types.InlineKeyboardButton(text='Оформит заказ', callback_data='order')
    clear=types.InlineKeyboardButton(text='очистит корзину', callback_data='clear')
    back=types.InlineKeyboardButton(text='назад', callback_data='back')

    #dobavim knopki v prostranstvo
    kb.add(clear, order, back)

    return kb
