import React, { useEffect, useState } from 'react';
import StarRatings from 'react-star-ratings';
import '../styles/Ratings.css';

export const NUM_STARS = 5;

const DisplayAverageRating = ({instructorName}) => {
    // initialize as 0 rating
    const [rating, setRating] = useState(0)

    // Catch Rating value
    useEffect(() => {
        fetchRating();
    }, []);

    const fetchRating = async () => {
        const response = await fetch( '/service/ratings/get_rating', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ instructor_name: instructorName }),
        });

        if ( !response.ok ) {
            console.error('Failed to fetch data:', response.statusText);
        }
        else {
            const data = await response.json();
            setRating(data.rating);
        }
    };

    return (
    <div className='rating'>
        {/* set average rating for that professor */}
        <StarRatings 
            rating={rating * NUM_STARS}
            starRatedColor="#F4B51A"
            numberOfStars={NUM_STARS}
            isSelectable={false}
            starDimension={"50px"}
            starSpacing={"4px"}
        />
        <p>{Math.round(rating * NUM_STARS * 10)/10} / {NUM_STARS}</p>
    </div>
    )
}

export default DisplayAverageRating;