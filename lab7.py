from flask import Blueprint, request, jsonify, session, render_template, current_app
import psycopg2
import sqlite3
from os import path
lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab6/lab7.html')