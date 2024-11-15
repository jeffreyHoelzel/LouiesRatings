import {useState, useEffect} from 'react';
import '../styles/main.css';
import AuthenticateUser from './AuthenticateUser';

const Comment = ({reviewType}) => {
  const [comments, setComments] = useState([]);
  const {loginStatus, username} = AuthenticateUser();
  const [content, setContent] = useState('');

  // fix bug where comments get duplicated in fetch (not displayed more than once but behind the scenes)
  const setUniqueComments = (unfilteredComments) => {
    if (!unfilteredComments) return null;
    const uniqueComments = unfilteredComments.filter((comment, index, self) =>
      index === self.findIndex((c) => c.id === comment.id)
    );
    setComments(uniqueComments);
  }

  // get all comments for a specific instructor or course page
  useEffect(() => {
    if (!reviewType) return;

    const fetchComments = async () => {
      try {
        const response = await fetch(`/service/comment/load_comments?review_type=${encodeURIComponent(reviewType)}`);

        if (!response.ok) {
          throw new Error('Fetching comments failed.');
        }

        const data = await response.json();
        setUniqueComments(data);
      } catch (e) {
        console.error('Error fetching comments:', e);
      }
    }

    fetchComments();
  }, [reviewType]);

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
        body: JSON.stringify({"username": username, "reviewType": reviewType, "content": content})
      });

      if (!response.ok) {
        console.error('Submitting new comment failed.');
      }

      // comment processed, now display it
      setComments((prevComments) => [...prevComments, {username, content}]); // adding normally and then filtering for duplicates later
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
          {comments.length ? comments.map((comment) => (
            <li key={comment.id} className="comment">
              <strong>@{comment.username}</strong> {comment.content}
            </li>
          )) : <p>Be the first to leave a review...</p>}
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