from flask import Blueprint, url_for, redirect,render_template, request
lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/a')
def a():
    return 'без слэша'


@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'


#Цветы

flower_list = [
    {"name": "Роза", "price": 300},
    {"name": "Тюльпан", "price": 310},
    {"name": "Ромашка", "price": 320},
    {"name": "Подсолнух", "price": 330},
    {"name": "Лилия", "price": 340}
]
   

@lab2.route('/lab2/add_flower', methods=['GET'])
def add_flower():
    name = request.args.get('name')
    price = request.args.get('price')

    if not name or not price:
        return "Неверные данные: необходимо указать название цветка и его цену", 400

    # Добавляем новый цветок в список
    flower_list.append({"name": name, "price": int(price)})


    # Перенаправляем на страницу с цветами
    return redirect(url_for('lab2.show_flowers'))


@lab2.route('/lab2/flowers')
def show_flowers():
    lab_num = 2  # Номер лабораторной работы
    return render_template('lab2/flowers.html', flower_list=flower_list, lab_num=lab_num)


@lab2.route('/lab2/del_flower/<int:flower_id>')
def delete_flower(flower_id):
    if 0 <= flower_id < len(flower_list):
        del flower_list[flower_id]
    else:
        return "Такого цветка нет", 404

    # После удаления цветка возвращаемся на страницу со списком цветов
    return redirect(url_for('lab2.show_flowers'))


@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    global flower_list
    flower_list.clear()

    # Возвращаемся на страницу со списком цветов после очистки
    return redirect(url_for('lab2.show_flowers'))


#Выражения

@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    addition = a + b
    subtraction = a - b
    multiplication = a * b
    division = a / b if b != 0 else "На ноль делить нельзя"
    exponentiation = a ** b
    
    return f"""
        <html>
        <head>
            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='lab1/lab1.css')}">
        </head>
        <body>
            <h1>Расчёт с параметрами: {a} и {b}</h1>
            <p>{a} + {b} = {addition}</p>
            <p>{a} - {b} = {subtraction}</p>
            <p>{a} * {b} = {multiplication}</p>
            <p>{a} / {b} = {division}</p>
            <p>{a}<sup>{b}</sup> = {exponentiation}</p>
        </body>
        </html>
    """

#Маршрут перенаправления по умолчанию на /lab2/calc/1/1

@lab2.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('lab2.calc', a=1, b=1))


#Перенаправление с числом a в URL

@lab2.route('/lab2/calc/<int:a>')
def calc_with_a(a):
    return redirect(url_for('lab2.calc', a=a, b=1))


# Обработчик для примера с шаблоном

@lab2.route('/lab2/example')
def example():
    name = 'Ярослава Орлова'
    lab_num = 2
    group = 'ФБИ-22'
    course = 3
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('lab2/example.html', 
                           name=name, 
                           lab_num=lab_num, 
                           group=group, 
                           course=course,
                           fruits=fruits)


@lab2.route('/lab2')
def lab2_home():
    return render_template('lab2/lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "О сколько нам открытий чудных..."
    return render_template('lab2/filter.html', phrase=phrase)


# Список книг

books = [
    {"author": "Джордж Оруэлл", "title": "1984", "genre": "Антиутопия", "pages": 328},
    {"author": "Федор Достоевский", "title": "Преступление и наказание", "genre": "Роман", "pages": 671},
    {"author": "Лев Толстой", "title": "Война и мир", "genre": "Эпос", "pages": 1225},
    {"author": "Дж. Р. Р. Толкин", "title": "Властелин колец", "genre": "Фэнтези", "pages": 1137},
    {"author": "Джейн Остин", "title": "Гордость и предубеждение", "genre": "Роман", "pages": 279},
    {"author": "Михаил Булгаков", "title": "Мастер и Маргарита", "genre": "Мистицизм", "pages": 480},
    {"author": "Габриэль Гарсиа Маркес", "title": "Сто лет одиночества", "genre": "Магический реализм", "pages": 417},
    {"author": "Марк Твен", "title": "Приключения Тома Сойера", "genre": "Приключения", "pages": 224},
    {"author": "Джек Лондон", "title": "Зов предков", "genre": "Приключения", "pages": 232},
    {"author": "Харпер Ли", "title": "Убить пересмешника", "genre": "Роман", "pages": 336}
]


@lab2.route('/lab2/books')
def show_books():
    return render_template('lab2/books.html', books=books)


#Машины

cars = [
    {"name": "Tesla Model S", "description": "Электромобиль от Tesla", "image": "lab2/tesla_model_s.jpg"},
    {"name": "BMW i8", "description": "Гибридный спортивный автомобиль", "image": "lab2/bmw_i8.jpg"},
    {"name": "Audi R8", "description": "Спортивный автомобиль от Audi", "image": "lab2/audi_r8.webp"},
    {"name": "Porsche 911", "description": "Знаменитый спортивный автомобиль", "image": "lab2/porsche_911.jpg"},
    {"name": "Lamborghini Aventador", "description": "Высокопроизводительный суперкар", "image": "lab2/lamborghini_aventador.jpg"}
]


@lab2.route('/lab2/cars')
def show_cars():
    return render_template('lab2/cars.html', cars=cars)
