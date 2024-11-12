from flask import Blueprint, make_response, request, render_template, redirect, session, url_for
import psycopg2
from psycopg2.extras import RealDictCursor

lab5 = Blueprint('lab5', __name__)

# Функция для подключения к базе данных
def db_connect():
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='yaroslava_orlova_knowledge_base',
        user='yaroslava_orlova_knowledge_base',
        password='123'
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)
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
        
        # Проверка на наличие логина и пароля
        if not login or not password:
            error = "Заполните все поля"
            return render_template('lab5/register.html', error=error)

        # Подключение к базе данных
        conn, cur = db_connect()
        
        # Проверка, существует ли пользователь
        cur.execute("SELECT login FROM users WHERE login = %s", (login,))
        if cur.fetchone():
            db_close(conn, cur)
            error = "Такой пользователь уже существует"
            return render_template('lab5/register.html', error=error)
        
        # Вставка нового пользователя
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s)", (login, password))
        db_close(conn, cur)

        return render_template('lab5/success.html')  # Перенаправление на страницу успеха

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
        
        # Подключение к базе данных
        conn, cur = db_connect()

        # Выполняем запрос на получение пользователя с указанным логином
        cur.execute("SELECT * FROM users WHERE login = %s", (login,))
        user = cur.fetchone()  # Получаем одну запись в формате словаря

        # Закрываем соединение
        db_close(conn, cur)

        # Проверка наличия пользователя и совпадения пароля
        if user and user['password'] == password:
            session['login'] = login
            return render_template('lab5/success_login.html', login=login)
        else:
            error = "Неверный логин и/или пароль"
    return render_template('lab5/login.html', error=error)


@lab5.route('/lab5/logout', methods=['POST'])
def logout():
    # Удаляем пользователя из сессии
    session.pop('login', None)
    # Перенаправляем на главную страницу
    return redirect(url_for('lab5.lab5_home'))
