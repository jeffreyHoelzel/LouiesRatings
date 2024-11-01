# For accessing webscraping script
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# create sqlalchemy object
db = SQLAlchemy()

# ====================================
# DATABASE MODELS
# ====================================
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
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
      
class Comment(db.Model):
    id = db.Column( db.Integer, primary_key=True, autoincrement = True )
    user_id = db.Column( db.Integer, autoincrement=True, nullable=False )
    content = db.Column( db.Text, nullable=False )
    timestamp = db.Column( db.DateTime, default=datetime.utcnow)

    def serialize( self ):
        return {
            'id' : self.id,
            'user_id': self.user_id,
            'content': self.content,
            'timestamp': self.timestamp.isoformat()
        }
      
# ====================================




# ====================================
# DATABASE FUNCTIONS
# ====================================

def add_comment(user_id, content):
    try:
        # Create a new Comment object with the provided user_id and content
        new_comment = Comment(user_id=user_id, content=content)
        
        # Add the new comment to the database session
        db.session.add(new_comment)
        
        # Commit the session to save changes
        db.session.commit()
        
        return new_comment  # Return the newly created comment
    except Exception as database_error:
        # Roll back the session in case of error
        db.session.rollback()
        
        return None

def fetch_comment(comment_id):
    return Comment.query.get(comment_id)

def delete_comment(comment):
    # Check if the comment exists
    db.session.delete(comment)
    db.session.commit()
    return True
    
def fetch_classes(class_name: str):
    # get all classes (id, name) from database that match the string up to that point
    return db.session.query(ClassData).with_entities(ClassData.class_nbr, ClassData.class_name).filter_by(class_name=class_name).all()

def search_instructors(instructor_name: str):
    # get all instructors (name) from database that match the string up to that point

    # make them distinct
    instructor_names = ClassData.query.with_entities(ClassData.instructor_name).filter(ClassData.instructor_name.ilike(f"%{instructor_name}%")).distinct().all()
    
    # convert to list of strings
    instructor_names = [name[0] for name in instructor_names]

    return instructor_names
  # ====================================
