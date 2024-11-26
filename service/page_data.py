from database import db, ClassData
import pandas as pd
from sqlalchemy import func
from flask import jsonify

def get_professor_data(instructor_name):
    # Split the instructor name into last name and first name and search database for any matching names
    last_name, first_name = instructor_name.split(", ")
    courses = ClassData.query.filter(
        ClassData.instructor_name.ilike(f"%{last_name}%"),
        ClassData.instructor_name.ilike(f"%{first_name}%")
    ).all()

    # Extract full instructor name from the first matched course, add space following comma
    full_instructor_name = courses[0].instructor_name
    
    course_data = [
        {
            "semester": course.semester,
            "subject": course.subject,
            "class_name": course.class_name,
            "section": course.section
        }
        for course in courses
    ]

    return full_instructor_name, course_data

def get_class_data(class_id):
    # Fetch class data from the database
    class_data = ClassData.query.filter_by(class_name=class_id).first()

    if class_data:
        '''
        // This works but I will leave it out for now
        primary_instructor_row = db.session.query(
            ClassData.instructor_name, func.count(ClassData.instructor_name).label('count')
            ).filter_by(class_name=class_id).group_by(ClassData.instructor_name).order_by(func.count(ClassData.instructor_name).desc()).first()
        '''
                                                       
        return {
            "title": f"{class_data.subject} {class_data.class_name}",
            "code": class_data.class_name
        }, 200
    
    return None, 404