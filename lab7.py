from flask import Blueprint, request, jsonify, session, render_template, current_app
from datetime import datetime
import psycopg2
import sqlite3
from os import path

lab7 = Blueprint('lab7', __name__)

# Функция подключения к базе данных
def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='yaroslava_orlova_knowledge_base',
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

@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html')

# Закрытие соединения с базой
def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

# Валидация данных фильма
def validate_film(film):
    current_year = datetime.now().year

    # Проверка названий
    if not film.get('title') and not film.get('title_ru'):
        return "Либо оригинальное, либо русское название должно быть указано."

    # Если оригинальное название пустое, но русское задано, используем русское
    if not film.get('title') and film.get('title_ru'):
        film['title'] = film['title_ru']

    # Проверка года
    if not (1895 <= film.get('year', 0) <= current_year):
        return f"Год должен быть в диапазоне от 1895 до {current_year}."

    # Проверка описания
    if not film.get('description'):
        return "Описание не может быть пустым."
    if len(film.get('description', '')) > 2000:
        return "Описание не может быть длиннее 2000 символов."

    return None  # Если ошибок нет

# Маршрут для получения всех фильмов
@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM films;")
    else:
        cur.execute("SELECT * FROM films")
    films = cur.fetchall()
    db_close(conn, cur)
    
    films_list = []
    for film in films:
        films_list.append({
            "id": film[0],
            "title": film[1],
            "title_ru": film[2],
            "year": film[3],
            "description": film[4]
        })
    return jsonify(films_list)

# Маршрут для получения информации о конкретном фильме по его ID
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM films WHERE id = %s;", (id,))
    else:
        cur.execute("SELECT * FROM films WHERE id = ?", (id,))
    film = cur.fetchone()
    db_close(conn, cur)
    
    if film:
        return jsonify({
            "id": film[0],
            "title": film[1],
            "title_ru": film[2],
            "year": film[3],
            "description": film[4]
        })
    else:
        return jsonify({"error": "Фильм не найден"}), 404

# Маршрут для удаления фильма по его ID
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def delete_film(id):
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM films WHERE id = %s;", (id,))
    else:
        cur.execute("SELECT * FROM films WHERE id = ?", (id,))
    film = cur.fetchone()
    
    if film:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM films WHERE id = %s;", (id,))
        else:
            cur.execute("DELETE FROM films WHERE id = ?", (id,))
        db_close(conn, cur)
        return '', 204  # Возвращаем пустое тело и код 204 No Content
    else:
        db_close(conn, cur)
        return jsonify({"error": "Фильм не найден"}), 404

# Маршрут для редактирования фильма по его ID
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    updated_film = request.get_json()
    error = validate_film(updated_film)
    
    if error:
        return jsonify({"error": error}), 400

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM films WHERE id = %s;", (id,))
    else:
        cur.execute("SELECT * FROM films WHERE id = ?", (id,))
    film = cur.fetchone()

    if film:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                UPDATE films 
                SET title = %s, title_ru = %s, year = %s, description = %s
                WHERE id = %s;
            """, (updated_film['title'], updated_film['title_ru'], updated_film['year'], updated_film['description'], id))
        else:
            cur.execute("""
                UPDATE films 
                SET title = ?, title_ru = ?, year = ?, description = ?
                WHERE id = ?;
            """, (updated_film['title'], updated_film['title_ru'], updated_film['year'], updated_film['description'], id))
        db_close(conn, cur)
        return jsonify({
            "id": id,
            "title": updated_film['title'],
            "title_ru": updated_film['title_ru'],
            "year": updated_film['year'],
            "description": updated_film['description']
        })
    else:
        db_close(conn, cur)
        return jsonify({"error": "Фильм не найден"}), 404

# Маршрут для добавления нового фильма
@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def post_film():
    new_film = request.get_json()
    error = validate_film(new_film)
    
    if error:
        return jsonify({"error": error}), 400
    
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            INSERT INTO films (title, title_ru, year, description)
            VALUES (%s, %s, %s, %s) RETURNING id;
        """, (new_film['title'], new_film['title_ru'], new_film['year'], new_film['description']))
        new_id = cur.fetchone()[0]
    else:
        cur.execute("""
            INSERT INTO films (title, title_ru, year, description)
            VALUES (?, ?, ?, ?) 
        """, (new_film['title'], new_film['title_ru'], new_film['year'], new_film['description']))
        new_id = cur.lastrowid
    
    db_close(conn, cur)
    
    return jsonify({"id": new_id}), 201  # Возвращаем ID нового фильма и код 201 Created
