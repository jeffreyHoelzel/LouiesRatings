import unittest
import sys
import os
import bcrypt as bc

# appends path for dockerfile, ignore warnings
sys.path.append(os.path.abspath("/app/service"))

from app import app
from database import db, Account, ClassData, InstructorComment, CourseComment, InstructorRating, ClassRating

from search import search_for
from user import add_user, try_login
from page_data import get_professor_data, get_pass_fail_rate, get_class_data
from graph_data import get_graph_data, get_graph_options
from comments import add_comment, fetch_comments
from rating import get_average_rating, add_rating

class TestBackend(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        cls.app = app
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        with cls.app_context:
            db.create_all()

        ############################################################
        ## ADD TEST DATA HERE
        ############################################################

        with cls.app_context:

            # class data for searching test
            class_data = ClassData(
                semester="Fall 2024",
                subject="CS",
                class_name="CS 249",
                section="2",
                class_nbr=1234,
                instructor_name="Doe,Jane",
                a=20,
                b=15,
                c=10,
                d=5,
                f=2,
                au=0,
                p=0,
                ng=0,
                w=3,
                i=1,
                ip=0,
                pending=0,
                total=56
            )
            db.session.add(class_data)

            # user data for testing login/registration
            hashed_pw = bc.hashpw("fakepassword123".encode("utf-8"), bc.gensalt())

            user_data = Account(
                username="testuser1",
                password=hashed_pw,
                first_name="Test",
                last_name="User",
                email="testuser1@example.com"
            )

            db.session.add(user_data)
            db.session.commit()

    def test_course_search(self):
        result = search_for("CS 249")
        self.assertEqual(result[0], ["CS 249"])
        self.assertEqual(result[1], "class")

    def test_instructor_search(self):
        result = search_for("Jane")
        self.assertEqual(result[0], ["Doe,Jane"])
        self.assertEqual(result[1], "instructor")

    def test_add_new_user(self):
        message, error, status = add_user(username="testuser2", password="fakepassword123", email="testuser2@example.com", first_name="Test", last_name="User2")
        self.assertEqual(message, "New user successfully added.")
        self.assertEqual(error, False)
        self.assertEqual(status, 200)

    def test_add_existing_user(self):
        message, error, status = add_user(username="testuser1", password="fakepassword123", email="testuser1@example.com", first_name="Test", last_name="User1")
        self.assertEqual(message, "Username or email already in use.")
        self.assertEqual(error, True)
        self.assertEqual(status, 403)

    def test_add_user_incomplete_info(self):
        message, error, status = add_user(username="", password="fakepassword123", email="testuser3@example.com", first_name="Test", last_name="User3") # no username, will work for any other missing parameter
        self.assertEqual(message, "Server was provided with incomplete information.")
        self.assertEqual(error, True)
        self.assertEqual(status, 422)

    def test_successful_login(self):
        message, logged_in, status = try_login(requested_username="testuser1", requested_password="fakepassword123")
        self.assertEqual(message, "User logged in successfully.")
        self.assertEqual(logged_in, True)
        self.assertEqual(status, 200)

    def test_unsuccessful_login(self):
        message, logged_in, status = try_login(requested_username="testuser1", requested_password="fakepassword") # incorrect password
        self.assertEqual(message, "Incorrect password. Please try again.")
        self.assertEqual(logged_in, False)
        self.assertEqual(status, 401)

    def test_login_user_dne(self):
        message, logged_in, status = try_login(requested_username="testuser4", requested_password="fakepassword123") # user dne
        self.assertEqual(message, "The user specified does not exist. Please try again.")
        self.assertEqual(logged_in, False)
        self.assertEqual(status, 401)
    
    def test_add_rating(self):
        message, status = add_rating("testuser2", 1, "class_name", "CS 249")
        self.assertEqual(message, 'Rating added!')
        self.assertEqual(status, 201)
    
    def test_average_rating(self):
        average_rating, status = get_average_rating("class_name", "CS 249")
        self.assertEqual(average_rating, 1)
        self.assertEqual(status, 200)

    def test_graph_options(self):
        options = get_graph_options("class_name", "CS 249")
        self.assertEqual(options, ["All", "Doe,Jane"])
    
    def test_get_graph_data(self):
        grade_distributions, status = get_graph_data("class_name", "CS 249", "Doe,Jane")
        self.assertEqual(grade_distributions.loc[0, 'sum'], 20)
        self.assertEqual(grade_distributions.loc[1, 'sum'], 15)
        self.assertEqual(grade_distributions.loc[2, 'sum'], 10)
        self.assertEqual(grade_distributions.loc[3, 'sum'], 5)
        self.assertEqual(grade_distributions.loc[4, 'sum'], 2)
        self.assertEqual(grade_distributions.loc[5, 'sum'], 0)
        self.assertEqual(grade_distributions.loc[6, 'sum'], 3)
        self.assertEqual(status, 200)

    def test_add_course_comment_successfully(self):
        comment = add_comment(username="testuser1", review_type="CS 249", content="test comment")
        self.assertEqual(comment.class_name, "CS 249")
        self.assertEqual(comment.content, "test comment")

    def test_add_instructor_comment_successfully(self):
        comment = add_comment(username="testuser1", review_type="Doe,Jane", content="test comment")
        self.assertEqual(comment.instructor_name, "Doe,Jane")
        self.assertEqual(comment.content, "test comment")

    def test_add_course_comment_unsuccessfully(self):
        comment = add_comment(username="", review_type="CS 249", content="test comment")
        self.assertEqual(comment, None)

    def test_add_instructor_comment_unsuccessfully(self):
        comment = add_comment(username="", review_type="Doe,Jane", content="test comment")
        self.assertEqual(comment, None)

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

if __name__ == "__main__":
    unittest.main()
