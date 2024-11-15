import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import '../styles/main.css';
import Chart from './Chart';
import DisplayAverageRating from './DisplayAverageRating.js';
import SubmitRating from './SubmitRating.js';

const ClassPage = () => {
  const { classId } = useParams();
  const [classData, setClassData] = useState(null);
  const [passFailData, setPassFailData] = useState({ passRate: 0, failRate: 0 });
  const [error, setError] = useState(null);

  const formatClassId = (id) => {
    if (!id) return null;
    return id.replace('-', ' ').toUpperCase();
  };

  const formattedClassId = formatClassId(classId);

  useEffect(() => {
    // Fetch general class data (grade distribution, etc.)
    const fetchClassData = async () => {
      try {
        const response = await fetch(`/service/class?classId=${encodeURIComponent(formattedClassId)}`);
        if (!response.ok) throw new Error("Class not found.");
        const data = await response.json();
        setClassData(data.class);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchClassData();
  }, [formattedClassId]);

  // Fetch pass/fail rate data
  useEffect(() => {
    if (formattedClassId) {
      const fetchPassFailRate = async () => {
        try {
          const passFailResponse = await fetch('/service/get_pass_fail_rate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ search_by: 'class_name', class_name: formattedClassId })
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
  }, [formattedClassId]);

  if (error) return <p>{error}</p>;
  if (!classData) return <p>Loading...</p>;

  // If class data is successfully fetched, render the class page
  return (
    <main className="class-page container">
      <header className="class-header">
        <h1>{formattedClassId}</h1>
        <h2>{classData.class_title || 'No Title Available'}</h2>
      </header>

      <DisplayAverageRating className={classData.code} instructorName={null} searchBy="class_name" />

      <div className="class-description">
        <p>{classData.description || 'No Description Available'}</p>
      </div>

      <div className="class-instructor">
        <h3>Primary instructor for this course:</h3>
        <p>{classData.instructor || 'No Instructor Available'}</p>
      </div>
      
      <div className="info-sections">
        <section className="grade-distribution-graph">
          <h2>Grade Distribution Graph</h2>
          <Chart className={classData.code} instructorName={null} searchBy="class_name" />
        </section>
      

        <section className="pass-fail-rates">
          <h2>Pass/Fail Rates</h2>
          <p>Pass Rate: {passFailData.passRate.toFixed(2)}%</p>
          <p>Fail Rate: {passFailData.failRate.toFixed(2)}%</p>        
        </section>
      </div>

      <section className="reviews">
        <h2>Leave a Rating</h2>
        <SubmitRating className={classData.code} instructorName={null} searchBy="class_name" />
      </section>

    </main>
  );
}

export default ClassPage;
