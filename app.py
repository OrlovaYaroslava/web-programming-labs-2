from flask import Flask, url_for, redirect

app = Flask(__name__)

# Глобальная переменная для отслеживания состояния ресурса
resource_created = False
count = 0

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
                </ul>
            </nav>
            <footer>
                <p>Студент: Орлова Ярослава Владиславовна</p>
                <p>Группа: ФБИ-22, Курс: 2, 2024</p>
            </footer>
        </body>
    </html>
    """

# Маршрут /lab1
@app.route("/lab1")
def lab1():
    css_path = url_for("static", filename="lab1.css")
    return f"""
    <!doctype html>
    <html>
        <head>
            <title>Лабораторная 1</title>
            <link rel="stylesheet" type="text/css" href="{css_path}">
        </head>
        <body>
            <header>
                <h1>Лабораторная 1</h1>
            </header>
            <p>Flask — фреймворк для создания веб-приложений на языке программирования Python...</p>
            <nav>
                <ul>
                    <li><a href="/lab1/web">Главная страница лабораторной (/lab1/web)</a></li>
                </ul>
            </nav>
            <footer>
                <p>Студент: Орлова Ярослава Владиславовна</p>
                <p>Группа: ФБИ-22, Курс: 2, 2024</p>
            </footer>
        </body>
    </html>
    """

# Родительская страница /lab1/resource с отображением статуса ресурса и ссылками на создание и удаление
@app.route("/lab1/resource")
def resource_status():
    global resource_created
    css_path = url_for("static", filename="lab1.css")
    status = "Ресурс создан" if resource_created else "Ресурс ещё не создан"
    return f"""
    <!doctype html>
    <html>
        <head>
            <title>Статус ресурса</title>
            <link rel="stylesheet" type="text/css" href="{css_path}">
        </head>
        <body>
            <header><h1>Статус ресурса</h1></header>
            <p>{status}</p>
            <nav>
                <ul>
                    <li><a href="/lab1/create_resource">Создать ресурс</a></li>
                    <li><a href="/lab1/delete_resource">Удалить ресурс</a></li>
                </ul>
            </nav>
            <footer><a href="/lab1/web">Вернуться ко всем роутам</a></footer>
        </body>
    </html>
    """

# Маршрут для создания ресурса
@app.route("/lab1/create_resource")
def create_resource():
    global resource_created
    css_path = url_for("static", filename="lab1.css")
    if resource_created:
        return f"""
        <!doctype html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="{css_path}">
            </head>
            <body>
                <header><h1>Отказано: ресурс уже создан</h1></header>
                <p>Ресурс уже существует, вы не можете создать его снова.</p>
                <footer><a href="/lab1/web">Вернуться ко всем роутам</a></footer>
            </body>
        </html>
        """, 400
    else:
        resource_created = True
        return f"""
        <!doctype html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="{css_path}">
            </head>
            <body>
                <header><h1>Успешно: ресурс создан</h1></header>
                <p>Вы успешно создали ресурс.</p>
                <footer><a href="/lab1/web">Вернуться ко всем роутам</a></footer>
            </body>
        </html>
        """, 201

# Маршрут для удаления ресурса
@app.route("/lab1/delete_resource")
def delete_resource():
    global resource_created
    css_path = url_for("static", filename="lab1.css")
    if resource_created:
        resource_created = False
        return f"""
        <!doctype html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="{css_path}">
            </head>
            <body>
                <header><h1>Ресурс успешно удалён</h1></header>
                <p>Ресурс был удалён.</p>
                <footer><a href="/lab1/web">Вернуться ко всем роутам</a></footer>
            </body>
        </html>
        """, 200
    else:
        return f"""
        <!doctype html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="{css_path}">
            </head>
            <body>
                <header><h1>Отказано: ресурс не существует</h1></header>
                <p>Невозможно удалить ресурс, так как он не был создан.</p>
                <footer><a href="/lab1/web">Вернуться ко всем роутам</a></footer>
            </body>
        </html>
        """, 400


# Маршрут /lab1/web с полным списком всех роутов
@app.route("/lab1/web")
def web():
    css_path = url_for("static", filename="lab1.css")
    return f"""<!doctype html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="{css_path}">
            </head>
           <body>
               <header><h1>WEB-сервер на Flask — все роуты</h1></header>
               <nav>
                   <ul>
                       <li><a href="/lab1/author">Страница автора (/lab1/author)</a></li>
                       <li><a href="/lab1/oak">Страница с дубом (/lab1/oak)</a></li>
                       <li><a href="/lab1/counter">Счётчик посещений (/lab1/counter)</a></li>
                       <li><a href="/lab1/reset_counter">Сброс счётчика (/lab1/reset_counter)</a></li>
                       <li><a href="/lab1/info">Перенаправление на автора (/lab1/info)</a></li>
                       <li><a href="/lab1/create">Код ответа 201 (Created) (/lab1/create)</a></li>
                       <li><a href="/lab1/response_headers">HTTP заголовки (/lab1/response_headers)</a></li>
                       <li><a href="/lab1/error400">Ошибка 400: Bad Request (/lab1/error400)</a></li>
                       <li><a href="/lab1/error401">Ошибка 401: Unauthorized (/lab1/error401)</a></li>
                       <li><a href="/lab1/error402">Ошибка 402: Payment Required (/lab1/error402)</a></li>
                       <li><a href="/lab1/error403">Ошибка 403: Forbidden (/lab1/error403)</a></li>
                       <li><a href="/lab1/error405">Ошибка 405: Method Not Allowed (/lab1/error405)</a></li>
                       <li><a href="/lab1/error418">Ошибка 418: I'm a teapot (/lab1/error418)</a></li>
                       <li><a href="/lab1/error500">Ошибка 500: Internal Server Error (/lab1/error500)</a></li>
                       <li><a href="/lab1/thewitcher">Страница про The Witcher (/lab1/thewitcher)</a></li>
                       <li><a href="/lab1/resource">Статус ресурса (/lab1/resource)</a></li>
                       <li><a href="/lab1/create_resource">Создать ресурс (/lab1/create_resource)</a></li>
                       <li><a href="/lab1/delete_resource">Удалить ресурс (/lab1/delete_resource)</a></li>
                   </ul>
               </nav>
               <footer><a href="/">Вернуться на главную</a></footer>
           </body>
        </html>"""

# Страница автора
@app.route("/lab1/author")
def author():
    css_path = url_for("static", filename="lab1.css")
    name = "Орлова Ярослава Владиславовна"
    group = "ФБИ-22"
    faculty = "ФБ"
    
    return f"""<!doctype html> 
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="{css_path}">
            </head>
           <body> 
               <header><h1>Информация об авторе</h1></header>
               <p>Студент: {name}</p>
               <p>Группа: {group}</p>
               <p>Факультет: {faculty}</p>
               <footer><a href="/lab1/web">Вернуться ко всем роутам</a></footer>
           </body> 
        </html>"""

# Страница с дубом и подключение CSS
@app.route("/lab1/oak") 
def oak(): 
    image_path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css")
    return f''' 
<!doctype html> 
<html> 
    <head>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body> 
        <header><h1>Дуб</h1></header> 
        <img src="{image_path}"> 
        <footer><a href="/lab1/web">Вернуться ко всем роутам</a></footer>
    </body> 
</html>''' 

# Счётчик посещений
@app.route("/lab1/counter")
def counter():
    global count
    css_path = url_for("static", filename="lab1.css")
    count += 1
    return f"""
    <!doctype html>
    <html>
        <head>
            <link rel="stylesheet" type="text/css" href="{css_path}">
        </head>
        <body>
            <header><h1>Счётчик посещений</h1></header>
            <p>Эта страница была посещена {count} раз(а).</p>
            <footer>
                <a href="/lab1/reset_counter">Очистить счётчик</a><br>
                <a href="/lab1/web">Вернуться ко всем роутам</a>
            </footer>
        </body>
    </html>
    """

# Очистка счётчика
@app.route("/lab1/reset_counter")
def reset_counter():
    global count
    css_path = url_for("static", filename="lab1.css")
    count = 0  # Сбрасываем счётчик в 0
    return f"""
    <!doctype html>
    <html>
        <head>
            <link rel="stylesheet" type="text/css" href="{css_path}">
        </head>
        <body>
            <header><h1>Счётчик был очищен!</h1></header>
            <footer>
                <a href="/lab1/counter">Вернуться на страницу счётчика</a><br>
                <a href="/lab1/web">Вернуться ко всем роутам</a>
            </footer>
        </body>
    </html>
    """

# Перенаправление на автора
@app.route("/lab1/info")
def info():
    return redirect(url_for('author'))

# Код 201 "Created"
@app.route("/lab1/create")
def create():
    css_path = url_for("static", filename="lab1.css")
    return f"""
    <!doctype html>
    <html>
        <head>
            <link rel="stylesheet" type="text/css" href="{css_path}">
        </head>
        <body>
            <header><h1>Ресурс был создан!</h1></header>
            <p>Этот ответ возвращает код 201 (Created).</p>
            <footer><a href="/lab1/web">Вернуться ко всем роутам</a></footer>
        </body>
    </html>
    """, 201

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

# HTTP заголовки
@app.route("/lab1/response_headers")
def response_headers():
    css_path = url_for("static", filename="lab1.css")
    return f"""<!doctype html> 
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="{css_path}">
            </head>
           <body> 
               <header><h1>Заголовки ответа HTTP</h1></header>
               <footer><a href="/lab1/web">Вернуться ко всем роутам</a></footer>
           </body> 
        </html>""", 200, {
        'X-Server': 'sample',
        'Content-Type': 'text/plain; charset=utf-8'
    }

# Страница с текстом про The Witcher
@app.route("/lab1/thewitcher")
def thewitcher_page():
    image_path = url_for("static", filename="custom_image.jpg")
    css_path = url_for("static", filename="lab1.css")
    return f"""
    <!doctype html>
    <html>
        <head>
            <link rel="stylesheet" type="text/css" href="{css_path}">
            <title>The Witcher</title>
        </head>
        <body>
            <header><h1>The Witcher</h1></header>
            <p><strong>The Witcher</strong> — это вселенная, созданная польским писателем Анджеем Сапковским, 
            где главный герой, ведьмак Геральт, охотится на чудовищ. Литературные произведения обрели популярность 
            благодаря сложным моральным выборам и насыщенному миру.</p>

            <p>Серия игр, разработанная CD Projekt Red, привнесла «Ведьмака» в массовую культуру. 
            Наибольший успех пришёл с игрой <strong>The Witcher 3: Wild Hunt</strong>, которая стала одной из самых известных игр в мире.</p>

            <p>Сериал от Netflix с Генри Кавиллом в главной роли ещё больше популяризировал франшизу, 
            привлекая внимание новых поклонников и укрепляя позиции «Ведьмака» как важной фэнтези-саги современности.</p>

            <img src="{image_path}" alt="Witcher Image">
            <footer><a href="/lab1/web">Вернуться ко всем роутам</a></footer>
        </body>
    </html>
    """, 200, {
        'Content-Language': 'ru',
        'X-Custom-Header-One': 'Witcher Universe',
        'X-Custom-Header-Two': 'Fantasy Saga'
    }

#ЛР2
@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = ["Роза", "Тюльпан", "Ромашка", "Подсолнух", 
               "Лилия", "Орхидея", "Гладиолус", "Нарцисс", 
               "Гиацинт", "Ирис", "Астра", "Гвоздика", 
               "Лаванда", "Мимоза", "Хризантема", "Фиалка", 
               "Фрезия", "Пион", "Магнолия", "Камелия"]

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return "Такого цветка нет", 404
    else:
        return "Цветок: " + flower_list[flower_id]