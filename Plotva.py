import telebot, Database as db, buttuns as bt
from telebot.types import ReplyKeyboardRemove as remove
from geopy import Nominatim

#подключения к боту
bot=telebot.TeleBot('6608170958:AAGZWOhdjec27K8khpb747pnQ-mlznNnh5Q')
geolocator=Nominatim(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
#vremennie dannie
users={}
#языки
ru={'satrt': 'dobro pojalovat'}
uz={'start': 'xush kelibsiz'}
#обработчик команди /start
@bot.message_handler(commands=['start'])
def start_message(message):
    global user_id
    user_id=message.from_user.id
    #проверка на наличии в базе
    check_user=db.checker(user_id)
    if check_user:
        products=db.get_pr_name_id()
        bot.send_message(user_id, 'Добро пожаловат!', reply_markup=remove())
        bot.send_message(user_id, 'выберите пункт меню', reply_markup=bt.main_menu_buttons(products))
    else:
        bot.send_message(user_id, 'Приветствую вас! Начнем регистратрацию, напишите своё имя', reply_markup=remove())
        #переход на этаб получения имени
        bot.register_next_step_handler(message, get_name)

def language(message):
    products=db.get_pr_name_id()
    if message.text== 'ru':
        bot.send_message(user_id, ru['start'], reply_markup=bt.main_menu_buttons(products))
    elif message.text=='uzb':
        bot.send_message(user_id, uz['start'], reply_markup=bt.main_menu_buttons(products))
#этап получения имени
def get_name(message):
    user_name=message.text
    bot.send_message(user_id, 'отлично! А теперь отправте номер!', reply_markup=bt.num_button())
    #этап получения номера
    bot.register_next_step_handler(message, get_num, user_name)

#этап получения локации
def get_num(message, user_name):
    #если нажал на кнопку
    if message.contact:
        user_num= message.contact.phone_number
        bot.send_message(user_id, 'А тепер отправте локатсию!', reply_markup=bt.loc_button())
        #переход на этап получения локации
        bot.register_next_step_handler(message, get_loc, user_name, user_num)
    #если не нажимал на кнопку
    else:
        bot.send_message(user_id, 'отправте свой контакт через кнопку!')
        bot.register_next_step_handler(message, get_num, user_name)
#функсия выбора количество товаров
@bot.callback_query_handler(lambda call: call.data in ['back', 'to_cart', 'increment', 'decrement'])
def get_user_count(call):
    message_id=call.message.message_id
    chat_id=call.message.chat.id

    if call.data=='increment':
        count=users[chat_id]['pr_amount']

        users[chat_id]['pr_amount']+=1
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=bt.choose_product_count(count, 'increment'))
    elif call.data=='decrement':
        count = users[chat_id]['pr_amount']

        users[chat_id]['pr_amount'] -= 1
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=bt.choose_product_count(count, 'decrement'))
    elif call.data=='back':
        products=db.get_pr_name_id()
        bot.edit_message_text('выберите пункт меню:', chat_id=chat_id, message_id=message_id, reply_markup=bt.main_menu_buttons(products))

    elif call.data=='to_cart':
        products=db.get_pr_name_id()
        product_count=users[chat_id]['pr_amount']
        user_total=products[0][3]*product_count
        user_product=db.get_pr_name(users[chat_id]['pr_name'])
        db.add_to_cart(chat_id, user_product[0], product_count, user_total)
        bot.edit_message_text('ваш товар был добавлен в корзину! хотите заказат что-то еще?', chat_id=chat_id, message_id=call.message.message_id, reply_markup=bt.main_menu_buttons(products))

#корзина
@bot.callback_query_handler(lambda call: call.data in ['cart', 'order', 'clear', 'back'])
def cart_handler(call):
    chat_id=call.message.chat.id
    message_id=call.message.message_id
    products=db.get_pr_name_id()
    if call.data=='clear':
        db.clear_cart(user_id)
        bot.edit_message_text('корзина очишена! желаете ещё что-нибуд?', chat_id=chat_id, message_id=message_id, reply_markup=bt.main_menu_buttons(products))
    elif call.data=='order':
        bot.send_message(113996076, 'новый заказ!')
        db.clear_cart(user_id)
        bot.edit_message_text('заказ был оформлен и скоро будет доставлен! Желаете заказат что-то ещё?', chat_id=chat_id, message_id=message_id, reply_markup=bt.main_menu_buttons(products))
    elif call.data == 'back':
        products = db.get_pr_name_id()
        bot.edit_message_text('выберите пункт меню:', chat_id=chat_id, message_id=message_id, reply_markup=bt.main_menu_buttons(products))
    elif call.data=='cart':
        text=db.show_cart(user_id)
        bot.edit_message_text(f'карзина:\nТовар:{text[0]}\nколичество:{text[1]}\nИтог:{text[2]}', chat_id=chat_id, message_id=message_id, reply_markup=bt.cart_buttons())
#этап получения локации
def get_loc(message, user_name, user_num):
    #если нажал по кнопку
    if message.location:
        user_loc=geolocator.reverse(f'{message.location.longitude}, {message.location.latitude}')
        #регистрация ползователя
        db.register(user_id, user_name, user_num, user_loc)
        #перевод на главное меню
        bot.send_message(user_id, 'vi uspeshno zaregistrirovalis')
        products=db.get_pr_name_id()
        bot.send_message(user_id, 'выберите пункт меню', reply_markup=bt.main_menu_buttons(products))

    #если не нажал по кнопку
    else:
        bot.send_message(user_id, 'otpravte lokatciyu cherez knopku')
        bot.register_next_step_handler(message, get_loc, user_name, user_num)

#funksiya dlya vibora kolichestvo
@bot.callback_query_handler(lambda call: int(call.data) in db.get_pr_id())
def get_user_product(call):
    chat_id=call.message.chat.id
    users[chat_id]={'pr_name': call.data, 'pr_amount':1}
    message_id=call.message.message_id
    bot.edit_message_text('виберите количество', chat_id=chat_id, message_id=message_id, reply_markup=bt.choose_product_count())

#запуск бота
bot.polling(non_stop=True)