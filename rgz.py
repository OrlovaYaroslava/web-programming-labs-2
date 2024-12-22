# Импортируем необходимые библиотеки
from flask import Flask, Blueprint, request, jsonify, session, render_template, redirect, flash, current_app
import psycopg2
import sqlite3
from os import path

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Ключ для сессий

# Временные данные для тестирования
users = [
    {"username": "admin", "password": "admin123", "role": "admin"},
    {"username": "user1", "password": "password1", "role": "user"},
    {"username": "user2", "password": "password2", "role": "user"}
]

rgz = Blueprint('rgz', __name__)

@rgz.route('/rgz/')
def main():
    return render_template('rgz/rgz.html')

@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Проверяем, существует ли пользователь
        user = next((u for u in users if u['username'] == username and u['password'] == password), None)
        if user:
            # Если 'user_recipes' еще нет в сессии, инициализируем его как пустой словарь
            if 'user_recipes' not in session:
                session['user_recipes'] = {}

            # Сохраняем рецепты текущего пользователя перед сменой аккаунта
            if 'current_user' in session:
                session['user_recipes'][session['current_user']] = session.get('current_recipes', [])

            # Настраиваем нового пользователя
            session['username'] = user['username']
            session['role'] = user['role']
            session['current_user'] = username

            # Загружаем рецепты нового пользователя
            session['current_recipes'] = session['user_recipes'].get(username, [])
            session.modified = True

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

@rgz.route('/rgz/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Проверка: пароли должны совпадать
        if password != confirm_password:
            flash('Пароли не совпадают!', 'error')
            return redirect('/rgz/register')

        # Проверка: пользователь с таким именем уже существует
        existing_user = next((u for u in users if u['username'] == username), None)
        if existing_user:
            flash('Пользователь с таким именем уже существует!', 'error')
            return redirect('/rgz/register')

        # Добавляем нового пользователя
        new_user = {"username": username, "password": password, "role": "user"}
        users.append(new_user)
        flash('Вы успешно зарегистрировались! Теперь войдите в систему.', 'success')
        return redirect('/rgz/login')

    return render_template('/rgz/register.html')

@rgz.route('/rgz/recipes')
def recipes():
    recipes_list = session.get('current_recipes', [])
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

        if 'current_recipes' not in session:
            session['current_recipes'] = []
        session['current_recipes'].append({
            'name': name,
            'description': description,
            'ingredients': ingredients,
            'steps': steps,
            'photo_url': photo_url
        })
        session.modified = True
        flash('Рецепт успешно добавлен!', 'success')
        return redirect('/rgz/recipes')

    return render_template('rgz/add_recipe.html')

@rgz.route('/rgz/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipes_list = session.get('current_recipes', [])

    if recipe_id < 0 or recipe_id >= len(recipes_list):
        flash('Рецепт не найден!', 'error')
        return redirect('/rgz/recipes')

    recipe = recipes_list[recipe_id]
    return render_template('rgz/recipe_detail.html', recipe=recipe, recipe_id=recipe_id)

@rgz.route('/rgz/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('У вас нет прав для редактирования рецептов', 'error')
        return redirect('/rgz/')

    recipes_list = session.get('current_recipes', [])

    if recipe_id < 0 or recipe_id >= len(recipes_list):
        flash('Рецепт не найден!', 'error')
        return redirect('/rgz/recipes')

    recipe = recipes_list[recipe_id]

    if request.method == 'POST':
        recipe['name'] = request.form['name']
        recipe['description'] = request.form['description']
        recipe['ingredients'] = request.form['ingredients']
        recipe['steps'] = request.form['steps']
        recipe['photo_url'] = request.form['photo_url']
        session.modified = True
        flash('Рецепт успешно обновлен!', 'success')
        return redirect('/rgz/recipes')

    return render_template('rgz/edit_recipe.html', recipe=recipe, recipe_id=recipe_id)

@rgz.route('/rgz/delete_recipe/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('У вас нет прав для удаления рецептов', 'error')
        return redirect('/rgz/')

    recipes_list = session.get('current_recipes', [])

    if recipe_id < len(recipes_list):
        del recipes_list[recipe_id]
        session['current_recipes'] = recipes_list
        session.modified = True
        flash('Рецепт успешно удален!', 'success')
    else:
        flash('Рецепт не найден!', 'error')

    return redirect('/rgz/recipes')

app.register_blueprint(rgz)


