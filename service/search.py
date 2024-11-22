from database import ClassData

def search_for(search: str):
        
    # strip any non-alphanumeric characters
    search = ''.join(e for e in search if e.isalnum())

    # find the first digit in the string
    numIndex = 0
    for index, char in enumerate(search):
        if char.isdigit():
            numIndex = index
            break

    # if there is a number, search for class name
    if numIndex:

        # search for class name 
        search_results = ClassData.query.with_entities(ClassData.class_name).filter(ClassData.class_name.ilike(f"%{search[:numIndex]} {search[numIndex:]}%")).distinct().all()
        search_results = [name[0] for name in search_results]
        return [search_results, "class"]

    # assume name and make them distinct
    instructor_names = ClassData.query.with_entities(ClassData.instructor_name).filter(ClassData.instructor_name.ilike(f"%{search}%")).distinct().all()

    # combine the two lists into search_results
    search_results = [name[0] for name in instructor_names]

    return [search_results, "instructor"]