import React, { useState, useEffect } from 'react';

const Comment = () => {
  const [comments, setComments] = useState([]);
  const [userId, setUserId] = useState(1); // Placeholder for user ID
  const [content, setContent] = useState('');
  const [message, setMessage] = useState('');

  const backendUrl = "service/comments";

  // Fetch comments when the component mounts
  useEffect(() => {
    fetchComments();
  }, []);

  const fetchComments = () => {
    fetch(backendUrl)
      .then(res => res.json())
      .then(data => {
        setComments(data);
        setMessage('');
      })
      .catch(err => {
        console.error(err);
        setMessage("Failed to load comments.");
      });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Prepare the comment data
    const newComment = {
      user_id: userId,
      content: content
    };

    // Send the new comment to the backend
    fetch(backendUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(newComment)
    })
      .then(res => {
        if (!res.ok) {
          throw new Error("Failed to submit comment");
        }
        return res.json();
      })
      .then(data => {
        setComments(prev => [...prev, data.comment]); // Update the comments list immediately
        setContent(''); // Clear the input field
        setMessage(data.message); // Set success message
      })
      .catch(err => {
        console.error(err);
        setMessage("Failed to submit comment.");
      });
  };

  return (
    <div>
      <h2>Comments</h2>
      {message && <p>{message}</p>}
      <form onSubmit={handleSubmit}>
        <textarea 
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Leave a comment..."
          required
        />
        <button type="submit">Submit</button>
      </form>
      <ul>
        {comments.map(comment => (
          <li key={comment.id}>
            <p><strong>User {comment.user_id}:</strong> {comment.content}</p>
            <p>{new Date(comment.timestamp).toLocaleString()}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Comment;
