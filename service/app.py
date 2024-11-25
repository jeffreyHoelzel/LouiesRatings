from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db
import logging
import sys
from search import search_for
from user import add_user, try_login
from page_data import get_professor_data, get_pass_fail_rate, get_class_data
from graph_data import get_graph_data, get_graph_options
from comments import add_comment, fetch_comments
from rating import get_average_rating, add_rating, get_top_rated_professors

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("service")

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
def send_message_route():

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
def search_route():

    # checks if the request is a get type also think Post as a way to send data to the backend to make changes to the data 
    # or just get data from the backend in this case
    if request.method == 'POST':

        # Get the JSON data from the request
        data = request.get_json() 

        # Extract the search query from the JSON data
        search_query = data.get('query')

        results = search_for(search_query)
        
        # Return the mock users to test and 200 means a successful request
        return jsonify(results), 200
    
@app.route('/register', methods=['POST'])
def register_route():
    if request.method == 'POST':
        # get JSON data from new user
        data = request.json

        # get username, password, email, first name, and last name
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        first_name = data.get('firstName')
        last_name = data.get('lastName')

        message, error, status_code = add_user(username, password, email, first_name, last_name)

        return jsonify({'message': message, 'error': error}), status_code
    
@app.route('/login', methods=['POST'])
def login_route():
    if request.method == 'POST':
        # get JSON data from user
        data = request.json
        requested_username = data.get('username')
        requested_password = data.get('password')

        message, exists, status_code = try_login(requested_username, requested_password)
    
        return jsonify({'message': message, 'exists': exists}), status_code
    
@app.route('/professor', methods=['GET'])
def get_professor_data_route():
    instructor_name = request.args.get('name')

    if instructor_name:
        full_instructor_name, course_data = get_professor_data(instructor_name)

        if full_instructor_name and course_data:
            # Include the full instructor name in the response
            return jsonify({"professor": full_instructor_name, "courses": course_data})

    return jsonify({"error": "Professor not found"}), 404

@app.route('/get_pass_fail_rate', methods=['POST'])
def get_pass_fail_rate_route():

    data = request.json

    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    search_by = data.get('search_by')
    search_name = data.get(search_by)

    if not search_by or not search_name:
        return jsonify({"error": "Invalid search criteria"}), 400

    # Fetch grade data from database, setup to work with class or instructor
    pass_rate, fail_rate, message, status_code = get_pass_fail_rate(search_by, search_name)

    if message == None:
        return jsonify({"pass_rate": pass_rate, "fail_rate": fail_rate}), status_code
    
    return jsonify({"error": message}), status_code

@app.route('/class', methods=['GET'])
def get_class_data_route():
    class_id = request.args.get('classId') 
    if not class_id:
        return jsonify({"error": "Class ID is required"}), 400

    class_data, status_code = get_class_data(class_id)
    if class_data:
        return jsonify({"class": class_data}), status_code
    
    return jsonify({"error": "Class not found"}), status_code

@app.route('/get_graph_data', methods=["POST"])
def get_graph_data_route():
    if request.method == 'POST':
        request_data = request.json  # Get JSON data from the request

        # get specfic class data
        search_by = request_data.get('search_by')
        search_name = request_data.get(search_by)
        option = request_data.get('option')

        grade_distributions, status_code = get_graph_data(search_by, search_name, option)
        
        if not grade_distributions.empty:
            return jsonify(grade_distributions.to_json(orient='records')), status_code
        
        return jsonify({"error": "No grade distributions for chart found"}), 404

@app.route('/get_graph_options', methods=["POST"])
def get_graph_options_route():
    if request.method == 'POST':
        request_data = request.json  # Get JSON data from the request

        # get specfic class data
        search_by = request_data.get('search_by')
        search_name = request_data.get(search_by)

        options = get_graph_options(search_by, search_name)
        
        return jsonify(options), 200

@app.route('/comment/load_comments', methods=['GET'])
def load_comments_route():
    if request.method == 'GET':
        review_type = request.args.get('review_type')
        
        comments = fetch_comments(review_type)

        if comments:
            return jsonify([comment.serialize() for comment in comments]), 200
    
        return jsonify([]), 400
        
@app.route('/comment/post_comment', methods=['POST'])
def post_comment():
    if request.method == 'POST':
        data = request.json

        # get username, instructor/course name, and content of comment
        username = data.get('username')
        review_type = data.get('reviewType')
        content = data.get('content')

        if all([username, review_type, content]):
            new_comment = add_comment(username, review_type, content)

            if new_comment:
                return jsonify({'message': 'Comment added successfully.', 'comment': new_comment.serialize()}), 200
            
            return jsonify({'message': 'Comment not added. Check content.'}), 400

# Route to delete a comment by ID
# @app.route('/comments/delete', methods=[ "POST" ])
# def remove_comment():

#     id = request.args.get('id')

#     comment = fetch_comment( id )

#     if not comment:
#         return jsonify({ 'message': 'Comment not found' }), 404

#     delete_comment( comment )
#     return jsonify({ 'message': 'Comment deleted successfully' }), 200

# Route to get total average rating for a professor
@app.route('/ratings/get_rating', methods=["POST"])
def get_rating_route():
    if request.method == 'POST':
        # Get JSON data from the request
        data = request.json

        # get 
        search_by = data.get('search_by')
        search_name = data.get(search_by)

        average_rating, status_code = get_average_rating(search_by, search_name)

        return jsonify({'rating': average_rating}), status_code
    
# Route to add rating for a professor
@app.route('/ratings/post_rating', methods=["POST"])
def post_rating_route():
    if request.method == 'POST':
        data = request.json  # Get JSON data from the request

        # Extract content from the request
        username = data.get('username')
        rating = data.get('rating')
        search_by = data.get('search_by')
        search_name = data.get(search_by)

        message, status_code = add_rating(username, rating, search_by, search_name)

        return jsonify({'message': message}), status_code

@app.route('/top_professors', methods=['GET'])
def top_professors():
    if request.method == 'GET':
        # Fetch top professors
        professors, status = get_top_rated_professors()

        # Return the list of professors as JSON, if any, or an empty list if none found
        return jsonify(professors), status

# ====================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
