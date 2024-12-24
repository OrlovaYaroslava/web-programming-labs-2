# Импортируем необходимые библиотеки
from flask import Flask, Blueprint, request, jsonify, session, render_template, redirect, flash, current_app
import psycopg2
import sqlite3
import re
from werkzeug.security import generate_password_hash, check_password_hash
from os import path
rgz = Blueprint('rgz', __name__)
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Ключ для сессий

# Функция для валидации логина
def is_valid_username(username):
    # Логин должен состоять из латинских букв, цифр и знаков препинания, длиной от 3 до 30 символов
    return bool(re.match(r'^[a-zA-Z0-9._-]{3,30}$', username))

# Функция для валидации пароля
def is_valid_password(password):
    # Пароль должен состоять из латинских букв, цифр и знаков препинания, длиной от 6 до 50 символов
    return bool(re.match(r'^[a-zA-Z0-9!@#$%^&*()_+=\-{}[\]:;"\'<>,.?/\\|]{6,50}$', password))

# Конфигурация приложения (выбор типа базы данных)
app.config['DB_TYPE'] = 'postgres'  # 'postgres' или 'sqlite'

# Функция подключения к базе данных
def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='yaroslava_recipes_db',
            user='yaroslava_orlova_knowledge_base',
            password='123'
        )
        cur = conn.cursor()
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

# Закрытие соединения с базой
def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@rgz.route('/rgz/')
def main():
    return render_template('rgz/rgz.html')


@rgz.route('/rgz/register', methods=['GET', 'POST'])
def register():
    def is_valid_username(username):
        import re
        return bool(re.match(r'^[a-zA-Z0-9._-]{3,30}$', username))

    def is_valid_password(password):
        import re
        return bool(re.match(r'^[a-zA-Z0-9!@#$%^&*()_+=\-{}[\]:;"\'<>,.?/\\|]{6,50}$', password))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if not is_valid_username(username):
            flash('Неверный формат логина.', 'error')
            return render_template('rgz/register.html')
        if not is_valid_password(password):
            flash('Неверный формат пароля.', 'error')
            return render_template('rgz/register.html')
        if password != confirm_password:
            flash('Пароли не совпадают.', 'error')
            return render_template('rgz/register.html')

        hashed_password = generate_password_hash(password)  # Хэшируем пароль

        conn, cur = db_connect()
        try:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT * FROM users WHERE username = %s;", (username,))
            else:
                cur.execute("SELECT * FROM users WHERE username = ?;", (username,))
            existing_user = cur.fetchone()

            if existing_user:
                flash('Пользователь с таким логином уже существует.', 'error')
                return render_template('rgz/register.html')

            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s);",
                            (username, hashed_password, 'user'))
            else:
                cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?);",
                            (username, hashed_password, 'user'))
        finally:
            db_close(conn, cur)

        flash('Вы успешно зарегистрировались!', 'success')
        return redirect('/rgz/login')

    return render_template('rgz/register.html')



@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn, cur = db_connect()
        try:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT username, password, role FROM users WHERE username = %s;", (username,))
            else:
                cur.execute("SELECT username, password, role FROM users WHERE username = ?;", (username,))
            user = cur.fetchone()
        finally:
            db_close(conn, cur)

        if user and check_password_hash(user[1], password):  # Проверяем хэш пароля
            session['username'] = user[0]  # Логин пользователя
            session['role'] = user[2]      # Роль пользователя (admin/user)
            flash('Вы успешно вошли в систему!', 'success')
            return redirect('/rgz')
        else:
            flash('Неверное имя пользователя или пароль.', 'error')

    return render_template('rgz/login.html')



@rgz.route('/rgz/logout')
def logout():
    # Сохраняем рецепты текущего пользователя перед выходом
    if 'current_user' in session:
        if 'user_recipes' not in session:
            session['user_recipes'] = {}
        session['user_recipes'][session['current_user']] = session.get('current_recipes', [])

    # Очищаем сессию
    session.clear()
    flash('Вы успешно вышли из системы.', 'success')
    return redirect('/rgz')

@rgz.route('/rgz/recipes')
def recipes():
    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id, name, description FROM recipes;")
        else:
            cur.execute("SELECT id, name, description FROM recipes;")
        recipes_list = cur.fetchall()
    finally:
        db_close(conn, cur)

    return render_template('rgz/recipes.html', recipes=recipes_list)


