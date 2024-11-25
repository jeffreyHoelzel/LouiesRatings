from database import db, ClassRating, InstructorRating, ClassData
from user import fetch_user_id
from sqlalchemy import func

def get_average_rating(search_by, search_name):
# Fetch all ratings on instructor/class from the database
    if search_by == 'class_name':
        ratings = ClassRating.query.filter_by(class_name=search_name).all()
    elif search_by == 'instructor_name':
        ratings = InstructorRating.query.filter_by(instructor_name=search_name).all()
    else:
        return 0, 400
    
    # get average rating if there are some existing
    average_rating = 0
    if len(ratings) > 0:
        average_rating = (sum([rating.rating for rating in ratings])/len(ratings))
    
    return average_rating, 200

def add_rating(username, rating, search_by, search_name):
    if username:
        # Get the user id from username
        user_id = fetch_user_id(username)
    else:
        return 'Username parameter missing or not provided.', 400

    # Check if rating is a valid percentage
    if rating > 0 and rating <= 1:
        new_rating, success_message = add_rating_to_db(user_id, search_name, rating, by=search_by)

        # Check if rating was successfully added
        if new_rating:
            return success_message, 201
        
        return 'Failed to add rating. Check username and instructor name.', 400
        
    return 'Failed to add rating. Rating not a valid percentage.', 400

def add_rating_to_db(user_id, search_name, rating, by):
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
    
def get_top_rated_professors():
    num_top_professors = 3
    try:       
        # Fetch top-rated professors based on average rating from InstructorRating
        top_professors = InstructorRating.query \
            .with_entities(InstructorRating.instructor_name, db.func.avg(InstructorRating.rating).label('avg_rating')) \
            .group_by(InstructorRating.instructor_name) \
            .order_by(db.func.avg(InstructorRating.rating).desc()) \
            .order_by(func.random()) \
            .limit(num_top_professors).all()

        if len(top_professors) >= 3:
            return [{
                'instructor_name': professor.instructor_name,
                'avg_rating': professor.avg_rating
            } for professor in top_professors], 200

        # Otherwise, get random professors to fill up the rest
        avg_ratings = []
            
        random_professors = (
            ClassData.query
            .with_entities(ClassData.instructor_name)
            .distinct()
            .order_by(func.random())
            .limit(num_top_professors - len(top_professors))  # Only get the needed amount
            .all()
        )

        for professor in top_professors:
            avg_ratings.append({
                'instructor_name': professor.instructor_name,
                'avg_rating': professor.avg_rating
            })
            
        for professor in random_professors:
            avg_ratings.append({
                'instructor_name': professor.instructor_name,
                'avg_rating': 0
            })

        return avg_ratings, 200

    except Exception as database_error:
        # Rollback the session in case of error
        db.session.rollback()

        return [], 400