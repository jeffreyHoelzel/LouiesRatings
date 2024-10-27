import React, { useState, useEffect } from 'react';

const Comment = () => {
  const [commentsList, setCommentsList] = useState([]); // Renamed from comments to commentsList
  const [currentUserId, setCurrentUserId] = useState(1); // Renamed from userId to currentUserId
  const [commentContent, setCommentContent] = useState(''); // Renamed from content to commentContent
  const [statusMessage, setStatusMessage] = useState(''); // Renamed from message to statusMessage

  const backendUrl = "service/comments";

  // Fetch comments when the component mounts
  useEffect(() => {
    fetchComments();
  }, []);

  const fetchComments = () => {
    fetch(backendUrl)
      .then(response => response.json())
      .then(data => {
        setCommentsList(data);
        setStatusMessage(''); // Reset message after fetching comments
      })
      .catch(error => {
        console.error(error);
        setStatusMessage("Failed to load comments.");
      });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    
    // Prepare the comment data
    const newCommentData = {
      user_id: currentUserId,
      content: commentContent
    };

    // Send the new comment to the backend
    fetch(backendUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(newCommentData)
    })
      .then(response => {
        if (!response.ok) {
          throw new Error("Failed to submit comment");
        }
        return response.json();
      })
      .then(data => {
        setCommentsList(prevComments => [...prevComments, data.comment]); // Update the comments list
        setCommentContent(''); // Clear the input field
        setStatusMessage(data.message); // Set success message
      })
      .catch(error => {
        console.error(error);
        setStatusMessage("Failed to submit comment.");
      });
  };

  return (
    <div>
      <h2>Comments</h2>
      {statusMessage && <p>{statusMessage}</p>}
      <form onSubmit={handleSubmit}>
        <textarea 
          value={commentContent}
          onChange={(event) => setCommentContent(event.target.value)}
          placeholder="Leave a comment..."
          required
        />
        <button type="submit">Submit</button>
      </form>
      <ul>
        {commentsList.map(comment => (
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
