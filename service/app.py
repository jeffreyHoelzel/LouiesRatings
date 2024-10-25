from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from database import db, User, ClassData, fetch_grade_distribution_data
import threading
import pandas as pd
import os
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("service")

# turn to true to start filling the database with class information when the server starts
FILL_DB_WITH_CLASS_DATA = False

# only fill if sqlite database does not already exists on start up
if not os.path.isfile('table.db'):
    FILL_DB_WITH_CLASS_DATA = True

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

@app.route('/search', methods=['POST'])
def search():

    # checks if the request is a get type also think Post as a way to send data to the backend to make changes to the data 
    # or just get data from the backend in this case
    if request.method == 'POST':

        # Get the JSON data from the request
        data = request.get_json() 

        # Extract the search query from the JSON data
        search_query = data.get('query')

        # usually a different return here 
        users = [{'id': 1, 'username': 'Alice'}, {'id': 2, 'username': 'Bob'}, {'id': 3, 'username': search_query}]

        # Return the mock users to test and 200 means a successful request
        return jsonify(users), 200
    
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

@app.route('/get_graph_data', methods=["GET", "POST"])
def get_graph_data():
    if request.method == 'POST':
        request_data = request.json  # Get JSON data from the request

        # get specfic class data
        search_by = request_data.get('search_by')

        # get specific data from search name
        grade_data = list()
        if search_by == 'class_name':
            search_name = request_data.get('class_name')
            grade_data = ClassData.query.filter_by(class_name=search_name).all()
        elif search_by == 'instructor_name':
            search_name = request_data.get('instructor_name')
            grade_data = ClassData.query.filter_by(instructor_name=search_name).all()
        if len(grade_data) == 0:
            # nothing found, so return empty data
            return jsonify({"grade": "empty", "sum":0})
        
        # create pandas data frame user the data
        grade_data_df= pd.DataFrame([
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
            } for data in grade_data
        ])

        # make all column names lower case
        grade_data_df.columns = grade_data_df.columns.str.lower()

        # extract only the grade distributions
        grade_distributions = grade_data_df.filter(items=['a', 'b', 'c', 'd', 'f', 'au', 'p', 'ng', 'w', 'i', 'ip', 'pending'])

        # add row for column sums
        grade_distributions.loc["sum"] = grade_distributions.sum(numeric_only=True)

        # remove all rows except for the last two
        grade_distributions = grade_distributions.iloc[[-1]]

        # transpose, and make the index a column for grades
        grade_distributions = grade_distributions.T.reset_index(drop=False).rename(columns={"index":"grade"})
        
        return jsonify(grade_distributions.to_json(orient='records'))

# ====================================

def fill_db_with_class_data():
    logger.info("\nWebscraper running...")
    # only run this to fill database with class data
    with app.app_context():
        fetch_grade_distribution_data(db)
    logger.info("\nWebscraper finished...")

if __name__ == '__main__':
    if FILL_DB_WITH_CLASS_DATA:
        thread = threading.Thread(target=fill_db_with_class_data)
        thread.start()

    app.run(host='0.0.0.0', port=8080)