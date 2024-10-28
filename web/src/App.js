import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Main from './components/Main';
import Footer from './components/Footer';
import ClassPage from './components/ClassPage'; 
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

function App() {
  const [message, setMessage] = useState("Loading...");

  // console.log('Backend URL:', process.env.REACT_APP_BACKEND_URL);

  // For testing only
  // This block of code sends a 'GET request' to the backend server
  useEffect(() => {
    const backendUrl = "/service/";

    // Parses the data
    fetch(backendUrl)
      .then(res => res.json())
      .then(data => setMessage(data.message))
      .catch(err => setMessage("Error connecting to backend", err));
  }, []);

  // Changes the html content in /web/public/index.html
  return (
    <Router>
      <div>
        <Header />
        <Routes>
          <Route path="/" element={<Main />} />
          <Route path="/class/:classId" element={<ClassPage />} /> 
        </Routes>
        <Footer />
        {/* <p>{message}</p> */}
      </div>
    </Router>
  );
}

export default App;
