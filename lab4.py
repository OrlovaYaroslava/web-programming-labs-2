from flask import Blueprint, make_response, request, render_template, redirect
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
    if operation == 'plant' and tree_count < 10:
        tree_count += 1
    elif operation == 'cut' and tree_count > 0:
        tree_count -= 1
    
    return redirect('/lab4/tree')