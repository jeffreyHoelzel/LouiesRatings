# For accessing webscraping script
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# create sqlalchemy object
db = SQLAlchemy()

# constants
MAX_COURSE_NUM_LEN: int = 7

# ====================================
# DATABASE MODELS
# ====================================
class Person(db.Model):
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
        username = fetch_username(self.user_id)

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
        username = fetch_username(self.user_id)

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




# ====================================
# DATABASE FUNCTIONS
# ====================================

def add_comment(username, review_type, content):
    try:
        # Get user id by provided username
        user_id = fetch_user_id(username)

        # Create a new Comment object with user_id, instructor/course name, and content
        if len(review_type) <= MAX_COURSE_NUM_LEN:
            new_comment = CourseComment(user_id=user_id, class_name=review_type, content=content)
        else:
            new_comment = InstructorComment(user_id=user_id, instructor_name=review_type, content=content)
        
        # Add the new comment to the database session
        db.session.add(new_comment)
        
        # Commit the session to save changes
        db.session.commit()
        
        return new_comment  # Return the newly created comment
    except Exception as database_error:
        # Roll back the session in case of error
        db.session.rollback()
        
        return None

def fetch_comments(search_by):
    if len(search_by) <= MAX_COURSE_NUM_LEN:
        return CourseComment.query.filter_by(class_name=search_by).all()

    return InstructorComment.query.filter_by(instructor_name=search_by).all()

# def delete_comment(comment):
#     # Check if the comment exists
#     db.session.delete(comment)
#     db.session.commit()
#     return True
    
def fetch_classes(class_name: str):
    # get all classes (id, name) from database that match the string up to that point
    return db.session.query(ClassData).with_entities(ClassData.class_nbr, ClassData.class_name).filter_by(class_name=class_name).all()

def search_for(search: str):
        
    # strip any non-alphanumeric characters
    search = ''.join(e for e in search if e.isalnum())

    # find the first digit in the string
    numIndex = 0
    for index, char in enumerate(search):
        if char.isdigit():
            numIndex = index
            break

    # if there is a number, search for class name
    if numIndex:

        # search for class name 
        search_results = ClassData.query.with_entities(ClassData.class_name).filter(ClassData.class_name.ilike(f"%{search[:numIndex]} {search[numIndex:]}%")).distinct().all()
        search_results = [name[0] for name in search_results]
        return [search_results, "class"]

    # assume name and make them distinct
    instructor_names = ClassData.query.with_entities(ClassData.instructor_name).filter(ClassData.instructor_name.ilike(f"%{search}%")).distinct().all()

    # combine the two lists into search_results
    search_results = [name[0] for name in instructor_names]

    return [search_results, "instructor"]

def add_rating(user_id, search_name, rating, by):
    try:
        # Check if user has already made a rating for this instructor/class
        rating_row = rating_exists(user_id, search_name, by=by)
        if rating_row:
            # overwrite current rating
            rating_row.rating = rating

            success_message = 'Previous rating overwritten!'
        else:

            if by == 'class_name':
                # Create a new ClassRating object with the provided user_id, class_name, and rating
                rating_row = ClassRating(user_id=user_id, class_name=search_name, rating=rating)
            else:
                # Create a new InstructorRating object with the provided user_id, instructor_name, and rating
                rating_row = InstructorRating(user_id=user_id, instructor_name=search_name, rating=rating)
            
            # Add the new rating to the database session
            db.session.add(rating_row)

            success_message = 'Rating added!'

        # Commit the session to save changes
        db.session.commit()
        
        # return new/overwritted rating and success mesage
        return rating_row, success_message
    
    except Exception as database_error:
        # Roll back the session in case of error
        db.session.rollback()
        
        return None, None

def rating_exists(user_id, search_name, by):
    if by == 'class_name':
        # return if the user has already given a rating to this class
        return ClassRating.query.filter_by(user_id=user_id, class_name=search_name).first()
    else:
        # return if the user has already given a rating to this instructor
        return InstructorRating.query.filter_by(user_id=user_id, instructor_name=search_name).first()
    

def fetch_user_id(username):
    # get user from database using username
    user = Person.query.filter_by(username=username).first()
    # return user id
    return user.id


def fetch_username(user_id):
    user = Person.query.filter_by(id=user_id).first()

    return user.username
  # ====================================
