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
        return None, 404
    
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

    # add row for column sums
    grade_distributions.loc["sum"] = grade_distributions.sum(numeric_only=True)

    # remove all rows except for the last two
    grade_distributions = grade_distributions.iloc[[-1]]

    # transpose, and make the index a column for grades
    grade_distributions = grade_distributions.T.reset_index(drop=False).rename(columns={"index":"grade"})

    return grade_distributions, 200

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