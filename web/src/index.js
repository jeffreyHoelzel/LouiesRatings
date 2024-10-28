import React from 'react';
import { createRoot } from 'react-dom/client';
import './styles/homepage.css';
import './styles/login.css';
import App from './App';

// I am gonna be so real I don't know what I did

const root = createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
      <App />
  </React.StrictMode>
);