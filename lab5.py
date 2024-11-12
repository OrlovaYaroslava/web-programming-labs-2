from flask import Blueprint, make_response, request, render_template, redirect, session, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

# Функция для подключения к базе данных
def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='yaroslava_orlova_knowledge_base',
            user='yaroslava_orlova_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        db_path = path.join(path.dirname(path.realpath(__file__)), 'database.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

# Функция для закрытия соединения
def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@lab5.route('/lab5')
def lab5_home():
    user_name = session.get('login', 'Anonymous')
    return render_template('lab5/lab5.html', user_name=user_name)


@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        if not login or not password:
            error = "Заполните все поля"
            return render_template('lab5/register.html', error=error)

        conn, cur = db_connect()
        
        cur.execute("SELECT login FROM users WHERE login = %s", (login,))
        if cur.fetchone():
            db_close(conn, cur)
            error = "Такой пользователь уже существует"
            return render_template('lab5/register.html', error=error)
        
        password_hash = generate_password_hash(password)
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s)", (login, password_hash))
        db_close(conn, cur)

        return render_template('lab5/success.html')

    return render_template('lab5/register.html')


@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        if not login or not password:
            error = "Заполните все поля"
            return render_template('lab5/login.html', error=error)
        
        conn, cur = db_connect()

        cur.execute("SELECT * FROM users WHERE login = %s", (login,))
        user = cur.fetchone()

        db_close(conn, cur)

        if user and check_password_hash(user['password'], password):
            session['login'] = login
            return render_template('lab5/success_login.html', login=login)
        else:
            error = "Неверный логин и/или пароль"
    return render_template('lab5/login.html', error=error)


@lab5.route('/lab5/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect(url_for('lab5.lab5_home'))


# Маршрут для создания статьи
@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    if 'login' not in session:
        return redirect(url_for('lab5.login'))

    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('article_text')
        
        conn, cur = db_connect()

        cur.execute("SELECT id FROM users WHERE login = %s", (session['login'],))
        user_id = cur.fetchone()['id']

        cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (%s, %s, %s)", (user_id, title, article_text))
        db_close(conn, cur)

        return redirect(url_for('lab5.lab5_home'))

    return render_template('lab5/create_article.html')


@lab5.route('/lab5/list', methods=['GET'])
def list_articles():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    # Получаем ID пользователя по логину
    cur.execute("SELECT id FROM users WHERE login = %s", (login,))
    user = cur.fetchone()

    if user:
        user_id = user['id']
        # Получаем статьи, принадлежащие этому пользователю
        cur.execute("SELECT * FROM articles WHERE user_id = %s", (user_id,))
        articles = cur.fetchall()
    else:
        articles = []

    db_close(conn, cur)
    return render_template('lab5/articles.html', articles=articles)
