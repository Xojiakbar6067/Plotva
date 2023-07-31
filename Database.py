import sqlite3
#подключения к базе данных
connection=sqlite3.connect('botbase.db', check_same_thread=False)
#связь sql c python
sql=connection.cursor()
#создания таблтцы ползователей
sql.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER, name TEXT, num TEXT, LOC TEXT);')

#таблица продуктов
sql.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, pr_name TEXT, pr_amount INTEGER, pr_price REAL, pr_des TEXT, pr_photo TEXT);')

#таблица с корзинкой
sql.execute('CREATE TABLE IF NOT EXISTS cart (user_id INTEGER, user_product TEXT, product_quantity INTEGER, total REAL);')

##методы для ползователей##

#регистрация
def register(id, name, num, loc):
    sql.execute('INSERT INTO users VALUES(?, ?, ?, ?);', (id, name, num, loc))
    connection.commit()

#проверка на наличие ползователя в базе
def checker(id):
    check=sql.execute('SELECT id FROM users WHERE id=?;', (id,))
    if check.fetchone():
        return True
    else:
        return False

        ##методы для продуктов##
#добавляем продуктов в базу данных
def add_product(pr_name, pr_amount, pr_prise, pr_des, pr_photo):
    sql.execute('INSERT INTO products (pr_name, pr_amount, pr_price, pr_des, pr_photo) VALUES (?, ?, ?, ?, ?);',(pr_name, pr_amount, pr_prise, pr_des, pr_photo))
    #fiksiruem izmenenie
    connection.commit()

#вывод информации о определенном продукте
def show_info(pr_id):
    sql.execute('SELECT pr_name, pr_amount, pr_price, pr_des, pr_photo FROM products WHERE id=?;',(pr_id,)).fetchone()

#вывод всез продуктов шз базы
def show_all_products():
    all_products=sql.execute('SELECT * FROM products')
    return all_products.fetchall()

#вывод id продуктов
def get_pr_name_id():
    products=sql.execute('SELECT id, pr_name, pr_amount FROM products;')
    return products.fetchall()

def get_pr_id():
    prods=sql.execute('SELECT pr_name, id, pr_amount FROM products;').fetchall()
    sorted_prods= [i[0] for i in prods if i[2]>0]
    return sorted_prods

       ##методы для корзини##
#добавления товаров в карзину
def add_to_cart(user_id, user_product, product_quantity, total):
    sql.execute('INSERT INTO cart(user_id, user_product, product_quantity, total) VALUES (?, ?, ?, ?);',(user_id, user_product, product_quantity, total))
    amount=sql.execute('SELECT pr_amount FROM products WHERE pr_name=?;', (user_product,)).fetchone()
    sql.execute(f'UPDATE products SET pr_amount={amount[0]-product_quantity} WHERE pr_name=?;', (user_product,))
    #фиксируем изменения
    connection.commit()
#очистка корзини
def clear_cart(user_id):
    pr_name=sql.execute('SELECT user_product FROM cart WHERE user_id=?;', (user_id,)).fetchone()
    amount=sql.execute('SELECT pr_amount FROM products WHERE pr_name=?;', (pr_name,)).fetchone()
    pr_quantity=sql.execute('SELECT product_quantity FROM cart WHERE user_id=?;', (user_id,)).fetchone()
    sql.execute(f'UPDATE products SET pr_amount={amount[0]+pr_quantity} WHERE pr_name=?;', (pr_name,))
    sql.execute('DELETE FROM cart WHERE user_id=?;', (user_id))
    connection.commit()

#отоброжения карзини
def show_cart(user_id):
    cart=sql.execute('SELECT user_product, product_quantity, total FROM cart WHERE user_id=?;', (user_id))
    return cart.fetchone()