@rgz.route('/rgz/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if 'role' not in session or session['role'] != 'admin':
        flash('У вас нет прав для добавления рецептов', 'error')
        return redirect('/rgz/')

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        ingredients = request.form['ingredients']
        steps = request.form['steps']
        photo_url = request.form['photo_url']

        conn, cur = db_connect()
        try:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute(
                    "INSERT INTO recipes (name, description, ingredients, steps, photo_url) VALUES (%s, %s, %s, %s, %s);",
                    (name, description, ingredients, steps, photo_url)
                )
            else:
                cur.execute(
                    "INSERT INTO recipes (name, description, ingredients, steps, photo_url) VALUES (?, ?, ?, ?, ?);",
                    (name, description, ingredients, steps, photo_url)
                )
        finally:
            db_close(conn, cur)

        flash('Рецепт успешно добавлен!', 'success')
        return redirect('/rgz/recipes')

    return render_template('rgz/add_recipe.html')

@rgz.route('/rgz/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM recipes WHERE id = %s;", (recipe_id,))
        else:
            cur.execute("SELECT * FROM recipes WHERE id = ?;", (recipe_id,))
        recipe = cur.fetchone()
    finally:
        db_close(conn, cur)

    if not recipe:
        flash('Рецепт не найден!', 'error')
        return redirect('/rgz/recipes')

    # Преобразование рецепта в словарь
    recipe_dict = {
        'id': recipe[0],
        'name': recipe[1],
        'description': recipe[2],
        'ingredients': recipe[3],
        'steps': recipe[4],
        'photo_url': recipe[5]
    }

    return render_template('rgz/recipe_detail.html', recipe=recipe_dict, recipe_id=recipe_id)



@rgz.route('/rgz/delete_recipe/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('У вас нет прав для удаления рецептов', 'error')
        return redirect('/rgz/')

    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM recipes WHERE id = %s;", (recipe_id,))
        else:
            cur.execute("DELETE FROM recipes WHERE id = ?;", (recipe_id,))
    finally:
        db_close(conn, cur)

    flash('Рецепт успешно удален!', 'success')
    return redirect('/rgz/recipes')

@rgz.route('/rgz/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('У вас нет прав для редактирования рецептов', 'error')
        return redirect('/rgz/')

    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM recipes WHERE id = %s;", (recipe_id,))
        else:
            cur.execute("SELECT * FROM recipes WHERE id = ?;", (recipe_id,))
        recipe = cur.fetchone()
    finally:
        db_close(conn, cur)

    if not recipe:
        flash('Рецепт не найден!', 'error')
        return redirect('/rgz/recipes')

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        ingredients = request.form['ingredients']
        steps = request.form['steps']
        photo_url = request.form['photo_url']

        conn, cur = db_connect()
        try:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute(
                    "UPDATE recipes SET name = %s, description = %s, ingredients = %s, steps = %s, photo_url = %s WHERE id = %s;",
                    (name, description, ingredients, steps, photo_url, recipe_id)
                )
            else:
                cur.execute(
                    "UPDATE recipes SET name = ?, description = ?, ingredients = ?, steps = ?, photo_url = ? WHERE id = ?;",
                    (name, description, ingredients, steps, photo_url, recipe_id)
                )
        finally:
            db_close(conn, cur)

        flash('Рецепт успешно обновлен!', 'success')
        return redirect('/rgz/recipes')
        # Передача данных в шаблон
    
    return render_template('rgz/edit_recipe.html', recipe={
        'id': recipe[0],
        'name': recipe[1],
        'description': recipe[2],
        'ingredients': recipe[3],
        'steps': recipe[4],
        'photo_url': recipe[5]
    },recipe_id=recipe_id)

    

@rgz.route('/rgz/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip().lower()  # Удаляем лишние пробелы и приводим к нижнему регистру
    ingredient_query = request.args.get('ingredient_query', '').strip().lower()  # Аналогично для ингредиентов
    search_mode = request.args.get('search_mode', 'all')  # 'all' или 'any' для ингредиентов

    conn, cur = db_connect()
    try:
        # Инициализируем список рецептов
        recipes_list = []

        # Поиск по названию
        if query:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT * FROM recipes WHERE LOWER(name) LIKE %s;", ('%' + query + '%',))
            else:
                cur.execute("SELECT * FROM recipes WHERE LOWER(name) LIKE ?;", ('%' + query + '%',))
            recipes_list = cur.fetchall()
        else:
            # Если название не введено, выбираем все рецепты
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT * FROM recipes;")
            else:
                cur.execute("SELECT * FROM recipes;")
            recipes_list = cur.fetchall()

        # Фильтрация по ингредиентам, если задано
        if ingredient_query:
            ingredients = [ingredient.strip() for ingredient in ingredient_query.split(',') if ingredient.strip()]
            filtered_recipes = []

            for recipe in recipes_list:
                # Ингредиенты рецепта из базы данных
                recipe_ingredients = [ingredient.strip().lower() for ingredient in recipe[3].split(',')]  # Предполагается, что ингредиенты в 4-й колонке
                if search_mode == 'all':
                    # Все ингредиенты должны совпадать
                    if all(ingredient in recipe_ingredients for ingredient in ingredients):
                        filtered_recipes.append(recipe)
                elif search_mode == 'any':
                    # Хотя бы один ингредиент должен совпадать
                    if any(ingredient in recipe_ingredients for ingredient in ingredients):
                        filtered_recipes.append(recipe)

            # Обновляем список рецептов
            recipes_list = filtered_recipes

    finally:
        db_close(conn, cur)

    # Отправляем результаты поиска в шаблон
    return render_template(
        'rgz/search.html',
        recipes=recipes_list,
        query=query,
        ingredient_query=ingredient_query,
        search_mode=search_mode,
    )

@rgz.route('/rgz/account', methods=['GET', 'POST'])
def account():
    if 'username' not in session:
        flash('Вы не авторизованы!', 'error')
        return redirect('/rgz/login')

    username = session['username']

    if request.method == 'POST':
        conn, cur = db_connect()
        try:
            # Удаляем аккаунт пользователя из базы данных
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("DELETE FROM users WHERE username = %s;", (username,))
            else:
                cur.execute("DELETE FROM users WHERE username = ?;", (username,))
        finally:
            db_close(conn, cur)

        # Завершаем сессию
        session.clear()
        flash('Ваш аккаунт успешно удалён.', 'success')
        return redirect('/rgz/')

    return render_template('rgz/account.html', username=username)
