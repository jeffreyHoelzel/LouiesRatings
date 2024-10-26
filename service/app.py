from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from database import db, User, ClassData, fetch_grade_distribution_data
import sys
import logging
import threading

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger('service')

# turn to true to start filling the database with class information when the server starts
FILL_DB_WITH_CLASS_DATA = False

# For testing only

# ====================================
# Create app
# ====================================
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# maybe change from sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///table.db'

# bind the database to backend
db.init_app(app)

# create database tables
with app.app_context():
    db.create_all()
# ====================================

# ====================================
# BACKEND FUNCTIONS
# ====================================
@app.route('/', methods=['GET', 'POST'])
def send_message():

    # checks if form is for post request
    if request.method == 'POST':

        # all post functions to the backend will have to do data manipulation 
        # think of POST as a way to send data to the backend to make changes to the data

        # usually a different return here 
        users = [{'id': 1, 'username': 'Alice'}, {'id': 2, 'username': 'Bob'}]
        return jsonify(users), 200

    # we cannot send render templates as we are not using flask python templates on the frontend
    return jsonify(message="Hello From Backend"), 200

@app.route('/add_user', methods=["GET", "POST"])
def profile():
    if request.method == 'POST':
        data = request.json  # Get JSON data from the request

        # get username and password
        username = data.get('username')
        password = data.get('password')

        # create an object of the User class of models
        # and store data as a row in our datatable
        if username != '' and password != '':
            p = User(username=username, password=password)
            db.session.add(p)
            db.session.commit()

        return jsonify({'message': 'Data received!', 'data': {'name': username}}), 200
    
@app.route('/login', methods=['POST'])
def login():


# ===============TESTING ONLY=====================

    # add a mock user to db
    mock_user = User(username='jeffhoelzel', password='jeff123')

    # save object to db
    db.session.add(mock_user)
    db.session.commit()

# ===============TESTING ONLY=====================


    if request.method == 'POST':
        # get JSON data from user
        data = request.json
        requested_username = data.get('username')
        requested_password = data.get('password')

        logger.info('\nreq user: %s', requested_username)
        logger.info('\nreq pass: %s', requested_password)

        # get username and password from database, if user DNE, user will be None
        user = db.session.query(User).filter_by(username=requested_username, password=requested_password).first();

        # check if user DNE
        if user is None:
            logger.info('\nThe username or password doesn\'t match our records. Please try again')
            return jsonify({'message': 'The username or password doesn\'t match our records. Please try again.', 'exists': False}), 401
        else:
            logger.info('\nUser logged in successfully.')
            return jsonify({'message': 'User logged in successfully.', "exists": True}), 200

# ====================================

def fill_db_with_class_data():
    # only run this to fill database with class data
    with app.app_context():
        fetch_grade_distribution_data(db)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)