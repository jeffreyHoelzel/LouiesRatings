import unittest
import sys
import os

# appends path for dockerfile, ignore warnings
sys.path.append(os.path.abspath("/app/service"))

from search import search_for
from user import add_user, try_login
from page_data import get_professor_data, get_pass_fail_rate, get_class_data
from graph_data import get_graph_data, get_graph_options
from comments import add_comment, fetch_comments
from rating import get_average_rating, add_rating

class TestBackend(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()
