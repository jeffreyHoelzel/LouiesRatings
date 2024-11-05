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
            const response = await fetch( 'service/comments' );

            if ( !response.ok ) {
                throw new Error( 'Network response was not ok' );
            }

            const data = await response.json();
            setComments(data);

        } catch ( error ) {
            console.error( 'Error fetching comments: ', error );
        }
    };

    const handleSubmit = async ( e ) => {
        e.preventDefault(); // Corrected the method name here <- Chat is that you?!?!!?
        if ( !userId || !content ) { // Corrected variable name here
            alert( 'Please enter both user ID and comment content.' );
            return;
        }

        try {
            const response = await fetch( 'service/comments', {
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

    const handleDeleteComment = async ( id ) => {
        try {
            const response = await fetch( `service/comments/delete?id=${encodeURIComponent(id)}`, {
                method: 'POST',
            });

            if ( !response.ok ) {
                throw new Error( 'Network response was not ok' );
            }

            fetchComments();

        } catch ( error ) {
            console.error( 'Error deleting comment: ', error );
        }
    }

    // The return statement must be inside the Comments component
    return (
        <div>
            <h2>Comments</h2>
            <form onSubmit={handleSubmit}>
                    <label htmlFor="userId">User ID:</label>
                    <input
                        type="number"
                        id="userId"
                        value={ userId }
                        onChange={(e) => setUserId( e.target.value )}
                        required
                    />
                    <label htmlFor="content">Comment:</label>
                    <textarea
                        id="content"
                        value={ content }
                        onChange={(e) => setContent( e.target.value )}
                        required
                    />
                <button id="submit" type="submit">Submit Comment</button>
            </form>
            <h3>Comment List</h3>
            <ul id="comment-list">
                {comments.map(( comment ) => (
                    <li className="comments" id={ `${comment.user_id}` } key={comment.id}>
                        <strong>User { comment.user_id }:</strong> {comment.content} <em>({new Date(comment.timestamp).toLocaleString()})</em>
                        <button class="trash-can" onClick={() => handleDeleteComment(comment.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Comments;
