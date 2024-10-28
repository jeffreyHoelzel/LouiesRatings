import { useState } from 'react';

// style imports
import '../styles/login.css';
import '../styles/homepage.css';
import RegisterUser from './RegisterUser';

const Login = () => {
  // set up use states for username, password, response message, and validations
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [valid, setValid] = useState(false);

  // allow user to register instead of logging in
  const [registrationPopup, setRegistrationPopup] = useState(false);

  // toggle popup as needed
  const toggleRegistrationPopup = () => {
    setRegistrationPopup(!registrationPopup);
  }

  // handle user submitting username and password
  const handleSubmit = async (e) => {
    // prevent page from reloading
    e.preventDefault();

    // try to get response from backend by requesting login verification in json format
    try {
      const response = await fetch('/service/login', {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({"username": username, "password": password})
      });

      // await json response
      const data = await response.json();

      // check if response ok and then add to localstorage
      if (response.ok) {
        localStorage.setItem("status", "true");
        localStorage.setItem("username", username);
      } else {
        setMessage(data.message || "Error logging in.");
      }

      // set message and validation to confirm or deny login
      setMessage(data.message);
      setValid(data.exists);

    } catch (error) {
      console.log("Error:", error);
      setMessage("Error logging in.");
    }

    // check if status true
    if (localStorage.getItem("status") === "true") {
      // refresh page to reflect correct user
      setTimeout(() => {
        window.location.reload();
      }, 1000);
    }
  }

  // render normal login on load and if user has input wrong username or password
  return (
    <div>
      {!registrationPopup ? (
        <form action="" className="form-container">
          <h2>Login</h2>
          <label for="username"><b>Username</b></label>
          <input type="text" placeholder="Enter username" name="username" onChange={(e) => setUsername(e.target.value)} required />
          <label for="password"><b>Password</b></label>
          <input type="password" placeholder="Enter password" name="password" onChange={(e) => setPassword(e.target.value)} required />
          <div className="option-container">
            <button type="submit" className="login-btn" onClick={handleSubmit}>Login</button>
            <a className="new-account" id="create-new-account" onClick={toggleRegistrationPopup}>Register</a>
          </div>
          {!valid && <span style={{color: 'red'}}>{message}</span>}
        </form>
      ) : (
        < RegisterUser />
      )}
    </div>
  );
}

export default Login;