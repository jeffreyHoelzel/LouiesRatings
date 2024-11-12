import React, { useEffect, useState } from 'react';
import StarRatings from 'react-star-ratings';
import { NUM_STARS } from './DisplayAverageRating';
import AuthenticateUser from './AuthenticateUser';
import '../styles/Ratings.css';

const SubmitRating = ({className, instructorName, searchBy}) => {
    const {loginStatus, username} = AuthenticateUser();
    const [rating, setRating] = useState(0);

    // Catch Rating value
    const handleRating = (newRating, name) => {
        setRating(newRating)
    };

    const handleSubmit = async ( e ) => {
        e.preventDefault();
        if (!loginStatus) {
            alert('Please log in to submit a rating.');
            return;
        }

        if (rating === 0) {
            alert('Choose a rating to submit.');
            return;
        }

        try {
            const response = await fetch( '/service/ratings/post_rating', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username: username, class_name: className, instructor_name: instructorName, search_by: searchBy, rating: rating/NUM_STARS }),
            });

            if ( !response.ok ) {
                throw new Error( 'Network response was not ok' );
            }
            
            const data = await response.json();

            // let user know whether message was added or overwritten
            // TODO: make this a brief pop up message
            window.alert(data.message);

            // refresh page
            window.location.reload();

        } catch ( error ) {
            console.error( 'Error submitting rating: ', error );
        }
    };
    return (
        <div className='rating'>
            <StarRatings
                numberOfStars={NUM_STARS}
                changeRating={handleRating}
                rating={rating}
                starRatedColor={"rgb(244,181,26)"}
                starHoverColor={"rgb(244,181,26)"}
                starDimension={"25px"}
                starSpacing={"2px"}
            />
            <button type="submit" onClick={handleSubmit}>Submit Rating</button>
        </div>
    )
}

export default SubmitRating;