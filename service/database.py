# For accessing webscraping script
from flask_sqlalchemy import SQLAlchemy
from webscraper import get_all_grade_distribution_data_parallel

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

def fetch_classes(class_name: str):
    # get all classes (id, name) from database that match the string up to that point
    return db.session.query(ClassData).with_entities(ClassData.class_nbr, ClassData.class_name).filter_by(class_name=class_name).all()

# ====================================