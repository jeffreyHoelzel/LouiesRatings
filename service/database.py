# For accessing webscraping script
from flask_sqlalchemy import SQLAlchemy
from webscraper import get_all_grade_distribution_data_parallel
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
    
class CourseComment(db.Model):
    id = db.Column( db.Integer, primary_key=True, autoincrement = True )
    user_id = db.Column( db.Integer, autoincrement=True, nullable=False )
    class_name = db.Column(db.String(10), nullable=False)
    content = db.Column( db.Text, nullable=False )
    timestamp = db.Column( db.DateTime, default=datetime.utcnow)

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
def fetch_grade_distribution_data(db: SQLAlchemy):
    grade_distribution_df = get_all_grade_distribution_data_parallel()

    data_to_add = []
    
    # create database object for each row
    # note: I want to use .tosql, but it won't work
    for idx, row in grade_distribution_df.iterrows():
        data = ClassData(
            semester = row["Semester"],
            subject = row["Subject"],
            class_name = row["Class"],
            section = row["Section"],
            class_nbr = int(row["Class NBR "]),
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
    
  # ====================================
