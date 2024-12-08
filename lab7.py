from flask import Blueprint, request, jsonify, session, render_template, current_app
import psycopg2
import sqlite3
from os import path
lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html')

# Список фильмов
films = [
    {
        "title": "Interstellar",
        "title_ru": "Интерстеллар",
        "year": 2014,
        "description": "Когда засуха, пыльные бури и вымирание растений приводят человечество к продовольственному кризису, коллектив исследователей и учёных отправляется сквозь червоточину (которая предположительно соединяет области пространства-времени через большое расстояние) в путешествие, чтобы превзойти прежние ограничения для космических путешествий человека и найти планету с подходящими для человечества условиями."
    },
    {
        "title": "The Shawshank Redemption",
        "title_ru": "Побег из Шоушенка",
        "year": 1994,
        "description": "Бухгалтер Энди Дифрейн обвинён в убийстве собственной жены и её любовника. Оказавшись в тюрьме под названием Шоушенк, он сталкивается с жестокостью и беззаконием, царящими по обе стороны решётки. Каждый, кто попадает в эти стены, становится их рабом до конца жизни. Но Энди, обладающий живым умом и доброй душой, находит подход как к заключённым, так и к охранникам, добиваясь их особого к себе расположения."
    },
    {
        "title": "The Green Mile",
        "title_ru": "Зеленая миля",
        "year": 1999,
        "description": "Пол Эджкомб — начальник блока смертников в тюрьме «Холодная гора». Каждый из узников которого однажды проходит по «зеленой миле» навсегда."
    },
    {
        "title": "Fight Club",
        "title_ru": "Бойцовский клуб",
        "year": 1999,
        "description": "Терзаемый хронической бессонницей и отчаянно пытающийся вырваться из мучительно скучной жизни, клерк встречает некоего Тайлера Дёрдена — харизматического торговца мылом с извращенной философией. Тайлер уверен, что самосовершенствование — удел слабых, а единственное, ради чего стоит жить, — саморазрушение."
    },
    {
        "title": "Inception",
        "title_ru": "Начало",
        "year": 2010,
        "description": "Кобб — талантливый вор, лучший из лучших в опасном искусстве извлечения: он крадет ценные секреты из глубин подсознания во время сна, когда человеческий разум наиболее уязвим. Редкие способности Кобба сделали его ценным игроком в привычном к предательству мире промышленного шпионажа, но они же превратили его в извечного беглеца и лишили всего, что он когда-либо любил."
    }
]

# Маршрут для получения всех фильмов
@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)

# Маршрут для получения информации о конкретном фильме по его ID
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    # Учитываем смещение на 1
    adjusted_id = id - 1
    if 0 <= adjusted_id < len(films):
        return jsonify(films[adjusted_id])
    else:
        return jsonify({"error": "Фильм не найден"}), 404

# Маршрут для удаления фильма по его ID
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def delete_film(id):
    # Учитываем смещение на 1
    adjusted_id = id - 1
    if 0 <= adjusted_id < len(films):
        del films[adjusted_id]
        return '', 204  # Возвращаем пустое тело и код 204 No Content
    else:
        return jsonify({"error": "Фильм не найден"}), 404

# Маршрут для редактирования фильма по его ID
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    adjusted_id = id - 1
    if 0 <= adjusted_id < len(films):
        film = request.get_json()
        # Проверка на пустое оригинальное имя
        if not film.get('title') and film.get('title_ru'):
            film['title'] = film['title_ru']
        if not film.get('description'):
            return jsonify({"description": "Описание не может быть пустым"}), 400
        films[adjusted_id] = film
        return jsonify(films[adjusted_id])
    else:
        return jsonify({"error": "Фильм не найден"}), 404

# Маршрут для добавления нового фильма
@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def post_film():
    film = request.get_json()
    # Проверка на пустое оригинальное имя
    if not film.get('title') and film.get('title_ru'):
        film['title'] = film['title_ru']
    if not film.get('description'):
        return jsonify({"description": "Описание не может быть пустым"}), 400
    films.append(film)
    new_film_id = len(films)
    return jsonify({"id": new_film_id}), 201  # Возвращаем ID нового фильма и код 201 Created
