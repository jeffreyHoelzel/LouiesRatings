import React from "react";
import {useNavigate} from "react-router-dom";

const Search = () => {
    // make a tied variable and mutator for string inputted
    const [search, setSearch] = React.useState("");

    // this pair will hold the classes from search and the other will update the classes
    const [filteredClasses, setFilteredClasses] = React.useState([]);

    // this will set up the navigation to the class page
    const navigate = useNavigate();

    // set up a function to update the value when it is changes
    const handleInputChange = (input) => {
        // this will set the form data to the search variable and call the mutator search function
        // side note this might change to be dynamic with the search idk how big our data set yet is
        setSearch(input.target.value);
    }

    // Define a function to call setSearch function to update the search variable
    const handleSearch = (input) => {

        // prevents enter from refreshing the page
        input.preventDefault(); 

        // make a fetch request to the API to get the search results
        fetch(`service/search`, { 
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({query: search}) 
        })

            //.then(res => res.json()) // will return the json data
            .then(data => { setFilteredClasses(data) }) // now this line will send data to console which you can see with crtl+shift+i on chrome
            .catch(err => console.log(err)); // will catch any errors but idk if we need this
        
            // the code above is temp after the fetch because the other parts isnt fleshed out yet

        console.log("search: ", filteredClasses);
    }

    const handleClassClick = (course) => {
        // this will redirect to the class page
        navigate(`/class/${course.id}`);
    }


    return (
        <div className="search-bar-box">
            <h1>Louie's Ratings</h1>
            <form onSubmit={handleSearch}>
                <input type="text" className="search-bar" placeholder="Search..." value={search} onChange={handleInputChange}/>
                <button type="submit" className="search-button">Search</button>
            </form>

            {search && filteredClasses.length > 0 && (
                <ul className="dropdown">
                    {filteredClasses.map((course) => (
                        <li key={course.id} onClick={() => handleClassClick(course)}>
                            {course.name}
                        </li>
                    ))}
                </ul>
            )}

        </div>
    );
}

export default Search;