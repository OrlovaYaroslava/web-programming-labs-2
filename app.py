from flask import Flask, url_for, redirect

app = Flask(__name__)

# Глобальная переменная для счётчика посещений
count = 0

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
