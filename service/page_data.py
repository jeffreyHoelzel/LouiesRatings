from database import ClassData
import pandas as pd
from collections import Counter

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
            "section": course.section,
        }
        for course in courses
    ]

    return full_instructor_name, course_data

def get_pass_fail_rate(search_by, search_name):
    try:
        if search_by == 'class_name':
            grade_data = ClassData.query.filter_by(class_name=search_name).all()
        elif search_by == 'instructor_name':
            grade_data = ClassData.query.filter_by(instructor_name=search_name).all()
        else:
            return 0, 0, "Invalid search criteria", 400

        if not grade_data:
            return 0, 0, None, 404

    except Exception as e:
        return 0, 0, "Database query failed", 500

    # Create a pandas DataFrame from the grade data to calculate pass/fail rates
    grade_distributions = pd.DataFrame([{
        'A': data.a,
        'B': data.b,
        'C': data.c,
        'D': data.d,
        'F': data.f,
        'P': data.p,
    } for data in grade_data])

    grade_sums = grade_distributions.sum(numeric_only=True)
    total_pass = grade_sums['A'] + grade_sums['B'] + grade_sums['C'] + grade_sums['P']
    total_fail = grade_sums['D'] + grade_sums['F']
    total_grades = total_pass + total_fail

    # Calculate final pass/fail rates
    pass_rate = (total_pass / total_grades * 100) if total_grades > 0 else 0
    fail_rate = (total_fail / total_grades * 100) if total_grades > 0 else 0

    return pass_rate, fail_rate, None, 200

def get_class_data(class_id):
    # Fetch class data from the database
    class_data = ClassData.query.filter_by(class_name=class_id).first()

    if class_data:
        all_class_data = ClassData.query.all()

        all_instructors = [data.instructor_name for data in all_class_data]

        value_counts = Counter(all_instructors)

        most_common_instructor, count = value_counts.most_common(1)[0]

        return {
            "title": f"{class_data.subject} {class_data.class_name}",
            "code": class_data.class_name,
            "instructor": most_common_instructor
        }, 200

    return None, 404