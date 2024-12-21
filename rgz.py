from flask import Blueprint, request, jsonify, session, render_template, current_app,redirect,flash
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
        
        # Добавление рецепта в сессию (или в базу данных)
        new_recipe = {
            'name': name,
            'description': description,
            'ingredients': ingredients,
            'steps': steps,
            'photo_url': photo_url
        }

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


@rgz.route('/rgz/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()  # Удаляем лишние пробелы из названия
    ingredient_query = request.args.get('ingredient_query', '').strip()  # Удаляем лишние пробелы из ингредиентов
    search_mode = request.args.get('search_mode', 'all')  # 'all' или 'any' для ингредиентов

    recipes_list = session.get('recipes', [])  # Получаем список рецептов из сессии

    # Фильтрация по названию рецепта
    if query:
        query = query.lower()  # Приводим к нижнему регистру для поиска
        filtered_recipes = [r for r in recipes_list if query in r['name'].lower()]
    else:
        filtered_recipes = recipes_list  # Если название не введено, используем все рецепты

    # Если есть запрос по ингредиентам
    if ingredient_query:
        # Преобразуем ингредиенты в список, очищаем и приводим к нижнему регистру
        ingredients = [ingredient.strip().lower() for ingredient in ingredient_query.split(',') if ingredient.strip()]
        final_recipes = []

        for recipe in filtered_recipes:
            # Преобразуем ингредиенты рецепта в список, очищаем и приводим к нижнему регистру
            recipe_ingredients = [ingredient.strip().lower() for ingredient in recipe['ingredients'].split(',')]

            # Проверяем режим поиска: все ингредиенты или хотя бы один
            if search_mode == 'all':
                if all(
                    any(
                        ingredient in recipe_ingredient
                        or recipe_ingredient in ingredient
                        for recipe_ingredient in recipe_ingredients
                    )
                    for ingredient in ingredients
                ):
                    final_recipes.append(recipe)
            elif search_mode == 'any':
                if any(
                    any(
                        ingredient in recipe_ingredient
                        or recipe_ingredient in ingredient
                        for recipe_ingredient in recipe_ingredients
                    )
                    for ingredient in ingredients
                ):
                    final_recipes.append(recipe)
    else:
        # Если ингредиенты не введены, используем только фильтрацию по названию
        final_recipes = filtered_recipes

    # Отправляем результаты поиска в шаблон
    return render_template(
        'rgz/search.html',
        recipes=final_recipes,
        query=query,
        ingredient_query=ingredient_query,
        search_mode=search_mode,
    )




# Страница для отображения деталей рецепта
@rgz.route('/rgz/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipes_list = session.get('recipes', [])
    if recipe_id < len(recipes_list):
        recipe = recipes_list[recipe_id]
        return render_template('rgz/recipe_detail.html', recipe=recipe)
    else:
        return "Рецепт не найден", 404

@rgz.route('/rgz/delete_recipe/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    # Проверка, что пользователь является администратором
    if 'role' not in session or session['role'] != 'admin':
        flash('У вас нет прав для удаления рецептов')
        return redirect('/rgz/')

    # Получаем список рецептов из сессии
    recipes_list = session.get('recipes', [])
    
    # Проверяем, что индекс рецепта существует в списке
    if recipe_id < len(recipes_list):
        # Удаляем рецепт по индексу
        del recipes_list[recipe_id]
        session['recipes'] = recipes_list  # Обновляем сессию
        session.modified = True
        flash('Рецепт успешно удален!')
    else:
        flash('Рецепт не найден!')

    return redirect('/rgz/recipes')  # Перенаправляем на страницу со списком рецептов
