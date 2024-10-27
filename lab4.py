from flask import Blueprint, make_response, request, render_template, redirect
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


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