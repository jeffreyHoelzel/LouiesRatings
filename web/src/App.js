import React, { useState, useEffect } from 'react';
import './styles/main.css';
import Header from './components/Header';
import Main from './components/Main';
import ClassPage from './components/ClassPage'; 
import ProfessorPage from './components/ProfessorPage';
import TopProfessors from './components/TopProfessors';
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
          <Route path="/professor/:professorId" element={<ProfessorPage />} />
          <Route path="/class/:classId" element={<ClassPage />} /> 
          <Route path="/top_professors" element={<TopProfessors />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
