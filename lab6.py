from flask import Blueprint, request, jsonify, session, render_template, current_app
import psycopg2
import sqlite3
from os import path
lab6 = Blueprint('lab6', __name__)

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

# Закрытие соединения с базой
def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')

# Список офисов берется из таблицы
@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    conn, cur = db_connect()
    data = request.json
    request_id = data.get('id', None)

    # Метод "info" для получения списка офисов
    if data.get('method') == 'info':
        cur.execute("SELECT number, tenant, price FROM offices ORDER BY number ASC")
        offices = [{"number": row[0], "tenant": row[1], "price": row[2]} for row in cur.fetchall()]
        db_close(conn, cur)
        return jsonify({
            "jsonrpc": "2.0",
            "result": offices,
            "id": request_id
        })

    # Проверка авторизации
    login = session.get('login')
    if not login:
        db_close(conn, cur)
        return jsonify({
            "jsonrpc": "2.0",
            "error": {"code": 1, "message": "Вы не авторизованы, пожалуйста, войдите в систему"},
            "id": request_id
        })

    # Метод "booking" для бронирования офиса
    if data.get('method') == 'booking':
        office_number = data.get('params')
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT tenant FROM offices WHERE number = %s", (office_number,))
        else:
            cur.execute("SELECT tenant FROM offices WHERE number = ?", (office_number,))
        tenant = cur.fetchone()[0]

        if tenant:
            db_close(conn, cur)
            return jsonify({
                "jsonrpc": "2.0",
                "error": {"code": 2, "message": "Офис уже забронирован"},
                "id": request_id
            })

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE offices SET tenant = %s WHERE number = %s", (login, office_number))
        else:
            cur.execute("UPDATE offices SET tenant = ? WHERE number = ?", (login, office_number))
        db_close(conn, cur)
        return jsonify({
            "jsonrpc": "2.0",
            "result": "success",
            "id": request_id
        })

    # Метод "cancellation" для отмены брони
    if data.get('method') == 'cancellation':
        office_number = data.get('params')
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT tenant FROM offices WHERE number = %s", (office_number,))
        else:
            cur.execute("SELECT tenant FROM offices WHERE number = ?", (office_number,))
        tenant = cur.fetchone()[0]

        if not tenant:
            db_close(conn, cur)
            return jsonify({
                "jsonrpc": "2.0",
                "error": {"code": 2, "message": "Нельзя снять бронь с неарендованного офиса"},
                "id": request_id
            })

        if tenant != login:
            db_close(conn, cur)
            return jsonify({
                "jsonrpc": "2.0",
                "error": {"code": 3, "message": "Вы не можете снять бронь, так как офис арендован другим пользователем"},
                "id": request_id
            })

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE offices SET tenant = NULL WHERE number = %s", (office_number,))
        else:
            cur.execute("UPDATE offices SET tenant = NULL WHERE number = ?", (office_number,))
        db_close(conn, cur)
        return jsonify({
            "jsonrpc": "2.0",
            "result": "success",
            "id": request_id
        })

    # Если метод не найден
    db_close(conn, cur)
    return jsonify({
        "jsonrpc": "2.0",
        "error": {"code": -32601, "message": "Метод не найден"},
        "id": request_id
    })
