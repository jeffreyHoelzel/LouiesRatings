import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import '../styles/ProfessorPageStyling.css';
import Chart from './Chart';
import DisplayAverageRating from './DisplayAverageRating.js';
import SubmitRating from './SubmitRating.js';

const ProfessorPage = () => {
  const { professorId } = useParams();
  const [professorData, setProfessorData] = useState(null); // Stores course data
  const [instructorName, setInstructorName] = useState(""); // Exact name from DB
  const [passFailData, setPassFailData] = useState({ passRate: 0, failRate: 0 });
  const [error, setError] = useState(null);

  // Format professorId to "Last Name, First Name" for query
  const formatName = (id) => {
    if (!id) return null;
    const [lastName, firstName] = id.split('-');
    if (!lastName || !firstName) return null;
    return `${lastName.charAt(0).toUpperCase() + lastName.slice(1)}, ${firstName.charAt(0).toUpperCase() + firstName.slice(1)}`;
  };

  const formattedInstructorName = formatName(professorId);

  // Fetch professor data
  useEffect(() => {
    const fetchProfessorData = async () => {
      try {
        // Call professor endpoint with formatted name
        const response = await fetch(`/service/professor?name=${encodeURIComponent(formattedInstructorName)}`);
        if (!response.ok) throw new Error("Professor not found.");
        
        const data = await response.json();
        setProfessorData(data.courses);
        setInstructorName(data.professor);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchProfessorData();
  }, [formattedInstructorName]);

  // Fetch pass/fail rate data
  useEffect(() => {
    if (instructorName) {
      const fetchPassFailRate = async () => {
        try {
          // Call pass/fail rate endpoint searching with instructor name
          const passFailResponse = await fetch('/service/get_pass_fail_rate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ search_by: 'instructor_name', instructor_name: instructorName })
          });

          if (passFailResponse.ok) {
            const passFailData = await passFailResponse.json();
            setPassFailData({ passRate: passFailData.pass_rate, failRate: passFailData.fail_rate });
          } else {
            console.error('Error fetching pass/fail data');
          }
        } catch (err) {
          console.error('Error fetching pass/fail data', err);
        }
      };

      fetchPassFailRate();
    }
  }, [instructorName]);

  if (error) return <p>{error}</p>;
  if (!professorData) return <p>Loading...</p>;

  return (
    <main className="professor-page container">
      <header className="professor-header">
        <h1>{instructorName}</h1>
        <hr className="professor-line"></hr>
      </header>

      <DisplayAverageRating className={null} instructorName={instructorName} searchBy="instructor_name" />
      
      <div className="info-sections">
        <section className="grade-distribution-graph">
          <h2>Grade Distribution Graph</h2>
          <Chart className={null} instructorName={instructorName} searchBy="instructor_name" />
        </section>

        <section className="pass-fail-rates">
          <h2>Pass/Fail Rates</h2>
          <p>Pass Rate: {passFailData.passRate.toFixed(2)}%</p>
          <p>Fail Rate: {passFailData.failRate.toFixed(2)}%</p>
        </section>
      </div>

      <section className="reviews">
        <h2>Leave a Rating</h2>
        <SubmitRating className={null} instructorName={instructorName} searchBy="instructor_name" />
      </section>

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
