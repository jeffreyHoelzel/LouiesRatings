import {useState, useEffect} from 'react';

const Comment = ({instructorName}) => {
  const [ comments, setComments ] = useState([]);
  const {loginStatus, username} = AuthenticateUser();
  const [ content, setContent ] = useState('');

  // Format professorId to "Last Name, First Name" for query --> thank you Will for this function!!!
  const formatName = (id) => {
    if (!id) return null;
    const [lastName, firstName] = id.split('-');
    if (!lastName || !firstName) return null;
    return `${lastName.charAt(0).toUpperCase() + lastName.slice(1)}, ${firstName.charAt(0).toUpperCase() + firstName.slice(1)}`;
  };

  const formattedInstructorName = formatName(instructor);

  // get all comments for a specific instructor's page
  useEffect(() => {
    const fetchComments = async () => {
      try {
        const response = await fetch(`service/comment/load_comments?instructor=${encodeURIComponent(formattedInstructorName)}`);

        if (!response.ok) {
          throw new Error('Fetching comments failed.');
        }

        const data = await response.json();
        setComments(data.comments);
      } catch (e) {
        console.error('Error fetching comments: ', e);
      }
    }

    fetchComments();
  }, []);

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
      const response = await fetch('service/comment/post_comment', {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({"username": username, "instructor": instructor, "content": content})
      });

      if (!response.ok) {
        console.error('Submitting new comment failed.');
      }

      // comment processed, now display it
      window.location.reload();
    } catch (e) {
      console.error('Error submitting comment: ', e);
    }
  }

  return (
    <div>
      <h2>Student Reviews</h2>
      <div className="review-list">
        <ul>
          {comments.map((comment) => {
            <li className="comment">
              <strong>@{username}</strong> {comment}
            </li>
          })}
        </ul>
      </div>
      <h2>Leave a Review</h2>
      <div className="new-review">
        <textarea value={content} onChange={(e) => setContent(e.target.value)} placeholder="Write your review here..." rows="5"></textarea>
        <button type="submit" onClick={handleSubmit}>Submit Review</button>
      </div>
    </div>
  );
}

export default Comment;