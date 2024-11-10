from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from database import db, User, ClassData, fetch_grade_distribution_data, Comment, InstructorRating
from database import add_comment, fetch_comment, delete_comment, search_instructors, add_rating
import threading
import pandas as pd
import bcrypt as bc
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

        instructors = search_instructors(search_query)
        
        # Return the mock users to test and 200 means a successful request
        return jsonify(instructors), 200
    
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        # get JSON data from new user
        data = request.json

        # get username, password, email, first name, and last name
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        first_name = data.get('firstName')
        last_name = data.get('lastName')

        # convert password to byte string
        byte_password = password.encode('utf-8')
        # generate salt
        salt = bc.gensalt()
        # get hashed password with salt
        hashed_password = bc.hashpw(byte_password, salt)

        # if all credentials are not empty strings, create a new user object, otherwise, throw error
        if all([username, password, email, first_name, last_name]):
            new_user = User(username=username, password=hashed_password, email=email, first_name=first_name, last_name=last_name)
        else:
            logger.info('\nServer was provided with incomplete information.')
            return jsonify({'message': 'Server was provided with incomplete information.', 'error': True}), 422

        # search for username and email in database
        user_db = db.session.query(User).filter_by(username=username, email=email).first()

        # if either are in use, send 403 response (already exists)
        if user_db is not None:
            logger.info('\nUsername or email already in use.')
            return jsonify({'message': 'Username or email already in use.', 'error': True}), 403
        
        # otherwise, add user to database
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as database_error:
            # Roll back the session in case of error
            db.session.rollback()

        # return success message and 200 response (ok)
        logger.info('\nNew user successfully added.')
        return jsonify({'message': 'New user successfully added.', 'error': False}), 200
    
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        # get JSON data from user
        data = request.json
        requested_username = data.get('username')
        requested_password = data.get('password')

        # get user from database using username
        user = db.session.query(User).filter_by(username=requested_username).first()
        db_password = user.password

        # check if user exists if a valid password is present
        if user is not None and db_password:
            # verify password
            if bc.checkpw(requested_password.encode('utf-8'), db_password):
                logger.info('\nPasswords match. User logged in successfully.')
                return jsonify({'message': 'User logged in successfully.', 'exists': True}), 200
            else:
                logger.info('\nIncorrect password.')
                return jsonify({'message': 'Incorrect password. Please try again.', 'exists': False}), 401
        else:
            logger.info('\nThe user specified does not exist.')
            return jsonify({'message': 'The user specified does not exist. Please try again.', 'exists': False}), 401
    
@app.route('/professor', methods=['GET'])
def get_professor_data():
    instructor_name = request.args.get('name')
    # Testing
    # app.logger.debug(f"Received request for instructor: {instructor_name}")

    if instructor_name:
        # Split the instructor name into last name and first name and search database for any matching names
        last_name, first_name = instructor_name.split(", ")
        courses = ClassData.query.filter(
            ClassData.instructor_name.ilike(f"%{last_name}%"),
            ClassData.instructor_name.ilike(f"%{first_name}%")
        ).all()
    else:
        return jsonify({"error": "Professor not found"}), 404

    # Extract full instructor name from the first matched course, add space following comma
    full_instructor_name = courses[0].instructor_name
    
    course_data = [
        {
            "semester": course.semester,
            "subject": course.subject,
            "class_name": course.class_name,
            "section": course.section,
            "grades": {
                "A": course.a,
                "B": course.b,
                "C": course.c,
                "D": course.d,
                "F": course.f,
                "P": course.p,
                "W": course.w
            },
        }
        for course in courses
    ]

    # Include the full instructor name in the response
    return jsonify({"professor": full_instructor_name, "courses": course_data})

@app.route('/class', methods=['GET'])
def get_class_data():
    class_id = request.args.get('classId') 
    if not class_id:
        return jsonify({"error": "Class ID is required"}), 400

    # Fetch class data from the database
    class_data = ClassData.query.filter_by(class_name=class_id).first()

    if class_data:
        return jsonify({"class": {
            "title": f"{class_data.subject} {class_data.class_name}",
            "code": class_data.class_name,
            "instructor": class_data.instructor_name,
            "grades": {
                "A": class_data.a,
                "B": class_data.b,
                "C": class_data.c,
                "D": class_data.d,
                "F": class_data.f,
                "P": class_data.p,
                "W": class_data.w
            },
        }}), 200
    else:
        return jsonify({"error": "Class not found"}), 404

