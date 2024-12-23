from flask import Blueprint, request, jsonify, session, render_template, current_app, redirect, url_for
from datetime import datetime
import psycopg2
import sqlite3
from os import path
from db import db
from db.models import Users, Articles
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_login import login_required, current_user

lab8 = Blueprint('lab8', __name__)

# Инициализация LoginManager
login_manager = LoginManager()
login_manager.login_view = 'lab8.login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@lab8.route('/lab8')
def lab8_home():
    user_name = current_user.login if current_user.is_authenticated else 'Anonymous'
    return render_template('lab8/lab8.html', user_name=user_name)


# Регистрация
from flask_login import login_user

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

    # Автоматический логин нового пользователя
    login_user(new_user, remember=False)

    # Перенаправляем на главную страницу
    return redirect(url_for('lab8.lab8_home'))



# Вход в систему
@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')

    # Получаем логин, пароль и значение чекбокса из формы
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_me = request.form.get('remember') is not None  # Возвращает True, если чекбокс установлен

    # Проверяем, существует ли пользователь
    user = Users.query.filter_by(login=login_form).first()

    if user and check_password_hash(user.password, password_form):
        # Авторизация с учётом параметра remember
        login_user(user, remember=remember_me)
        return redirect(url_for('lab8.lab8_home'))

    # Если данные неверны
    error = 'Ошибка входа: логин и/или пароль неверны'
    return render_template('lab8/login.html', error=error)



# Выход из системы
@lab8.route('/lab8/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('lab8.lab8_home'))


@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')

    # Получаем данные из формы
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = request.form.get('is_favorite') == 'on'  # Возвращает True, если чекбокс установлен
    is_public = request.form.get('is_public') == 'on'      # Возвращает True, если чекбокс установлен

    # Проверяем, что заголовок и текст статьи не пустые
    if not title or not article_text:
        error = 'Заголовок и текст статьи не могут быть пустыми'
        return render_template('lab8/create.html', error=error)

    # Создаём статью и сохраняем её в базу данных
    new_article = Articles(
        login_id=current_user.id,
        title=title,
        article_text=article_text,
        is_favorite=is_favorite,
        is_public=is_public,
        likes=0
    )
    db.session.add(new_article)
    db.session.commit()

    # Перенаправляем на страницу со списком статей
    return redirect(url_for('lab8.article_list'))


@lab8.route('/lab8/articles', methods=['GET'])
@login_required
def article_list():
    articles = Articles.query.filter_by(login_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=articles)


#Маршрут для редактирования статьи
@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    # Ищем статью по ID
    article = Articles.query.get_or_404(article_id)

    # Проверяем, что текущий пользователь — автор статьи
    if article.login_id != current_user.id:
        return "Вы не можете редактировать эту статью", 403

    if request.method == 'GET':
        # Отображаем текущие данные статьи в форме
        return render_template('lab8/edit.html', article=article)

    # Получаем обновлённые данные из формы
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = request.form.get('is_favorite') == 'on'  # Возвращает True, если чекбокс установлен
    is_public = request.form.get('is_public') == 'on'      # Возвращает True, если чекбокс установлен

    # Проверяем, что заголовок и текст статьи не пустые
    if not title or not article_text:
        error = 'Заголовок и текст статьи не могут быть пустыми'
        return render_template('lab8/edit.html', article=article, error=error)

    # Обновляем данные статьи
    article.title = title
    article.article_text = article_text
    article.is_favorite = is_favorite
    article.is_public = is_public

    db.session.commit()

    # Перенаправляем на страницу со списком статей
    return redirect(url_for('lab8.article_list'))


@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    # Находим статью по ID
    article = Articles.query.get_or_404(article_id)

    # Проверяем, что текущий пользователь является автором статьи
    if article.login_id != current_user.id:
        return "Вы не можете удалить эту статью", 403

    # Удаляем статью из базы данных
    db.session.delete(article)
    db.session.commit()

    # Перенаправляем на страницу со списком статей
    return redirect(url_for('lab8.article_list'))
