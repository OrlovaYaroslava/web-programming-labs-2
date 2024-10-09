from flask import Blueprint, make_response, request, render_template, redirect
lab3 = Blueprint('lab3', __name__)

# Вывод cookie на странице
@lab3.route('/lab3/')
def lab3_page():
    name = request.cookies.get('name', 'None')  # Получение cookie name
    name_color = request.cookies.get('name_color', 'black')  # Получение цвета имени
    return render_template('lab3/lab3.html', name=name, name_color=name_color)


# Установка cookies
@lab3.route('/lab3/cookie')
def set_cookie():
    resp = make_response(redirect('/lab3/'))  # Редирект на страницу /lab3/
    resp.set_cookie('name', 'Alex')  # Установка cookie name
    resp.set_cookie('age', '20')  # Установка cookie age
    resp.set_cookie('name_color', 'magenta')  # Установка cookie цвета имени
    return resp


# Удаление cookies
@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp
