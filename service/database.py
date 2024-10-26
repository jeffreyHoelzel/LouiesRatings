# For accessing webscraping script
from flask_sqlalchemy import SQLAlchemy

# create sqlalchemy object
db = SQLAlchemy()

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
    instructor_name = db.Column(db.String(100), nullable=False)
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

# ====================================