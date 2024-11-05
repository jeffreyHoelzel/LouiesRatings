import React, { useEffect, useState } from 'react';
import StarRatings from 'react-star-ratings';
import { NUM_STARS } from './DisplayAverageRating';
import '../styles/Ratings.css';

const SubmitRating = ({instructorName}) => {
    const [ userId, setUserId ] = useState( '' );
    const [rating, setRating] = useState(0);

    // Catch Rating value
    const handleRating = (newRating, name) => {
        setRating(newRating)
    };

    const handleSubmit = async ( e ) => {
        e.preventDefault();
        if ( !userId || rating == 0 ) {
            alert( 'Please enter both user ID and rating.' );
            return;
        }

        try {
            const response = await fetch( '/service/ratings/post_rating', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_id: userId, instructor_name: instructorName, rating: rating/NUM_STARS }),
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
             <label htmlFor="userId">User ID:</label>
                <input
                    type="number"
                    id="userId"
                    value={ userId }
                    onChange={(e) => setUserId( e.target.value )}
                    required
                />
            <button type="submit" onClick={handleSubmit}>Submit Rating</button>
        </div>
    )
}

export default SubmitRating;