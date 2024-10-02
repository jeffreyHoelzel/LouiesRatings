from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from datetime import datetime

# For accessing webscraping script
import sys
import os
scripts_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'scripts'))
sys.path.append(scripts_path)
from webscraper import get_all_grade_distribution_data 

# For testing only

# ====================================
# Create app
# ====================================
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# maybe change from sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///table.db'
db = SQLAlchemy(app)
# ====================================

# ====================================
# DATABASE MODELS
# ====================================
class User(db.Model):
    # id: Primary key for user
    # username: Used to store the username if the user
    # password: Used to store the password of the user
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.Integer, nullable=False)

    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"username : {self.username}, password : {self.password}"

class ClassData(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    semester = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(5), nullable=False)
    class_name = db.Column(db.String(10), nullable=False)
    section = db.Column(db.String(5), nullable=False)
    class_nbr = db.Column(db.Integer, nullable=False)
    instructor_name = db.Column(db.String(20), nullable=False)
    a = db.Column(db.Integer, nullable=False)
    b = db.Column(db.Integer, nullable=False)
    c = db.Column(db.Integer, nullable=False)
    d = db.Column(db.Integer, nullable=False)
    f = db.Column(db.Integer, nullable=False)
    au = db.Column(db.Integer, nullable=False)
    p = db.Column(db.Integer, nullable=False)
    ng = db.Column(db.Integer, nullable=False)
    w = db.Column(db.Integer, nullable=False)
    i = db.Column(db.Integer, nullable=False)
    ip = db.Column(db.Integer, nullable=False)
    pending = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)

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

# ====================================

# ====================================
# DATABASE FUNCTIONS
# ====================================
def fetch_grade_distribution_data(db: SQLAlchemy):
    grade_distribution_df = get_all_grade_distribution_data()

    data_to_add = []
    
    # create database object for each row
    # note: I want to use .tosql, but it won't work
    for idx, row in grade_distribution_df.iterrows():
        data = ClassData(
            class_nbr = int(row["Class NBR "]),
            semester = row["Semester"],
            subject = row["Subject"],
            class_name = row["Class"],
            section = row["Section"],
            instructor_name = row["Instructor Name"],
            a = int(row["A"]),
            b = int(row["B"]),
            c = int(row["C"]),
            d = int(row["D"]),
            f = int(row["F"]),
            au = int(row["AU"]),
            p = int(row["P"]),
            ng = int(row["NG"]),
            w = int(row["W"]),
            i = int(row["I"]),
            ip = int(row["IP"]),
            pending = int(row["Pending"]),
            total = int(row["Total"])
        )
        data_to_add.append(data)

    # add all data objects to database
    db.session.bulk_save_objects(data_to_add)
    db.session.commit()

# ====================================

if __name__ == '__main__':
    # only run this to fill database with class data
    # fetch_grade_distribution_data(db)
                                  
    app.run(host='0.0.0.0', port=5000)

