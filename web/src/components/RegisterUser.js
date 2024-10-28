import { useState } from 'react';

const RegisterUser = () => {
  // set up states for registration data
  const [registrationData, setRegistrationData] = useState({
    username: "",
    password: "",
    email: "",
    firstName: "",
    lastName: ""
  });
  // states for message and validation (if user already exists)
  const [message, setMessage] = useState("");
  const [error, setError] = useState(false);

  // function to dynamically handle changes to registration data
  const handleChange = (e) => {
    // set name and value pair
    const {name, value} = e.target;

    // set corresponding registration data
    setRegistrationData((previousData) => ({
      ...previousData,
      [name]: value,
    }));
  }

  // handle submission of new user data
  const handleSubmit = async (e) => {
    // prevent page from reloading
    e.preventDefault();

    // try to get response from backend by requesting new user verification in json format
    try {
      const response = await fetch('/service/register', {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          "username": registrationData.username,
          "password": registrationData.password,
          "email": registrationData.email,
          "firstName": registrationData.firstName,
          "lastName": registrationData.lastName
        })
      });

      // await json response
      const data = await response.json();

      // check if response ok and then add to localstorage for automatic login
      if (response.ok) {
        localStorage.setItem("status", "true");
        localStorage.setItem("username", registrationData.username);
      } else {
        setMessage(data.message || "Error logging in.");
      }

      // set message and validation to confirm or deny login
      setMessage(data.message);
      setError(data.error);

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

  return (
    <div>
      <form action="" className="form-container">
        <h2>New account</h2>
        <label for="firstName"><b>First name</b></label>
        <input type="text" placeholder="Enter first name" name="firstName" onChange={handleChange} required />

        <label for="lastName"><b>Last name</b></label>
        <input type="text" placeholder="Enter last name" name="lastName" onChange={handleChange} required />

        <label for="email"><b>Email</b></label>
        <input type="email" placeholder="Enter email" name="email" onChange={handleChange} required />

        <label for="username"><b>Username</b></label>
        <input type="text" placeholder="Enter username" name="username" onChange={handleChange} required />

        <label for="password"><b>Password</b></label>
        <input type="password" placeholder="Enter password" name="password" onChange={handleChange} required />

        <div className="option-container">
          <button type="submit" className="sign-up-btn" onClick={handleSubmit}>Sign up</button>
        </div>
        {error && <span style={{color: 'red'}}>{message}</span>}
      </form>
    </div>
  );
}

export default RegisterUser;