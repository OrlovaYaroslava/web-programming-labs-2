from flask import Blueprint, request, jsonify, session, render_template

lab6 = Blueprint('lab6', __name__)

# Список офисов с добавлением стоимости аренды
offices = [{"number": i, "tenant": "", "price": 900 + i * 3} for i in range(1, 11)]

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    request_id = data.get('id', None)
    
    # Метод "info" для получения списка офисов
    if data.get('method') == 'info':
        return jsonify({
            "jsonrpc": "2.0",
            "result": offices,
            "id": request_id
        })

    # Проверка авторизации
    login = session.get('login')
    if not login:
        return jsonify({
            "jsonrpc": "2.0",
            "error": {"code": 1, "message": "Вы не авторизованы, пожалуйста, войдите в систему"},
            "id": request_id
        })

    # Метод "booking" для бронирования офиса
    if data.get('method') == 'booking':
        office_number = data.get('params')
        for office in offices:
            if office['number'] == office_number:
                if office['tenant']:
                    return jsonify({
                        "jsonrpc": "2.0",
                        "error": {"code": 2, "message": "Офис уже забронирован"},
                        "id": request_id
                    })
                office['tenant'] = login
                return jsonify({
                    "jsonrpc": "2.0",
                    "result": "success",
                    "id": request_id
                })

    # Метод "cancellation" для отмены брони
    if data.get('method') == 'cancellation':
        office_number = data.get('params')
        for office in offices:
            if office['number'] == office_number:
                if not office['tenant']:
                    return jsonify({
                        "jsonrpc": "2.0",
                        "error": {"code": 2, "message": "Нельзя снять бронь с неарендованного офиса"},
                        "id": request_id
                    })
                if office['tenant'] != login:
                    return jsonify({
                        "jsonrpc": "2.0",
                        "error": {"code": 3, "message": "Вы не можете снять бронь, так как офис арендован другим пользователем"},
                        "id": request_id
                    })
                office['tenant'] = ""
                return jsonify({
                    "jsonrpc": "2.0",
                    "result": "success",
                    "id": request_id
                })

    # Если метод не найден
    return jsonify({
        "jsonrpc": "2.0",
        "error": {"code": -32601, "message": "Метод не найден"},
        "id": request_id
    })
