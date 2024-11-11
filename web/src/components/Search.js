import React from "react";
import {useNavigate} from "react-router-dom";

import '../styles/Search.css';

const Search = () => {
    // make a tied variable and mutator for string inputted
    const [search, setSearch] = React.useState("");

    // this pair will hold the classes from search and the other will update the classes
    const [filteredResults, setFilteredResults] = React.useState([]);

    // this will set up the navigation to the class page
    const navigate = useNavigate();

    // set up a function to update the value when it is changes
    const handleInputChange = async(input) => {
        // this will set the form data to the search variable and call the mutator search function
        const newValue = input.target.value;
        setSearch(newValue);
        
        // if char count greater than 3 then call the search function
        if (newValue.length > 3) {
            await handleSearch(newValue);
        }
    }

    // Define a function to call setSearch function to update the search variable
    const handleSearch = async (input) => {

        console.log(input);

        // make a fetch request to the API to get the search results
        try {
            const res = await fetch(`http:/service/search`, {  // Needs to be whole url as header is consistent with all pages
                method: 'POST', 
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({query: input}) 
            })

            // if the fetch was successful then update the classes
            if (res.ok) 
            {
                const data = await res.json();
                setFilteredResults(data);
            }
            else 
            {
                console.error('Fetch was unsuccessful');    
            }

        } catch (error) {
            console.error(error);
        }
    }

    const handleItemClick = async (item, type) => {
        
        if(type === "instructor") {
            // this will redirect to the Prof page
            // get lowercase of name
            const prof = item.toLowerCase();

            // split the name into first and last
            const last = prof.split(",")[0];

            // in case of multiple "first" names
            const first = prof.split(",")[1].split(' ')[0];
            
            await navigate(`/professor/${last}-${first}`);
        }
        else if(type === "class") {
            // replace space with -
            item = item.replace(' ', '-');

            // this will redirect to the class page
            await navigate(`/class/${item}`);

        }

        // clear the search bar

        // refresh the page
        window.location.reload();
    }


    return (
        <div className="search-bar-box">
            <h1>Louie's Ratings</h1>

            <div className="search-container">
                <input type="text" className="search-bar" placeholder="Search..." value={search} onChange={handleInputChange}/>

                
                {search && filteredResults.length > 0 && filteredResults[0].length > 0 && (
                    <ul className="dropdown">
                        {filteredResults[0].slice(0,5).map((Item) => ( // only show the first 5 results bc we dont want to overload the user and system
                            <li key={Item} onClick={() => handleItemClick(Item, filteredResults[1])}>
                                {Item || 'Unnamed Item'}
                            </li>
                        ))}
                    </ul>
                )}
            </div>

        </div>
    );
}

export default Search;