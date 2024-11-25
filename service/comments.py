from database import db, CourseComment, InstructorComment
from user import fetch_user_id
# constants
MAX_COURSE_NUM_LEN: int = 7

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