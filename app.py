from flask import Flask, url_for, redirect, make_response

app = Flask(__name__)

# Глобальная переменная для счётчика посещений
count = 0

@app.route("/web")
def web():
    return """<!doctype html> 
        <html>
           <body> 
               <h1>web-сервер на flask</h1>
               <ul>
                   <li><a href="/author">Автор</a></li>
                   <li><a href="/lab1/oak">Страница с дубом</a></li>
                   <li><a href="/lab1/counter">Счётчик посещений</a></li>
                   <li><a href="/info">Перенаправление на автора (Info)</a></li>
                   <li><a href="/create">Код ответа 201 (Create)</a></li>
                   <li><a href="/response_headers">HTTP заголовки</a></li>
               </ul>
           </body> 
        </html>"""

@app.route("/author")
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
               <a href="/web">Вернуться на главную</a> 
           </body> 
        </html>"""

@app.route("/lab1/oak") 
def oak(): 
    path = url_for("static", filename="oak.jpg") 
    return ''' 
<!doctype html> 
<html> 
    <body> 
        <h1>Дуб</h1> 
        <img src="''' + path + '''"> 
        <a href="/web">Вернуться на главную</a> 
    </body> 
</html>'''    

# Роут для счётчика
@app.route("/lab1/counter")
def counter():
    global count  # Указание, что переменная глобальная
    count += 1
    return """
    <!doctype html>
    <html>
        <body>
            <h1>Счётчик посещений</h1>
            <p>Эта страница была посещена """ + str(count) + """ раз(а).</p>
            <a href="/web">Вернуться на главную</a>
        </body>
    </html>
    """

# Роут для перенаправления
@app.route("/info")
def info():
    return redirect(url_for('author'))  # Перенаправление на страницу "author"

# Роут, который возвращает код 201 "Created"
@app.route("/create")
def create():
    return """
    <!doctype html>
    <html>
        <body>
            <h1>Ресурс был создан!</h1>
            <p>Этот ответ возвращает код 201 (Created).</p>
            <a href="/web">Вернуться на главную</a>
        </body>
    </html>
    """, 201  # Указываем код ответа 201

# Обработчик ошибки 404 (страница не найдена)
@app.errorhandler(404)
def page_not_found(e):
    return """
    <!doctype html>
    <html>
        <body>
            <h1>404: Страница не найдена</h1>
            <p>К сожалению, страница, которую вы ищете, не существует.</p>
            <a href="/web">Вернуться на главную</a>
        </body>
    </html>
    """, 404

# Обработчик ошибки 500 (внутренняя ошибка сервера)
@app.errorhandler(500)
def internal_server_error(e):
    return """
    <!doctype html>
    <html>
        <body>
            <h1>500: Внутренняя ошибка сервера</h1>
            <p>Произошла внутренняя ошибка на сервере. Мы уже работаем над её устранением.</p>
            <a href="/web">Вернуться на главную</a>
        </body>
    </html>
    """, 500

# Роут для демонстрации HTTP заголовков
@app.route("/response_headers")
def response_headers():
    return """<!doctype html> 
        <html>
           <body> 
               <h1>Заголовки ответа HTTP</h1>
               <a href="/web">Вернуться на главную</a>
           </body> 
        </html>""", 200, {
        'X-Server': 'sample',
        'Content-Type': 'text/plain; charset=utf-8'
    }


