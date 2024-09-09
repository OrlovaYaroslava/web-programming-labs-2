from flask import Flask, url_for, redirect

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
    return redirect('/author')  # Перенаправление на страницу "author"

