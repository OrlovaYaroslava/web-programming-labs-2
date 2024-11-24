from flask import Blueprint, make_response, request, render_template, redirect,session
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


# Обработчик для суммирования
@lab4.route('/lab4/add-form', methods=['GET'])
def add_form():
    return render_template('lab4/add-form.html')

@lab4.route('/lab4/add', methods=['POST'])
def add():
    x1 = request.form.get('x1') or 0
    x2 = request.form.get('x2') or 0
    result = int(x1) + int(x2)
    return render_template('lab4/result.html', operation='Суммирование', x1=x1, x2=x2, result=result, operation_sign="+")

# Обработчик для умножения
@lab4.route('/lab4/mul-form', methods=['GET'])
def mul_form():
    return render_template('lab4/mul-form.html')

@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1') or 1
    x2 = request.form.get('x2') or 1
    result = int(x1) * int(x2)
    return render_template('lab4/result.html', operation='Умножение', x1=x1, x2=x2, result=result, operation_sign="*")

# Обработчик для вычитания
@lab4.route('/lab4/sub-form', methods=['GET'])
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if not x1 or not x2:
        error = "Оба поля должны быть заполнены!"
        return render_template('lab4/result.html', error=error)
    
    result = int(x1) - int(x2)
    return render_template('lab4/result.html', operation='Вычитание', x1=x1, x2=x2, result=result, operation_sign="-")

# Обработчик для возведения в степень
@lab4.route('/lab4/pow-form', methods=['GET'])
def pow_form():
    return render_template('lab4/pow-form.html')

@lab4.route('/lab4/pow', methods=['POST'])
def pow():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if not x1 or not x2:
        error = "Оба поля должны быть заполнены!"
        return render_template('lab4/result.html', error=error)
    
    if int(x1) == 0 and int(x2) == 0:
        error = "Оба значения не могут быть нулями одновременно!"
        return render_template('lab4/result.html', error=error)

    result = int(x1) ** int(x2)
    return render_template('lab4/result.html', operation='Возведение в степень', x1=x1, x2=x2, result=result, operation_sign="^")


# Главная страница с формой
@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


# Обработчик формы для деления чисел
@lab4.route('/lab4/div', methods=['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    # Проверка на пустые поля и деление на ноль
    if not x1 or not x2:
        return render_template('lab4/div.html', error="Оба поля должны быть заполнены!")
    
    # Проверяем, что оба значения являются числами
    if x1.isdigit() and x2.isdigit():
        x1 = int(x1)
        x2 = int(x2)
        
        if x2 == 0:
            return render_template('lab4/div.html', error="Деление на ноль невозможно!")
        
        result = x1 / x2
        return render_template('lab4/div.html', x1=x1, x2=x2, result=result)
    
    else:
        return render_template('lab4/div.html', error="Оба поля должны содержать числа!")
    


tree_count = 0  # Глобальная переменная для хранения количества деревьев

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')
    if operation == 'plant' and tree_count < 15:
        tree_count += 1
    elif operation == 'cut' and tree_count > 0:
        tree_count -= 1
    
    return redirect('/lab4/tree')


users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр Иванов', 'gender': 'male'},
    {'login': 'bob', 'password': '555', 'name': 'Боб Смит', 'gender': 'male'},
    # Добавьте других пользователей
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    error = None
    login = ''
    authorized = False

    if request.method == 'POST':
        login = request.form.get('login', '')
        password = request.form.get('password', '')

        # Проверка на пустые значения
        if not login:
            error = 'Не введён логин'
        elif not password:
            error = 'Не введён пароль'
        else:
            for user in users:
                if login == user['login'] and password == user['password']:
                    session['login'] = login
                    session['name'] = user['name']
                    authorized = True
                    return redirect('/lab4/login')

            error = 'Неверные логин и/или пароль'

    # Проверяем, если пользователь уже авторизован
    if 'login' in session:
        authorized = True
        login = session['login']

    return render_template('lab4/login.html', login=login, error=error, authorized=authorized)


@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        name = request.form.get('name')

        if not login or not password or not name:
            error = 'Заполните все поля'
        elif any(user['login'] == login for user in users):
            error = 'Пользователь с таким логином уже существует'
        else:
            users.append({'login': login, 'password': password, 'name': name})
            return redirect('/lab4/login')

    return render_template('lab4/register.html', error=error)


@lab4.route('/lab4/users')
def users_list():
    if 'login' not in session:
        return redirect('/lab4/login')

    return render_template('lab4/users.html', users=users)


@lab4.route('/lab4/delete_user', methods=['POST'])
def delete_user():
    if 'login' in session:
        login = session['login']
        global users
        users = [user for user in users if user['login'] != login]
        session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/edit_user', methods=['GET', 'POST'])
def edit_user():
    if 'login' not in session:
        return redirect('/lab4/login')

    login = session['login']
    user = next((user for user in users if user['login'] == login), None)
    
    if request.method == 'POST':
        new_name = request.form.get('name')
        new_password = request.form.get('password')

        if user:
            user['name'] = new_name
            user['password'] = new_password
        return redirect('/lab4/users')

    return render_template('lab4/edit_user.html', user=user)





@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    error = None
    temperature = None
    snowflakes = ""

    if request.method == 'POST':
        try:
            temperature = float(request.form.get('temperature', ''))
        except ValueError:
            error = "Ошибка: не задана температура"
            return render_template('lab4/fridge.html', error=error, temperature=temperature, snowflakes=snowflakes)

        if temperature < -12:
            error = "Не удалось установить температуру — слишком низкое значение"
        elif temperature > -1:
            error = "Не удалось установить температуру — слишком высокое значение"
        elif -12 <= temperature <= -9:
            snowflakes = "❄️❄️❄️"
        elif -8 <= temperature <= -5:
            snowflakes = "❄️❄️"
        elif -4 <= temperature <= -1:
            snowflakes = "❄️"
        else:
            error = "Ошибка: не задана температура"

    return render_template('lab4/fridge.html', error=error, temperature=temperature, snowflakes=snowflakes)


@lab4.route('/lab4/grain', methods=['GET', 'POST'])
def grain():
    error = None
    grain = None
    weight = 0
    price = 0
    discount = 0

    prices = {
        'ячмень': 12345,
        'овёс': 8522,
        'пшеница': 8722,
        'рожь': 14111
    }

    if request.method == 'POST':
        grain = request.form.get('grain')
        try:
            weight = float(request.form.get('weight', ''))
        except ValueError:
            error = "Вес не был указан или введено неверное значение."
            return render_template('lab4/grain.html', error=error, grain=grain, weight=weight, price=price, discount=discount)

        if grain not in prices:
            error = "Зерно не указано."
        elif weight <= 0:
            error = "Вес указан неверно или слишком мал для заказа."
        elif weight > 500:
            error = "Такого объёма зерна сейчас нет в наличии."
        else:
            price = prices[grain] * weight

            if weight > 50:
                discount = 10
                price *= 0.9

    return render_template('lab4/grain.html', error=error, grain=grain, weight=weight, price=price, discount=discount)