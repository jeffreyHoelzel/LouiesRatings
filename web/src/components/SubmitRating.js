import React, { useEffect, useState } from 'react'
import { Rating } from 'react-simple-star-rating'
import { NUM_STARS } from './DisplayAverageRating'
import '../styles/Ratings.css';

const SubmitRating = ({instructorName}) => {
    const [ userId, setUserId ] = useState( '' );
    const [rating, setRating] = useState(0)

    // Catch Rating value
    const handleRating = (rate) => {
        setRating(rate)
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
            
            // refresh page
            location.reload();

        } catch ( error ) {
            console.error( 'Error submitting rating: ', error );
        }
    };
    return (
        <div className='rating'>
            <Rating
                iconsCount={NUM_STARS}
                onClick={handleRating}
                ratingValue={rating}
                disableFillHover={true}
            />
             <label htmlFor="userId">User ID:</label>
                <input
                    type="number"
                    id="userId"
                    value={ userId }
                    onChange={(e) => setUserId( e.target.value )}
                    required
                />
            <button type="submit" onClick={handleSubmit}>Submit Review</button>
        </div>
    )
}

export default SubmitRating;