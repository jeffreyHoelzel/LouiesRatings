import React, { useState, useEffect } from 'react';

function App() {
  const [message, setMessage] = useState("Loading...");

  // console.log('Backend URL:', process.env.REACT_APP_BACKEND_URL);

  // For testing only

  // This block of code sends a 'GET request' to the backend server
  useEffect(() => {
    const backendUrl = "http://localhost:5000";

    // parses the data
    fetch(backendUrl)
      .then(res => res.json())
      .then(data => setMessage(data.message))
      .catch(err => setMessage("Error connecting to backend"));

  }, []);

  // changes the html content in /web/public/index.html
  return (
    <div>
      <h1>Frontend - React App</h1>
      <p>Backend says: {message}</p>
    </div>
    
  );
}

export default App;

