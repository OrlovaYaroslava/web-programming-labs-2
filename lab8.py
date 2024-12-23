from flask import Blueprint, request, jsonify, session, render_template, current_app
from datetime import datetime
import psycopg2
import sqlite3
from os import path

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8')
def lab8_home():
    user_name = session.get('login', 'Anonymous')
    return render_template('lab8/lab8.html', user_name=user_name)