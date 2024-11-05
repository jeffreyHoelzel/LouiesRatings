import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import '../styles/ProfessorPageStyling.css';
import Chart from './Chart';
import DisplayAverageRating from './DisplayAverageRating.js';
import SubmitRating from './SubmitRating.js';

const ProfessorPage = () => {
  const { professorId } = useParams();
  const [professorData, setProfessorData] = useState(null);
  const [error, setError] = useState(null);

  // Format professorId to "Last Name, First Name" for query
  const formatName = (id) => {
    if (!id) return null;
    const [lastName, firstName] = id.split('-');
    if (!lastName || !firstName) return null;
    return `${lastName.charAt(0).toUpperCase() + lastName.slice(1)}, ${firstName.charAt(0).toUpperCase() + firstName.slice(1)}`;
  };

  const instructorName = formatName(professorId);

  useEffect(() => {
    // Fetch professor data from the backend
    const fetchProfessorData = async () => {
      try {
        const response = await fetch(`/service/professor?name=${encodeURIComponent(instructorName)}`);
        if (!response.ok) throw new Error("Professor not found.");

        if (response.status === 404) {
          setError("Professor not found");
          return;
        }
        
        const data = await response.json();
        setProfessorData(data.professor);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchProfessorData();
  }, [instructorName]);

  if (error) return <p>{error}</p>;
  if (!professorData) return <p>Loading...</p>;

  // If professor data is successfully fetched, render the professor page

  return (
    <main className="professor-page container">
      <header className="professor-header">
        <h1>{professorData}</h1>
      </header>

      <DisplayAverageRating instructorName={professorData} />
      
      {/* Lots of basic placeholders until we implement these features */}
      <div className="info-sections">
        <section className="grade-distribution-graph">
          <h2>Grade Distribution Graph</h2>
          <Chart className="CS 249" instructorName={professorData} searchBy="instructor_name" />
        </section>

        <section className="pass-fail-rates">
          <h2>Pass/Fail Rates</h2>
          <p>Simplified data on pass/fail rates.</p>
        </section>
      </div>

      <SubmitRating instructorName={professorData} />

      <section className="reviews">
        <h2>Student Reviews</h2>
        <div className="review-list">
          <p>No reviews yet. Be the first to leave one!</p>
        </div>
      </section>

      <section className="leave-review">
        <h3>Leave a Review</h3>
        <textarea placeholder="Write your review here..." rows="5"></textarea>
        <button type="submit">Submit Review</button>
      </section>

    </main>
  );
}

export default ProfessorPage;
