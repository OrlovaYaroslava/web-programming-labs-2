from flask import Blueprint, request, jsonify, session, render_template, current_app,redirect
import psycopg2
import sqlite3
from os import path
rgz = Blueprint('rgz', __name__)

@rgz.route('/rgz/')
def main():
    return render_template('rgz/rgz.html')

# Страница для добавления нового рецепта
@rgz.route('/rgz/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        # Получение данных из формы
        name = request.form['name']
        description = request.form['description']
        ingredients = request.form['ingredients']
        steps = request.form['steps']
        photo_url = request.form['photo_url']
        
        # Здесь можно будет сохранить рецепт в базу данных, но пока добавляем его в список
        new_recipe = {
            'name': name,
            'description': description,
            'ingredients': ingredients,
            'steps': steps,
            'photo_url': photo_url
        }
        
        # Временно храним рецепты в списке (для тестирования)
        if 'recipes' not in session:
            session['recipes'] = []
        session['recipes'].append(new_recipe)
        session.modified = True
        
        return redirect('/rgz/')
    
    return render_template('rgz/add_recipe.html')


# Страница для отображения всех рецептов
@rgz.route('/rgz/recipes')
def recipes():
    recipes_list = session.get('recipes', [])
    return render_template('rgz/recipes.html', recipes=recipes_list)


# Страница для поиска рецептов
@rgz.route('/rgz/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    recipes_list = session.get('recipes', [])
    
    if query:
        # Фильтрация рецептов по названию
        filtered_recipes = [r for r in recipes_list if query.lower() in r['name'].lower()]
    else:
        filtered_recipes = []
    
    return render_template('rgz/search.html', recipes=filtered_recipes, query=query)



# Страница для отображения деталей рецепта
@rgz.route('/rgz/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipes_list = session.get('recipes', [])
    if recipe_id < len(recipes_list):
        recipe = recipes_list[recipe_id]
        return render_template('rgz/recipe_detail.html', recipe=recipe)
    else:
        return "Рецепт не найден", 404

