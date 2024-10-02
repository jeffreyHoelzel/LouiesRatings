import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './index.css';
import App from './App';
import AddData from './DBExample';

// I am gonna be so real I don't know what I did

ReactDOM.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/db_example"element={<AddData />} />
      </Routes>
    </Router>
  </React.StrictMode>,
  document.getElementById('root')
);
