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
                    margin-top: auto;
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

# Маршрут /lab1
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
         

            <h2>Список роутов</h2>
            <ul>
                <li><a href="/lab1/web">Главная страница лабораторной (/lab1/web)</a></li>

            </ul>

            <a href="/">Вернуться на главную</a>
        </body>
    </html>
    """

# Маршрут /lab1/web с полным списком всех роутов
@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>WEB-сервер на Flask — все роуты</h1>
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
                   <li><a href="/nonexistent">Искусственная ошибка 404 (/nonexistent)</a></li>
               </ul>
               <a href="/">Вернуться на главную</a>
           </body>
        </html>"""

# Страница автора
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
               <a href="/lab1/web">Вернуться ко всем роутам</a>
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
        <a href="/lab1/web">Вернуться ко всем роутам</a>
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
            <a href="/lab1/web">Вернуться ко всем роутам</a>
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
            <a href="/lab1/counter">Вернуться на страницу счётчика</a><br>
            <a href="/lab1/web">Вернуться ко всем роутам</a>
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
    return """
    <!doctype html>
    <html>
        <body>
            <h1>Ресурс был создан!</h1>
            <p>Этот ответ возвращает код 201 (Created).</p>
            <a href="/lab1/web">Вернуться ко всем роутам</a>
        </body>
    </html>
    """, 201

# Обработчик ошибки 404 с добавленными стилями и изображением
@app.errorhandler(404)
def page_not_found(e):
    image_path = url_for("static", filename="404_image.jpg")
    return """
    <!doctype html>
    <html>
        <head>
            <title>Страница не найдена</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    color: #333;
                    background-color: #f4f4f9;
                    margin: 0;
                    padding: 0;
                }
                h1 {
                    font-size: 48px;
                    color: #e74c3c;
                    margin-top: 50px;
                }
                p {
                    font-size: 18px;
                    color: #555;
                }
                img {
                    width: 50%;
                    margin-top: 20px;
                }
                a {
                    display: inline-block;
                    margin-top: 20px;
                    padding: 10px 20px;
                    color: white;
                    background-color: #3498db;
                    text-decoration: none;
                    border-radius: 5px;
                    font-size: 18px;
                }
                a:hover {
                    background-color: #2980b9;
                }
            </style>
        </head>
        <body>
            <h1>404: Страница не найдена</h1>
            <p>Извините, но страница, которую вы ищете, не существует.</p>
            <p>Не волнуйтесь, вы всегда можете вернуться на <a href="/lab1/web">главную страницу роутов</a>.</p>
            <img src='""" + image_path + """' alt="404 error image">
        </body>
    </html>
    """, 404

# Искусственная ошибка 404
@app.route("/nonexistent")
def nonexistent():
    # Специальный маршрут, который вызывает ошибку 404
    return page_not_found(None)

# Перехватчик для ошибки 500
@app.errorhandler(500)
def internal_server_error(e):
    return """
    <!doctype html>
    <html>
        <head>
            <title>Ошибка 500: Внутренняя ошибка сервера</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    color: #333;
                    background-color: #f4f4f9;
                    margin: 0;
                    padding: 0;
                }
                h1 {
                    font-size: 48px;
                    color: #e74c3c;
                    margin-top: 50px;
                }
                p {
                    font-size: 18px;
                    color: #555;
                }
                a {
                    display: inline-block;
                    margin-top: 20px;
                    padding: 10px 20px;
                    color: white;
                    background-color: #3498db;
                    text-decoration: none;
                    border-radius: 5px;
                    font-size: 18px;
                }
                a:hover {
                    background-color: #2980b9;
                }
            </style>
        </head>
        <body>
            <h1>500: Внутренняя ошибка сервера</h1>
            <p>Произошла внутренняя ошибка на сервере. Мы уже работаем над её устранением.</p>
            <p>Пожалуйста, попробуйте зайти позже или вернитесь на <a href="/lab1/web">главную страницу роутов</a>.</p>
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
               <a href="/lab1/web">Вернуться ко всем роутам</a>
           </body> 
        </html>""", 200, {
        'X-Server': 'sample',
        'Content-Type': 'text/plain; charset=utf-8'
    }

# Страница с кодом 400 (Bad Request)
@app.route("/lab1/error400")
def error400():
    return """
    <!doctype html>
    <html>
        <body>
            <h1>400: Bad Request</h1>
            <p>Запрос не может быть выполнен из-за неверного синтаксиса.</p>
            <a href="/lab1/web">Вернуться ко всем роутам</a>
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
            <a href="/lab1/web">Вернуться ко всем роутам</a>
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
            <a href="/lab1/web">Вернуться ко всем роутам</a>
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
            <a href="/lab1/web">Вернуться ко всем роутам</a>
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
            <a href="/lab1/web">Вернуться ко всем роутам</a>
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
            <a href="/lab1/web">Вернуться ко всем роутам</a>
        </body>
    </html>
    """, 418

# Страница с текстом про The Witcher
@app.route("/lab1/thewitcher")
def thewitcher_page():
    image_path = url_for("static", filename="custom_image.jpg")
    return """
    <!doctype html>
    <html>
        <head>
            <title>The Witcher</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    color: #333;
                    background-color: #f9f9f9;
                    margin: 0;
                    padding: 0;
                }
                h1 {
                    text-align: center;
                    color: #2c3e50;
                    margin-top: 30px;
                }
                p {
                    margin: 20px;
                    font-size: 18px;
                    line-height: 1.6;
                }
                footer {
                    text-align: center;
                    padding: 10px;
                    background-color: #f8f8f8;
                    position: auto;
                    width: 100%;
                    bottom: 0;
                }
               
                 img {
                    display: block;
                    margin: 20px auto;
                    width: 50%;
                }
            </style>
        </head>
        <body>
            <h1>The Witcher</h1>
            <p><strong>The Witcher</strong> — это вселенная, созданная польским писателем Анджеем Сапковским, 
            где главный герой, ведьмак Геральт, охотится на чудовищ. Литературные произведения обрели популярность 
            благодаря сложным моральным выборам и насыщенному миру.</p>

            <p>Серия игр, разработанная CD Projekt Red, привнесла «Ведьмака» в массовую культуру. 
            Наибольший успех пришёл с игрой <strong>The Witcher 3: Wild Hunt</strong>, которая стала одной из самых известных игр в мире.</p>

            <p>Сериал от Netflix с Генри Кавиллом в главной роли ещё больше популяризировал франшизу, 
            привлекая внимание новых поклонников и укрепляя позиции «Ведьмака» как важной фэнтези-саги современности.</p>
            
            <img src='""" + image_path + """' alt="Witcher Image">

            <footer>
                <p>Спасибо за внимание!</p>
            </footer>
        </body>
    </html>
    """, 200, {
        'Content-Language': 'ru',
        'X-Custom-Header-One': 'Witcher Universe',
        'X-Custom-Header-Two': 'Fantasy Saga'
    }
