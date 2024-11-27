import React from 'react';
import TopProfessors from './TopProfessors';

// make a main component for the website that contains the main content (class and professor ratings)
const Main = () => {
  return (
    <main>
      <div className="content-box">
        <div className="description">
          <h2>Welcome to Louie’s Ratings.</h2>
          <p>We help NAU students make confident course choices by providing insights into professor teaching styles, grade distributions, and student feedback.</p>
          <p>Get the information you need to succeed each semester, all in one place.</p>
        </div>
      </div>
      <TopProfessors/>
    </main>
  );
};

export default Main;
