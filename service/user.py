from database import db, Account
import bcrypt as bc

def add_user(username, password, email, first_name, last_name):        
    # convert password to byte string
    byte_password = password.encode('utf-8')
    # generate salt
    salt = bc.gensalt()
    # get hashed password with salt
    hashed_password = bc.hashpw(byte_password, salt)

    # if all credentials are not empty strings, create a new user object, otherwise, throw error
    if all([username, password, email, first_name, last_name]):
        new_user = Account(username=username, password=hashed_password, email=email, first_name=first_name, last_name=last_name)
    else:
        return 'Server was provided with incomplete information.', True, 422

    # search for username and email in database
    user_db = db.session.query(Account).filter_by(username=username, email=email).first()

    # if either are in use, send 403 response (already exists)
    if user_db is not None:
        return 'Username or email already in use.', True, 403
    
    # otherwise, add user to database
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as database_error:
        # Roll back the session in case of error
        db.session.rollback()

    # return success message and 200 response (ok)
    return 'New user successfully added.', False, 200

def try_login(requested_username, requested_password):
    # get user from database using username
    user = db.session.query(Account).filter_by(username=requested_username).first()

    # check if user exists if a valid password is present
    if user is not None:
        db_password = user.password # user may be None so password attribute will not be present
        # verify password
        if bc.checkpw(requested_password.encode('utf-8'), db_password):
            return 'User logged in successfully.', True, 200
        else:
            return 'Incorrect password. Please try again.', False, 401
    else:
        return 'The user specified does not exist. Please try again.', False, 401
    
def fetch_user_id(username):
    return Account.query.filter_by(username=username).first().id