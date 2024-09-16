from flask import Flask, url_for, redirect

app = Flask(__name__)

# Глобальная переменная для счётчика посещений
count = 0

# Главная страница по маршрутам / и /index
@app.route("/")
@app.route("/index")
def index():
    return """
    <!doctype html>
    <html>
        <head>
            <title>НГТУ, ФБ, Лабораторные работы</title>
            <style>
                body {
                    display: flex;
                    flex-direction: column;
                    min-height: 100vh;
                    margin: 0;
                }
                header {
                    background-color: #f8f8f8;
                    padding: 20px;
                    text-align: center;
                }
                footer {
                    background-color: #f8f8f8;
                    padding: 10px;
                    text-align: center;
                    margin-top: auto; /* Это свойство прижимает футер к низу */
                }
                nav {
                    padding: 20px;
                }
                nav ul {
                    list-style-type: none;
                    padding: 0;
                }
                nav ul li {
                    display: inline;
                    margin-right: 10px;
                }
            </style>
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

# Обновлённый маршрут /lab1/web
@app.route("/lab1/web")
def web():
    return """<!doctype html> 
        <html>
           <body> 
               <h1>web-сервер на flask</h1>
               <ul>
                   <li><a href="/lab1/author">Автор</a></li>
                   <li><a href="/lab1/oak">Страница с дубом</a></li>
                   <li><a href="/lab1/counter">Счётчик посещений</a></li>
                   <li><a href="/lab1/info">Перенаправление на автора (Info)</a></li>
                   <li><a href="/lab1/create">Код ответа 201 (Create)</a></li>
                   <li><a href="/lab1/response_headers">HTTP заголовки</a></li>
               </ul>
           </body> 
        </html>"""

# Обновлённый маршрут /lab1/author
@app.route("/lab1/author")
def author():
    name = "Орлова Ярослава Владиславовна"
    group = "ФБИ-22"
    faculty = "ФБ"
    
    return """<!doctype html> 
        <html>
           <body> 
               <p>Судент: """ + name + """</p>
               <p>Группа: """ + group + """</p>
               <p>Факультет: """ + faculty + """</p>
               <a href="/lab1/web">Вернуться на главную</a> 
           </body> 
        </html>"""

# Страница с дубом и подключение CSS
@app.route("/lab1/oak") 
def oak(): 
    image_path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css")
    return ''' 
<!doctype html> 
<html> 
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body> 
        <h1>Дуб</h1> 
        <img src="''' + image_path + '''"> 
        <a href="/lab1/web">Вернуться на главную</a> 
    </body> 
</html>'''    

# Счётчик посещений
@app.route("/lab1/counter")
def counter():
    global count
    count += 1
    return """
    <!doctype html>
    <html>
        <body>
            <h1>Счётчик посещений</h1>
            <p>Эта страница была посещена """ + str(count) + """ раз(а).</p>
            <a href="/lab1/reset_counter">Очистить счётчик</a><br>
            <a href="/lab1/web">Вернуться на главную</a>
        </body>
    </html>
    """

# Очистка счётчика
@app.route("/lab1/reset_counter")
def reset_counter():
    global count
    count = 0  # Сбрасываем счётчик в 0
    return """
    <!doctype html>
    <html>
        <body>
            <h1>Счётчик был очищен!</h1>
            <a href="/lab1/counter">Вернуться на страницу счётчика</a>
        </body>
    </html>
    """

# Обновлённый маршрут /lab1/info
@app.route("/lab1/info")
def info():
    return redirect(url_for('author'))  # Перенаправление на страницу /lab1/author

# Код 201 "Created"
@app.route("/lab1/create")
def create():
    return """
    <!doctype html>
    <html>
        <body>
            <h1>Ресурс был создан!</h1>
            <p>Этот ответ возвращает код 201 (Created).</p>
            <a href="/lab1/web">Вернуться на главную</a>
        </body>
    </html>
    """, 201  # Указываем код ответа 201

# Обработчик ошибки 404
@app.errorhandler(404)
def page_not_found(e):
    return """
    <!doctype html>
    <html>
        <body>
            <h1>404: Страница не найдена</h1>
            <p>К сожалению, страница, которую вы ищете, не существует.</p>
            <a href="/lab1/web">Вернуться на главную</a>
        </body>
    </html>
    """, 404

# Обработчик ошибки 500
@app.errorhandler(500)
def internal_server_error(e):
    return """
    <!doctype html>
    <html>
        <body>
            <h1>500: Внутренняя ошибка сервера</h1>
            <p>Произошла внутренняя ошибка на сервере. Мы уже работаем над её устранением.</p>
            <a href="/lab1/web">Вернуться на главную</a>
        </body>
    </html>
    """, 500

# HTTP заголовки
@app.route("/lab1/response_headers")
def response_headers():
    return """<!doctype html> 
        <html>
           <body> 
               <h1>Заголовки ответа HTTP</h1>
               <a href="/lab1/web">Вернуться на главную</a>
           </body> 
        </html>""", 200, {
        'X-Server': 'sample',
        'Content-Type': 'text/plain; charset=utf-8'
    }

# Новый маршрут /lab1
@app.route("/lab1")
def lab1():
    return """
    <!doctype html>
    <html>
        <head>
            <title>Лабораторная 1</title>
        </head>
        <body>
            <h1>Лабораторная 1</h1>
            <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, 
            а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, 
            сознательно предоставляющих лишь самые базовые возможности.</p>
            <ul><a href="/lab1/web">Задания первой лабораторной</a></ul>
            <a href="/">Вернуться на главную</a>
        </body>
    </html>
    """


# Страница с кодом 400 (Bad Request)
@app.route("/lab1/error400")
def error400():
    return """
    <!doctype html>
    <html>
        <body>
            <h1>400: Bad Request</h1>
            <p>Запрос не может быть выполнен из-за неверного синтаксиса.</p>
            <a href="/lab1/web">Вернуться на главную</a>
        </body>
    </html>
    """, 400

# Страница с кодом 401 (Unauthorized)
@app.route("/lab1/error401")
def error401():
    return """
    <!doctype html>
    <html>
        <body>
            <h1>401: Unauthorized</h1>
            <p>Для доступа к запрашиваемому ресурсу требуется аутентификация.</p>
            <a href="/lab1/web">Вернуться на главную</a>
        </body>
    </html>
    """, 401

# Страница с кодом 402 (Payment Required)
@app.route("/lab1/error402")
def error402():
    return """
    <!doctype html>
    <html>
        <body>
            <h1>402: Payment Required</h1>
            <p>Требуется оплата для доступа к ресурсу.</p>
            <a href="/lab1/web">Вернуться на главную</a>
        </body>
    </html>
    """, 402

# Страница с кодом 403 (Forbidden)
@app.route("/lab1/error403")
def error403():
    return """
    <!doctype html>
    <html>
        <body>
            <h1>403: Forbidden</h1>
            <p>У вас нет прав для доступа к запрашиваемому ресурсу.</p>
            <a href="/lab1/web">Вернуться на главную</a>
        </body>
    </html>
    """, 403

# Страница с кодом 405 (Method Not Allowed)
@app.route("/lab1/error405")
def error405():
    return """
    <!doctype html>
    <html>
        <body>
            <h1>405: Method Not Allowed</h1>
            <p>Метод, используемый в запросе, не поддерживается для запрашиваемого ресурса.</p>
            <a href="/lab1/web">Вернуться на главную</a>
        </body>
    </html>
    """, 405

# Страница с кодом 418 (I'm a teapot)
@app.route("/lab1/error418")
def error418():
    return """
    <!doctype html>
    <html>
        <body>
            <h1>418: I'm a teapot</h1>
            <p>Я - чайник. Я не могу заварить кофе, потому что я чайник.</p>
            <a href="/lab1/web">Вернуться на главную</a>
        </body>
    </html>
    """, 418

