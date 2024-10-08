from flask import Blueprint, url_for, redirect,render_template, request
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab3_page():
    return render_template('lab3/lab3.html')