from flask import Flask, url_for
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3

app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)

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
                    <li><a href="/lab3">Третья лабораторная</a></li>
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



