import React from "react";

const Search = () => {
    // make a tied variable and mutator for string inputted
    const [search, setSearch] = React.useState("");

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

            .then(res => res.json()) // will return the json data
            .then(data => { console.log(data)}) // now this line will send data to console which you can see with crtl+shift+i on chrome
            .catch(err => console.log(err)); // will catch any errors but idk if we need this
        
            // the code above is temp after the fetch because the other parts isnt fleshed out yet
    }


    return (
        <div className="search-bar-box">
            <h1>Louie's Ratings</h1>
            <form onSubmit={handleSearch}>
                <input type="text" className="search-bar" placeholder="Search..." value={search} onChange={handleInputChange}/>
            </form>
        </div>
    );
}

export default Search;