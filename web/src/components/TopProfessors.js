import React, { useState, useEffect } from 'react';
import StarRatings from 'react-star-ratings';
import '../styles/main.css';
import { NUM_STARS } from './DisplayAverageRating';

const TopProfessors = () => {
  const [professors, setProfessors] = useState([]);

  // Fetch top professors from the API
  useEffect(() => {
    const fetchTopProfessors = async () => {
      try {
        const response = await fetch('/service/top_professors'); // Ensure this matches the route in your backend <-- Thanks Chat!

        // Check if the response is okay (status 2xx)
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const text = await response.text();

        // Try to parse the text as JSON
        const data = JSON.parse(text);
        setProfessors(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchTopProfessors();
  }, []);

  // Split professors into three columns
  const col1 = professors?.slice(0, Math.ceil(professors.length / 3));
  const col2 = professors?.slice(
    Math.ceil(professors.length / 3),
    Math.ceil((professors.length / 3) * 2)
  );
  const col3 = professors?.slice(
    Math.ceil((professors.length / 3) * 2),
    professors.length
  );

  return (
    <div className="best-rated-box">
      <h2>Top Rated Professors</h2>

      <div className="sections-container">
        {/* Column 1 */}
        <div className="section">
          {col1.map((professor, index) => (
            <div key={index} className="professor">
              <h2>{professor.instructor_name}</h2>
              <div className="rating2">
                <StarRatings 
                  rating={professor.avg_rating * NUM_STARS}
                  starRatedColor="#F4B51A"
                  numberOfStars={NUM_STARS}
                  isSelectable={false}
                  starDimension={"30px"}
                  starSpacing={"4px"}
                />
                <p>{professor.avg_rating?.toFixed(2) * NUM_STARS} / {NUM_STARS}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Column 2 */}
        <div className="section">
          {col2.map((professor, index) => (
            <div key={index} className="professor">
              <h2>{professor.instructor_name}</h2>
              <div className="rating2">
                <StarRatings 
                  rating={professor.avg_rating * NUM_STARS}
                  starRatedColor="#F4B51A"
                  numberOfStars={NUM_STARS}
                  isSelectable={false}
                  starDimension={"30px"}
                  starSpacing={"4px"}
                />
                <p>{professor.avg_rating?.toFixed(2) * NUM_STARS} / {NUM_STARS}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Column 3 */}
        <div className="section">
          {col3.map((professor, index) => (
            <div key={index} className="professor">
              <h2>{professor.instructor_name}</h2>
              <div className="rating2">
                <StarRatings 
                  rating={professor.avg_rating * NUM_STARS}
                  starRatedColor="#F4B51A"
                  numberOfStars={NUM_STARS}
                  isSelectable={false}
                  starDimension={"30px"}
                  starSpacing={"4px"}
                />
                <p>{professor.avg_rating?.toFixed(2) * NUM_STARS} / {NUM_STARS}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
  };

  export default TopProfessors;