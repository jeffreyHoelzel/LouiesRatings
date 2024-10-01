from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# For testing only


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# maybe change from sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///table.db'
db = SQLAlchemy(app)

# Models
class Profile(db.Model):
    # name: Used to store the first name if the user
    # Age: Used to store the age of the user
    name = db.Column(db.String(20), primary_key=True)
    age = db.Column(db.Integer, nullable=False)

    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"Name : {self.name}, Age: {self.age}"

# create database tables
with app.app_context():
    db.create_all()

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

@app.route('/add_data', methods=["GET", "POST"])
def profile():
    if request.method == 'POST':
        data = request.json  # Get JSON data from the request

        # In this function we will input data from the 
        # form page and store it in our database.
        # Remember that inside the get the name should
        # exactly be the same as that in the html
        # input fields
        name = data.get('name')
        age = data.get('age')
        # age = data["age"]
        # create an object of the Profile class of models
        # and store data as a row in our datatable
        if name != '' and age != '':
            p = Profile(name=name, age=age)
            db.session.add(p)
            db.session.commit()

        return jsonify({'message': 'Data received!', 'data': {'name': name}}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
