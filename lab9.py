from flask import Blueprint, request, jsonify, session, render_template, current_app
from datetime import datetime
import psycopg2
import sqlite3
from os import path

lab9 = Blueprint('lab9', __name__)


@lab9.route('/lab9/')
def main():
    return render_template('lab9/index.html')   