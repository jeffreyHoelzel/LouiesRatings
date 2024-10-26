import { useState, useEffect } from "react";

const Authenticate = () => {
  // set up states for username and logged in
  const [loginStatus, setLoginStatus] = useState(false);
  const [username, setUsername] = useState("");

  useEffect(() => {
    // get login status and username if they exist
    const storedLoginStatus = localStorage.getItem("status");
    const storedUsername = localStorage.getItem("username");

    // check if login status is true
    if (storedLoginStatus === "true") {
      // set status to true as bool and username
      setLoginStatus(true);
      setUsername(storedUsername);
    } else {
      // set status to false as bool and empty string to username
      setLoginStatus(false);
      setUsername("");
    }
  });

  return {loginStatus, username};
}

export default Authenticate;