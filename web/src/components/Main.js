import React from 'react';
import TopProfessors from './TopProfessors';

// make a main component for the website that contains the main content (class and professor ratings)
const Main = () => {
  return (
    <main>
      <div className="title-box">
        <h1>Louie's Ratings</h1>
        <p>By students, for students</p>
      </div>
      <TopProfessors/>
    </main>
  );
};

export default Main;
