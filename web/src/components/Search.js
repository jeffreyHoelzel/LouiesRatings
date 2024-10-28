import React from "react";
import {useNavigate} from "react-router-dom";

const Search = () => {
    // make a tied variable and mutator for string inputted
    const [search, setSearch] = React.useState("");

    // this pair will hold the classes from search and the other will update the classes
    const [filteredProfs, setFilteredProfs] = React.useState([]);

    // this will set up the navigation to the class page
    const navigate = useNavigate();

    // set up a function to update the value when it is changes
    const handleInputChange = (input) => {
        // this will set the form data to the search variable and call the mutator search function
        // side note this might change to be dynamic with the search idk how big our data set yet is
        setSearch(input.target.value);

        // if char count greater tham 3 then call the search function
        if (input.target.value.length > 3) {
            handleSearch(input);
        }
    }

    // Define a function to call setSearch function to update the search variable
    const handleSearch = async (input) => {

        // prevents enter from refreshing the page
        input.preventDefault(); 

        // make a fetch request to the API to get the search results
        try {
            const res = await fetch(`http:/service/search`, {  // Needs to be whole url as header is consistent with all pages
                method: 'POST', 
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({query: search}) 
            })

            // if the fetch was successful then update the classes
            if (res.ok) 
            {
                const data = await res.json();
                setFilteredProfs(data);
            }
            else 
            {
                console.error('Fetch was unsuccessful');    
            }

        } catch (error) {
            console.error(error);
        }
    }

    const handleProfClick = (prof) => {
        // this will redirect to the Prof page

        // get lowercase of name
        prof = prof.toLowerCase();

        // split the name into first and last
        const last = prof.split(",")[0];

        // in case of multiple "first" names
        const first = prof.split(",")[1].split(' ')[0];
        
        navigate(`/professor/${last}-${first}`);
    }


    return (
        <div className="search-bar-box">
            <h1>Louie's Ratings</h1>
            <form onSubmit={handleSearch}>
                <input type="text" className="search-bar" placeholder="Search..." value={search} onChange={handleInputChange}/>
                <button type="submit" className="search-button">Search</button>
            </form>

            {search && filteredProfs.length > 0 && (
                <ul className="dropdown">
                    {filteredProfs.slice(0,5).map((prof) => ( // only show the first 5 results bc we dont want to overload the user and system
                        <li key={prof} onClick={() => handleProfClick(prof)}>
                            {prof || 'Unnamed professor'}
                        </li>
                    ))}
                </ul>
            )}

        </div>
    );
}

export default Search;