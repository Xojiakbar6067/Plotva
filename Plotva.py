import telebot, Database as db, buttuns as bt
from geopy import Nominatim

#подключения к боту
bot=telebot.TeleBot('6608170958:AAGZWOhdjec27K8khpb747pnQ-mlznNnh5Q')
geolocator=Nominatim(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')

#обработчик команди /start
@bot.message_handler(commands=['start'])
def start_message(message):
    global user_id
    user_id=message.from_user.id
    #проверка на наличии в базе
    check_user=db.checker(user_id)
    if check_user:
        products=db.get_pr_name_id()
        bot.send_message(user_id, 'Добро пожаловат!', reply_markup=bt.remove())
        bot.send_message(user_id, 'выберите пункт меню', reply_markup=bt.main_menu_buttons(products))
    else:
        bot.send_message(user_id, 'Приветствую вас! Начнем регистратрацию, напишите своё имя', reply_markup=bt.remove())
        #переход на этаб получения имени
        bot.register_next_step_handler(message, get_name)
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
#запуск бота
bot.polling(none_stop=True)