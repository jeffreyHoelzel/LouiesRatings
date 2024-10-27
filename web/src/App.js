import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Main from './components/Main';
import Footer from './components/Footer';
import Comment from './components/Comment';

function App() {
  const [message, setMessage] = useState("Loading...");

  // console.log('Backend URL:', process.env.REACT_APP_BACKEND_URL);

  // For testing only

  // This block of code sends a 'GET request' to the backend server
  useEffect(() => {
    const backendUrl = "/service/"

    // parses the data
    fetch(backendUrl)
      .then(res => res.json())
      .then(data => setMessage(data.message))
      .catch(err => setMessage("Error connecting to backend", err));

  }, []);

  // changes the html content in /web/public/index.html
  return (
    <div>
      <Header />
      <Main />
      <Comment />
      <Footer />
      <p>{message}</p>
    </div>
  );
}

export default App;

