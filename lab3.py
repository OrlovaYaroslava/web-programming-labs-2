from flask import Blueprint, make_response, request, render_template, redirect
lab3 = Blueprint('lab3', __name__)

# Вывод cookie на странице
@lab3.route('/lab3/')
def lab3_page():
    name = request.cookies.get('name', 'None')  
    name_color = request.cookies.get('name_color', 'black')  
    return render_template('lab3/lab3.html', name=name, name_color=name_color)


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
