from flask import Blueprint, make_response, request, render_template, redirect,session,url_for
lab5 = Blueprint('lab5', __name__)
import psycopg2

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

        conn = psycopg2.connect(
            dbname="yaroslava_orlova_knowledge_base",
            user="yaroslava_orlova_knowledge_base",
            password="123",
            host="localhost",
            port="5432"
        )

        cur = conn.cursor()
        
        # Проверка, существует ли пользователь
        cur.execute("SELECT login FROM users WHERE login = %s", (login,))
        if cur.fetchone():
            cur.close()
            conn.close()
            error = "Такой пользователь уже существует"
            return render_template('lab5/register.html', error=error)
        
        # Вставка нового пользователя
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s)", (login, password))
        conn.commit()
        cur.close()
        conn.close()

        return render_template('lab5/success.html')  # Перенаправление на страницу успеха

    return render_template('lab5/register.html')
