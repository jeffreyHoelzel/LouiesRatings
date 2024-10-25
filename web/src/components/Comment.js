import React, { useState, useEffect } from 'react';

const Comments = () => {
    const [ comments, setComments ] = useState([]);
    const [ userId, setUserId ] = useState( '' );
    const [ content, setContent ] = useState( '' ); // Fixed variable name here

    useEffect(() => {
        fetchComments();
    }, []);

    const fetchComments = async () => {
        try {
            const response = await fetch( '/comments' );
            if ( !response.ok ) {
                throw new Error( 'Network response was not ok' );
            } // Added missing closing brace here
            const data = await response.json();
            setComments(data);
        } catch ( error ) {
            console.error( 'Error fetching comments: ', error );
        }
    };

    const handleSubmit = async ( e ) => {
        e.preventDefault(); // Corrected the method name here
        if ( !userId || !content ) { // Corrected variable name here
            alert( 'Please enter both user ID and comment content.' );
            return;
        }

        try {
            const response = await fetch( '/comments', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }, // Added missing comma here
                body: JSON.stringify({ user_id: userId, content: content }),
            });

            if ( !response.ok ) {
                throw new Error( 'Network response was not ok' );
            }

            setUserId('');
            setContent('');
            fetchComments();
        } catch ( error ) {
            console.error( 'Error submitting comments: ', error );
        }
    };

    // The return statement must be inside the Comments component
    return (
        <div>
            <h2>Comments</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="userId">User ID:</label>
                    <input
                        type="number"
                        id="userId"
                        value={ userId }
                        onChange={(e) => setUserId( e.target.value )}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="content">Comment:</label>
                    <textarea
                        id="content"
                        value={ content }
                        onChange={(e) => setContent( e.target.value )}
                        required
                    />
                </div>
                <button type="submit">Submit Comment</button>
            </form>
            <h3>Comment List</h3>
            <ul>
                {comments.map(( comment ) => (
                    <li key={ comment.id }>
                        <strong>User { comment.user_id }:</strong> {comment.content} <em>({new Date(comment.timestamp).toLocaleString()})</em>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Comments;
