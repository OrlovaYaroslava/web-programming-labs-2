from flask import Flask, url_for, redirect, render_template, request
from lab1 import lab1


app = Flask(__name__)
app.register_blueprint(lab1)

# Главная страница по маршрутам / и /index
@app.route("/")
@app.route("/index")
def index():
    css_path = url_for("static", filename="lab1.css")
    return f"""
    <!doctype html>
    <html>
        <head>
            <title>НГТУ, ФБ, Лабораторные работы</title>
            <link rel="stylesheet" type="text/css" href="{css_path}">
        </head>
        <body>
            <header>
                <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
            </header>
            <nav>
                <ul>
                    <li><a href="/lab1">Первая лабораторная</a></li>
                    <li><a href="/lab2">Вторая лабораторная</a></li>
                </ul>
            </nav>
            <footer>
                <p>Студент: Орлова Ярослава Владиславовна</p>
                <p>Группа: ФБИ-22, Курс: 3, 2024</p>
            </footer>
        </body>
    </html>
    """



# Обработчик ошибки 404
@app.errorhandler(404)
def page_not_found(e):
    css_path = url_for("static", filename="lab1.css")
    image_path = url_for("static", filename="404_image.jpg")
    return f"""
    <!doctype html>
    <html>
        <head>
            <link rel="stylesheet" type="text/css" href="{css_path}">
            <title>Страница не найдена</title>
        </head>
        <body>
            <header><h1>404: Страница не найдена</h1></header>
            <p>Извините, но страница, которую вы ищете, не существует.</p>
            <p>Не волнуйтесь, вы всегда можете вернуться на <a href="/lab1/web">главную страницу роутов</a>.</p>
            <img src="{image_path}" alt="404 error image">
        </body>
    </html>
    """, 404

# Искусственная ошибка 404
@app.route("/nonexistent")
def nonexistent():
    return page_not_found(None)


#ЛР2
@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
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

   

@app.route('/lab2/add_flower', methods=['GET'])
def add_flower():
    name = request.args.get('name')
    price = request.args.get('price')

    if not name or not price:
        return "Неверные данные: необходимо указать название цветка и его цену", 400

    # Добавляем новый цветок в список
    flower_list.append({"name": name, "price": int(price)})

    # Перенаправляем на страницу с цветами
    return redirect(url_for('show_flowers'))




@app.route('/lab2/flowers')
def show_flowers():
    lab_num = 2  # Номер лабораторной работы
    return render_template('flowers.html', flower_list=flower_list, lab_num=lab_num)


@app.route('/lab2/del_flower/<int:flower_id>')
def delete_flower(flower_id):
    if 0 <= flower_id < len(flower_list):
        del flower_list[flower_id]
    else:
        return "Такого цветка нет", 404

    # После удаления цветка возвращаемся на страницу со списком цветов
    return redirect(url_for('show_flowers'))


@app.route('/lab2/clear_flowers')
def clear_flowers():
    global flower_list
    flower_list.clear()

    # Возвращаемся на страницу со списком цветов после очистки
    return redirect(url_for('show_flowers'))



#Выражения

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    addition = a + b
    subtraction = a - b
    multiplication = a * b
    division = a / b if b != 0 else "На ноль делить нельзя"
    exponentiation = a ** b
    
    return f"""
        <html>
        <head>
            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='lab1.css')}">
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
@app.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('calc', a=1, b=1))

#Перенаправление с числом a в URL
@app.route('/lab2/calc/<int:a>')
def calc_with_a(a):
    return redirect(url_for('calc', a=a, b=1))




# Обработчик для примера с шаблоном
@app.route('/lab2/example')
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
    return render_template('example.html', 
                           name=name, 
                           lab_num=lab_num, 
                           group=group, 
                           course=course,
                           fruits=fruits)


@app.route('/lab2')
def lab2():
    return render_template('lab2.html')


@app.route('/lab2/filters')
def filters():
    phrase = "О сколько нам открытий чудных..."
    return render_template('filter.html', phrase=phrase)

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

@app.route('/lab2/books')
def show_books():
    return render_template('books.html', books=books)

#Машины
cars = [
    {"name": "Tesla Model S", "description": "Электромобиль от Tesla", "image": "tesla_model_s.jpg"},
    {"name": "BMW i8", "description": "Гибридный спортивный автомобиль", "image": "bmw_i8.jpg"},
    {"name": "Audi R8", "description": "Спортивный автомобиль от Audi", "image": "audi_r8.webp"},
    {"name": "Porsche 911", "description": "Знаменитый спортивный автомобиль", "image": "porsche_911.jpg"},
    {"name": "Lamborghini Aventador", "description": "Высокопроизводительный суперкар", "image": "lamborghini_aventador.jpg"}
]

@app.route('/lab2/cars')
def show_cars():
    return render_template('cars.html', cars=cars)
