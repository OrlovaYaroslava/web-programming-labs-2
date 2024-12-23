from flask import Blueprint, request, jsonify, session, render_template, current_app, redirect, url_for
from datetime import datetime
import psycopg2
import sqlite3
from os import path
from db import db
from db.models import Users, Articles
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import login_user, LoginManager, login_required, current_user

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8')
def lab8_home():
    user_name = session.get('login', 'Anonymous')
    return render_template('lab8/lab8.html', user_name=user_name)
#регистрация
@lab8.route('/lab8/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    # Получаем данные формы
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    # Проверяем, что логин и пароль не пустые
    if not login_form or not password_form:
        error = 'Логин и пароль не могут быть пустыми'
        return render_template('lab8/register.html', error=error)

    # Проверяем, существует ли пользователь
    user_exists = Users.query.filter_by(login=login_form).first()
    if user_exists:
        error = 'Такой пользователь уже существует'
        return render_template('lab8/register.html', error=error)

    # Хэшируем пароль и добавляем пользователя в базу
    password_hash = generate_password_hash(password_form)
    new_user = Users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    # Перенаправляем на главную страницу
    return redirect(url_for('lab8.lab8_home'))


@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')

    # Получаем логин и пароль из формы
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    # Проверяем, существует ли пользователь
    user = Users.query.filter_by(login=login_form).first()

    if user and check_password_hash(user.password, password_form):
        login_user(user, remember=False)
        return redirect(url_for('lab8.lab8_home'))
    
    error = 'Ошибка входа: логин и/или пароль неверны'
    return render_template('lab8/login.html', error=error)

@lab8.route('/lab8/articles/')
@login_required
def article_list():
    return "Список статей"
