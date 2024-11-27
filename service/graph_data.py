from database import ClassData
import pandas as pd

def get_graph_data(search_by, search_name, option):
    # initialize the query
    query = ClassData.query

    # build the filter conditions
    if search_by == 'class_name':
        query = query.filter_by(class_name=search_name)
        if option != "All":
            query = query.filter_by(instructor_name=option)
            
    else:
        query = query.filter_by(instructor_name=search_name)
        if option != "All":
            query = query.filter_by(class_name=option)

    # execute the query and get the result
    class_data = query.all()

    if len(class_data) == 0:
        # nothing found, so return empty data
        return pd.DataFrame(), 404
    
    # create pandas data frame user the data, only get relevant information
    grade_distributions= pd.DataFrame([
        {
            'A': data.a,
            'B': data.b,
            'C': data.c,
            'D': data.d,
            'F': data.f,
            'P': data.p,
            'W': data.w
        } for data in class_data
    ])

    pass_rate, fail_rate, withdraw_rate =  calculate_pass_fail_rates(grade_distributions)

    # add row for column sums
    grade_distributions.loc["sum"] = grade_distributions.sum(numeric_only=True)

    # remove all rows except for the sum
    grade_distributions = grade_distributions.iloc[[-1]]

    # transpose, and make the index a column for grades
    grade_distributions = grade_distributions.T.reset_index(drop=False).rename(columns={"index":"grade"})

    return grade_distributions, pass_rate, fail_rate, withdraw_rate, 200

def get_graph_options(search_by, search_name):
    # default option
    options = ["All"]

    if search_by == 'class_name':
        class_data = ClassData.query.filter_by(class_name=search_name).all()
        new_options = [data.instructor_name for data in class_data]
    else:
        class_data = ClassData.query.filter_by(instructor_name=search_name).all()
        new_options = [data.class_name for data in class_data]

    # make unqiue and sort
    new_options = sorted(list(set(new_options)))

    options += new_options

    return options

def get_professor_list(search_name):
    # get all options (minus All)
    professors = get_graph_options(search_by='class_name', search_name=search_name)
    professors.remove("All")
    return professors

def get_pass_fail_rate(search_by, search_name, option):
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

def calculate_pass_fail_rates(grade_distributions: pd.DataFrame):
    grade_sums = grade_distributions.sum(numeric_only=True)
    total_pass = grade_sums['A'] + grade_sums['B'] + grade_sums['C'] + grade_sums['P']
    total_fail = grade_sums['D'] + grade_sums['F']
    total_withdraw = grade_sums['W']
    total_grades = total_pass + total_fail + total_withdraw

    # Calculate final pass/fail rates
    pass_rate = (total_pass / total_grades * 100) if total_grades > 0 else 0
    fail_rate = (total_fail / total_grades * 100) if total_grades > 0 else 0
    withdraw_rate = (total_withdraw / total_grades * 100) if total_grades > 0 else 0

    return pass_rate, fail_rate, withdraw_rate