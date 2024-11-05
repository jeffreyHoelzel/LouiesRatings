import React, { useEffect, useState } from 'react'
import { Rating } from 'react-simple-star-rating'

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
        <Rating 
            initialValue={rating * NUM_STARS} 
            readonly={true} 
            allowFraction={true}
            iconsCount={NUM_STARS}
        />
    </div>
    )
}

export default DisplayAverageRating;