from flask import Blueprint, request, render_template, redirect, url_for, session

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/', methods=['GET', 'POST'])
def index():
    # Проверяем, есть ли данные в сессии
    if 'name' in session and 'age' in session and 'gender' in session:
        # Если данные есть, сразу отображаем последнее поздравление
        return redirect(url_for('lab9.greeting'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            error = "Введите имя!"
            return render_template('lab9/index.html', error=error)
        session['name'] = name  # Сохраняем имя в сессию
        return redirect(url_for('lab9.age'))
    
    # Если метод GET или данных в сессии нет
    return render_template('lab9/index.html')


@lab9.route('/lab9/get_name', methods=['GET'])
def get_name():
    session.clear()  # Очищаем данные при сбросе
    return render_template('lab9/get_name.html')

@lab9.route('/lab9/age', methods=['GET', 'POST'])
def age():
    if request.method == 'POST':
        age = request.form.get('age')
        if not age or not age.isdigit():
            error = "Введите корректный возраст!"
            return render_template('lab9/age.html', error=error)
        session['age'] = int(age)  # Сохраняем возраст в сессию
        return redirect(url_for('lab9.gender'))
    return render_template('lab9/age.html')

@lab9.route('/lab9/gender', methods=['GET', 'POST'])
def gender():
    if request.method == 'POST':
        gender = request.form.get('gender')
        if not gender:
            error = "Выберите пол!"
            return render_template('lab9/gender.html', error=error)
        session['gender'] = gender  # Сохраняем пол в сессию
        return redirect(url_for('lab9.preference1'))
    return render_template('lab9/gender.html')

@lab9.route('/lab9/preference1', methods=['GET', 'POST'])
def preference1():
    if request.method == 'POST':
        preference1 = request.form.get('preference1')
        if not preference1:
            error = "Выберите предпочтение!"
            return render_template('lab9/preference1.html', error=error)
        session['preference1'] = preference1  # Сохраняем предпочтение в сессию
        return redirect(url_for('lab9.preference2'))
    return render_template('lab9/preference1.html')

@lab9.route('/lab9/preference2', methods=['GET', 'POST'])
def preference2():
    if request.method == 'POST':
        preference2 = request.form.get('preference2')
        if not preference2:
            error = "Выберите предпочтение!"
            return render_template('lab9/preference2.html', error=error)
        session['preference2'] = preference2  # Сохраняем предпочтение в сессию
        return redirect(url_for('lab9.greeting'))
    return render_template('lab9/preference2.html')

@lab9.route('/lab9/greeting', methods=['GET'])
def greeting():
    # Получаем данные из сессии
    name = session.get('name', 'Гость')
    age = session.get('age', 0)
    gender = session.get('gender', 'unknown')
    preference1 = session.get('preference1', 'unknown')
    preference2 = session.get('preference2', 'unknown')

    # Выбор картинки
    if gender == 'male':
        if preference1 == 'sweet':
            image = 'lab9/sweet_male.jpg'
        else:
            image = 'lab9/beautiful_male.jpg'
    else:
        if preference1 == 'sweet':
            image = 'lab9/sweet_female.jpg'
        else:
            image = 'lab9/beautiful_female.jpg'

    return render_template(
        'lab9/greeting.html',
        name=name, age=age, gender=gender, preference1=preference1,
        preference2=preference2, image=image
    )