@app.route('/get_graph_data', methods=["GET", "POST"])
def get_graph_data():
    if request.method == 'POST':
        request_data = request.json  # Get JSON data from the request

        # get specfic class data
        search_by = request_data.get('search_by')

        # get specific data from search name
        grade_data = list()

        search_name = request_data.get(search_by)

        if search_by == 'class_name':
            grade_data = ClassData.query.filter_by(class_name=search_name).all()

        else:
            grade_data = ClassData.query.filter_by(instructor_name=search_name).all()

        if len(grade_data) == 0:
            # nothing found, so return empty data
            return jsonify({"grade": "empty", "sum":0}), 404
        
        # create pandas data frame user the data, only get relevant information
        grade_distributions= pd.DataFrame([
            {
                'A': data.a,
                'B': data.b,
                'C': data.c,
                'D': data.d,
                'F': data.f,
                'P': data.p,
                'W': data.w
            } for data in grade_data
        ])

        # add row for column sums
        grade_distributions.loc["sum"] = grade_distributions.sum(numeric_only=True)

        # remove all rows except for the last two
        grade_distributions = grade_distributions.iloc[[-1]]

        # transpose, and make the index a column for grades
        grade_distributions = grade_distributions.T.reset_index(drop=False).rename(columns={"index":"grade"})
        
        return jsonify(grade_distributions.to_json(orient='records')), 200

@app.route('/comments', methods=["GET", "POST"])
def handle_comments():
    if request.method == 'GET':
        # Fetch all comments from the database
        comments = Comment.query.all()
        return jsonify([comment.serialize() for comment in comments]), 200

    elif request.method == 'POST':
        data = request.json  # Get JSON data from the request

        # Extract user_id and content from the request
        user_id = data.get('user_id')
        content = data.get('content')

        # Use the add_comment function to create a new comment
        new_comment = add_comment(user_id, content)

        if new_comment:
            return jsonify({'message': 'Comment added!', 'comment': new_comment.serialize()}), 201

        return jsonify({'message': 'Failed to add comment. Check user_id and content.'}), 400

# Route to delete a comment by ID
@app.route('/comments/delete', methods=[ "POST" ])
def remove_comment():

    id = request.args.get('id')

    comment = fetch_comment( id )

    if not comment:
        return jsonify({ 'message': 'Comment not found' }), 404

    delete_comment( comment )
    return jsonify({ 'message': 'Comment deleted successfully' }), 200

# Route to get total average rating for a professor
@app.route('/ratings/get_rating', methods=["POST"])
def get_rating():
    if request.method == 'POST':
        # Get JSON data from the request
        data = request.json

        # get instructor name
        instructor_name = data.get('instructor_name')

        if not instructor_name:
            return jsonify({"error": "Instructor name is required"}), 400

        # Fetch all ratings on instructor from the database
        ratings = InstructorRating.query.filter_by(instructor_name=instructor_name).all()
        
        # get average rating if there are some existing
        average_rating = 0
        if len(ratings) > 0:
            average_rating = (sum([rating.rating for rating in ratings])/len(ratings))
        return jsonify({'rating': average_rating}), 200
    
# Route to add rating for a professor
@app.route('/ratings/post_rating', methods=["POST"])
def post_rating():
    if request.method == 'POST':
        data = request.json  # Get JSON data from the request

        # Extract user_id and content from the request
        user_id = data.get('user_id')
        instructor_name = data.get('instructor_name')
        rating = data.get('rating')

        # Check if rating is a valid percentage
        if rating > 0 and rating <= 1:
            # Use the add_rating function to create a new rating
            new_rating, success_message = add_rating(user_id, instructor_name, rating)

            # Check if rating was successfully added
            if new_rating:
                return jsonify({'message': success_message}), 201
            
            return jsonify({'message': 'Failed to add rating. Check user id and instructor name.'}), 400
            
        return jsonify({'message': 'Failed to add rating. Rating not a valid percentage.'}), 400

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
