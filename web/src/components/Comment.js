import {useState, useEffect} from 'react';
import '../styles/Comment.css';
import AuthenticateUser from './AuthenticateUser';

const Comment = ({instructorName}) => {
  const [comments, setComments] = useState([]);
  const {loginStatus, username} = AuthenticateUser();
  const [content, setContent] = useState('');

  // get all comments for a specific instructor's page
  useEffect(() => {
    if (!instructorName) return;

    const fetchComments = async () => {
      try {
        const response = await fetch(`/service/comment/load_comments?instructorName=${encodeURIComponent(instructorName)}`);

        if (!response.ok) {
          throw new Error('Fetching comments failed.');
        }

        const data = await response.json();
        setComments(data);
      } catch (e) {
        console.error('Error fetching comments:', e);
      }
    }

    fetchComments();
  }, [instructorName]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // check if user logged in
    if (!loginStatus) {
      alert('Please log in to submit a rating.');
      return;
    }

    // check if user typed anything
    if (!content) {
      alert('Enter a comment to submit.');
      return;
    }

    // submit a comment
    try {
      const response = await fetch('/service/comment/post_comment', {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({"username": username, "instructorName": instructorName, "content": content})
      });

      if (!response.ok) {
        console.error('Submitting new comment failed.');
      }

      // comment processed, now display it
      setComments((prevComments) => [...prevComments, {username, content}]);
      setContent('');
    } catch (e) {
      console.error('Error submitting comment:', e);
    }
  }

  return (
    <div className="reviews-container">
      <section className="reviews">
        <h2>Student Reviews</h2>
        <div className="review-list">
          <ul>
            {comments.map((comment) => (
              <li key={comment.id} className="comment">
                <strong>@{comment.username}</strong> {comment.content}
              </li>
            ))}
          </ul>
        </div>
      </section>
      <section className="reviews">
        <h2>Leave a Review</h2>
        <div className="new-review">
          <textarea value={content} onChange={(e) => setContent(e.target.value)} placeholder="Write your review here..." rows="5"></textarea>
          <button type="submit" onClick={handleSubmit}>Submit Review</button>
        </div>
      </section>
    </div>
  );
}

export default Comment;