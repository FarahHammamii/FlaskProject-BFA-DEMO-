from flask import Flask, url_for
import os

from flaskext.mysql import MySQL
from flask_login import LoginManager

x = MySQL()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'abcdef'
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = ''
    app.config['MYSQL_DATABASE_DB'] = 'bfa'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


   
    x.init_app(app)

    try:
        with app.app_context():
            # Obtain a database connection
            db = x.connect()
            cursor = db.cursor()

            # Example: Execute a query to check MySQL server version
            cursor.execute('SELECT VERSION()')
            db_version = cursor.fetchone()
            print(f"Connected to MySQL Server version: {db_version[0]}")



    except Exception as e:
        print(f"Error while connecting to MySQL database: {e}")


    from .views import views

    app.register_blueprint(views, url_prefix='/')


    return app
