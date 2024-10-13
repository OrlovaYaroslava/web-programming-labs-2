from flask import Blueprint, make_response, request, render_template, redirect
lab3 = Blueprint('lab3', __name__)

# Вывод cookie на странице
@lab3.route('/lab3/')
def lab3_page():
    # Проверка на наличие имени и замена 'None' на 'аноним'
    name = request.cookies.get('name', 'аноним')  
    name_color = request.cookies.get('name_color', 'black')  

    # Проверка на наличие возраста и замена 'None' на 'неизвестен'
    age = request.cookies.get('age', 'неизвестен')

    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)



# Установка cookies
@lab3.route('/lab3/cookie')
def set_cookie():
    resp = make_response(redirect('/lab3/'))  
    resp.set_cookie('name', 'Alex')  
    resp.set_cookie('age', '20')  
    resp.set_cookie('name_color', 'magenta')  
    return resp


# Удаление cookies
@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    
    user = request.args.get('user')
    age = request.args.get('age')
    sex = request.args.get('sex')

    # Проверка, что поле 'user' заполнено
    if not user:
        errors['user'] = 'Заполните поле!'

    # Проверка, что поле 'age' заполнено
    if not age:
        errors['age'] = 'Заполните поле возраста!'

    # Отправляем все параметры в шаблон
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70
    
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
    
    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success', methods=['POST'])
def success():
    return render_template('lab3/success.html')


@lab3.route('/lab3/settings', methods=['GET', 'POST'])
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    bold = request.args.get('bold')

    resp = make_response(render_template('lab3/settings.html', color=color, bg_color=bg_color, font_size=font_size, bold=bold))

    # Устанавливаем cookie только если они были переданы в запросе
    if color:
        resp.set_cookie('color', color)
    if bg_color:
        resp.set_cookie('bg_color', bg_color)
    if font_size:
        resp.set_cookie('font_size', font_size)
    if bold:
        resp.set_cookie('bold', bold)
    else:
        resp.set_cookie('bold', '', expires=0)  # Удаляем cookie bold, если параметр не был передан

    return resp


@lab3.route('/lab3/ticket', methods=['GET', 'POST'])
def ticket():
    if request.method == 'POST':
        fio = request.form.get('fio')
        polka = request.form.get('polka')
        belie = request.form.get('belie')
        bagazh = request.form.get('bagazh')
        age = int(request.form.get('age'))
        departure = request.form.get('departure')
        destination = request.form.get('destination')
        date = request.form.get('date')
        insurance = request.form.get('insurance')

        # Логика расчета цены
        if age < 18:
            ticket_type = "Детский билет"
            price = 700
        else:
            ticket_type = "Взрослый билет"
            price = 1000

        if polka in ["нижняя", "нижняя боковая"]:
            price += 100
        if belie:
            price += 75
        if bagazh:
            price += 250
        if insurance:
            price += 150

        return render_template('lab3/ticket_result.html', fio=fio, polka=polka, ticket_type=ticket_type,
                               price=price, departure=departure, destination=destination, date=date)

    return render_template('lab3/ticket_form.html')


@lab3.route('/lab3/clear_settings')
def clear_settings():
    # Создаем ответ и удаляем все куки, установленные в приложении
    resp = make_response(redirect('/lab3/settings'))
    # Удаление кук, установленных в настройках
    resp.delete_cookie('color')
    resp.delete_cookie('bg_color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('bold')
    # Удаление остальных кук
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    
    return resp


# Список товаров
products = [
    {'name': 'Apple iPhone 12', 'price': 15000, 'brand': 'Apple', 'color': 'Black'},
    {'name': 'Samsung Galaxy S21', 'price': 25000, 'brand': 'Samsung', 'color': 'White'},
    {'name': 'Dell XPS 13', 'price': 55000, 'brand': 'Dell', 'color': 'Silver'},
    {'name': 'LG OLED TV', 'price': 45000, 'brand': 'LG', 'color': 'Black'},
    {'name': 'Apple Watch Series 6', 'price': 12000, 'brand': 'Apple', 'color': 'Gold'},
    {'name': 'Samsung Galaxy Tab S7', 'price': 18000, 'brand': 'Samsung', 'color': 'Gray'},
    {'name': 'Sony WH-1000XM4', 'price': 5000, 'brand': 'Sony', 'color': 'Red'},
    {'name': 'PlayStation 5', 'price': 35000, 'brand': 'Sony', 'color': 'Black'},
    {'name': 'Canon EOS 90D', 'price': 60000, 'brand': 'Canon', 'color': 'Black'},
    {'name': 'Xiaomi Mi Electric Scooter', 'price': 30000, 'brand': 'Xiaomi', 'color': 'Green'},
    {'name': 'Acer Predator Monitor', 'price': 20000, 'brand': 'Acer', 'color': 'Black'},
    {'name': 'Logitech G502 Mouse', 'price': 3000, 'brand': 'Logitech', 'color': 'White'},
    {'name': 'Corsair K95 Keyboard', 'price': 4500, 'brand': 'Corsair', 'color': 'Black'},
    {'name': 'TP-Link Archer C6', 'price': 6000, 'brand': 'TP-Link', 'color': 'White'},
    {'name': 'Fitbit Versa 3', 'price': 10000, 'brand': 'Fitbit', 'color': 'Black'},
    {'name': 'Anker PowerCore 10000', 'price': 1500, 'brand': 'Anker', 'color': 'Blue'},
    {'name': 'SanDisk 64GB USB Drive', 'price': 800, 'brand': 'SanDisk', 'color': 'Red'},
    {'name': 'HP LaserJet Pro MFP', 'price': 17000, 'brand': 'HP', 'color': 'White'},
    {'name': 'Bosch Serie 6 Washing Machine', 'price': 35000, 'brand': 'Bosch', 'color': 'Silver'},
    {'name': 'Dyson V11 Vacuum Cleaner', 'price': 9000, 'brand': 'Dyson', 'color': 'Red'}
]

# Страница формы для поиска товаров по диапазону цен
@lab3.route('/lab3/products', methods=['GET', 'POST'])
def products_search():
    if request.method == 'POST':
        min_price = int(request.form.get('min_price'))
        max_price = int(request.form.get('max_price'))
        filtered_products = [p for p in products if min_price <= p['price'] <= max_price]
        return render_template('lab3/products_results.html', products=filtered_products)

    return render_template('lab3/products_form.html')