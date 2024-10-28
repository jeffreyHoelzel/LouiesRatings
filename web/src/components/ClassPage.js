import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import '../styles/ClassPageStyling.css';
import Chart from './Chart';

const ClassPage = () => {
  const { classId } = useParams();
  const [classData, setClassData] = useState(null);
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

  if (error) return <p>{error}</p>;
  if (!classData) return <p>Loading...</p>;

  // If class data is successfully fetched, render the class page
  return (
    <main className="class-page container">
      <header className="class-header">
        <h1>{formattedClassId}</h1>
        <h2>{classData.class_title || 'No Title Available'}</h2>
      </header>

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
          <Chart className={classData.code} instructorName={classData.instructor} searchBy="class_name" />
        </section>
      

        <section className="pass-fail-rates">
          <h2>Pass/Fail Rates</h2>
          <p>Simplified data on pass/fail rates for this class.</p>
        </section>
      </div>

    </main>
  );
}

export default ClassPage;
