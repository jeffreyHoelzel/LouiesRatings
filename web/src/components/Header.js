import { useState } from 'react';
import Search from './Search';
import Login from './Login';
import AuthenticateUser from './AuthenticateUser';

// style imports
import '../styles/login.css';


// make a header component for the website that contains the logo, search bar, and profile icon
const Header = () => {
    // set up use state for displaying login popup
    const [loginPopup, setLoginPopup] = useState(false);
    // set up authentication hook
    const {loginStatus, username} = AuthenticateUser();

    // allow login popup to be toggleable
    const toggleLoginPopup = () => {
      setLoginPopup(!loginPopup);
    //   localStorage.clear(); // FOR TESTING
    };

    const logout = () => {
        // remove status and username from localstorage
        localStorage.removeItem("status");
        localStorage.removeItem("username");
        // refresh page to reflect changes
        setTimeout(() => {
            window.location.reload();
        }, 1000);
      }

    // TODO: we should add a route to the logo to lead to main!
    return (
        <header>
            <div className="container">
                <div className="logo-box">
                    <a href="#">
                        <img src="/imgs/logo.png" alt="Logo" />
                    </a>
                </div>

                <Search/>

                <div className="profile-box">
                    <a onClick={toggleLoginPopup}>
                        <img src="imgs/profile.jpeg" alt="Profile Icon" />
                    </a>
                </div>
                <div>
                {!loginStatus ? (
                    loginPopup &&
                    <div className="login-popup" id="popup">
                        <div className="login-popup-content">
                            <span onClick={toggleLoginPopup} className="close-popup">&times;</span>
                                <Login />
                        </div>
                    </div>
                ) : (
                    loginPopup && 
                    <div className="login-popup" id="popup">
                        <div className="login-popup-content">
                            <span onClick={toggleLoginPopup} className="close-popup">&times;</span>
                            <div className="successful-login">
                                <h2>@{username}</h2>
                                <a className="sign-out" onClick={logout}>Sign out</a>
                            </div>
                        </div>
                    </div>
                )}
                </div>
            </div>
        </header>
    );
};

export default Header;
