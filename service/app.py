from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from database import db, User, ClassData, fetch_grade_distribution_data
from generate_graph import make_graph
import threading
import pandas as pd

# turn to true to start filling the database with class information when the server starts
FILL_DB_WITH_CLASS_DATA = False

# For testing only

# ====================================
# Create app
# ====================================
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

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

@app.route('/make_graph', methods=["GET", "POST"])
def profile():
    if request.method == 'POST':
        data = request.json  # Get JSON data from the request

        # get specfic class data
        # todo: add functionality for professor data too
        search_class_name = data.get('class_name')

        # create data frame to generate chart from
        class_data = ClassData.query.filter_by(class_name=search_class_name).all()

        # create pandas data frame user the data
        class_data_df= pd.DataFrame([
            {
                'id': data.id,
                'semester': data.semester,
                'subject': data.subject,
                'class_name': data.class_name,
                'section': data.section,
                'class_nbr': data.class_nbr,
                'instructor_name': data.instructor_name,
                'a': data.a,
                'b': data.b,
                'c': data.c,
                'd': data.d,
                'f': data.f,
                'au': data.au,
                'p': data.p,
                'ng': data.ng,
                'w': data.w,
                'i': data.i,
                'ip': data.ip,
                'pending': data.pending,
                'total': data.total
            } for data in class_data
        ])

        # return chart as json (will need to read from front end using vega-embed)
        return make_graph(class_data_df)

# ====================================

def fill_db_with_class_data():
    # only run this to fill database with class data
    with app.app_context():
        fetch_grade_distribution_data(db)

if __name__ == '__main__':
    if FILL_DB_WITH_CLASS_DATA:
        thread = threading.Thread(target=fill_db_with_class_data)
        thread.start()

    app.run(host='0.0.0.0', port=5000)

                                  
    

