# For accessing webscraping script
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# create sqlalchemy object
db = SQLAlchemy()

# ====================================
# DATABASE MODELS
# ====================================
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.LargeBinary, nullable=False) # hashed password as byte string (don't have to mess with encode/decode)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)

    def __repr__(self):
        return f"username : {self.username}, password : {self.password}, first_name : {self.first_name}, last_name : {self.last_name}, email : {self.email}"

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
     
    # method to convert the object to a dictionary
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
      
class InstructorComment(db.Model):
    id = db.Column( db.Integer, primary_key=True, autoincrement = True )
    user_id = db.Column( db.Integer, autoincrement=True, nullable=False )
    instructor_name = db.Column(db.String(20), nullable=False)
    content = db.Column( db.Text, nullable=False )
    timestamp = db.Column( db.DateTime, default=datetime.utcnow)

    def serialize( self ):
        # get username from id for display
        username = Account.query.filter_by(id=self.user_id).first().username

        return {
            'id' : self.id,
            'user_id': self.user_id,
            'username': username,
            'instructor_name': self.instructor_name,
            'content': self.content,
            'timestamp': self.timestamp.isoformat()
        }
    
class CourseComment(db.Model):
    id = db.Column( db.Integer, primary_key=True, autoincrement = True )
    user_id = db.Column( db.Integer, autoincrement=True, nullable=False )
    class_name = db.Column(db.String(10), nullable=False)
    content = db.Column( db.Text, nullable=False )
    timestamp = db.Column( db.DateTime, default=datetime.utcnow)

    def serialize( self ):
        # get username from id for display
        username = Account.query.filter_by(id=self.user_id).first().username

        return {
            'id' : self.id,
            'user_id': self.user_id,
            'username': username,
            'class_name': self.class_name,
            'content': self.content,
            'timestamp': self.timestamp.isoformat()
        }

class InstructorRating(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    instructor_name = db.Column(db.String(50), nullable=False)
    # rating saved as percentage (allows for dynamic stars)
    rating = db.Column(db.Float, nullable=False)

class ClassRating(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    class_name = db.Column(db.String(10), nullable=False)
    # rating saved as percentage (allows for dynamic stars)
    rating = db.Column(db.Float, nullable=False)

# ====================================
