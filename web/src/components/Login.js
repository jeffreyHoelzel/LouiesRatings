// style imports
import '../styles/login.css';
import '../styles/homepage.css';
import { useState } from 'react';

const Login = () => {
  // set up use states for username, password, response message
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [valid, setValid] = useState(false);

  // handle user submitting username and password
  const handleSubmit = async (e) => {
    e.preventDefault();

    // try to get response from backend
    try {
      const response = await fetch('/service/login', {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({"username": username, "password": password})
      });

      const data = await response.json();
      console.log(data)
      setMessage(data.message);
      setValid(data.exists)
    } catch (error) {
      console.log("Error:", error);
      setMessage("Username and password pair does not exist.");
    }
  }
  // return boolean from backend if username, password kv pair exists
  // if true, log in and display that they are logged in, otherwise, display error message

  return (
    <div>
      <form action="" className="form-container">
        <h2>Login</h2>
        <label for="username"><b>Username</b></label>
        <input type="text" placeholder="Enter username" name="username" onChange={(e) => setUsername(e.target.value)} required />
        <label for="password"><b>Password</b></label>
        <input type="password" placeholder="Enter password" name="password" onChange={(e) => setPassword(e.target.value)} required />
        <div className="option-container">
          <button type="submit" className="login-btn" onClick={handleSubmit}>Login</button>
          <a className="new-account" id="create-new-account">Register</a>
        </div>
      </form>
    </div>
  );
}

export default Login;