import { useState } from 'react';
import Search from './Search';
import { Link } from 'react-router-dom';
import Login from './Login';
import AuthenticateUser from './AuthenticateUser';

// style imports
import '../styles/main.css';


// make a header component for the website that contains the logo, search bar, and profile icon
const Header = () => {
    // set up use state for displaying login popup
    const [loginPopup, setLoginPopup] = useState(false);
    // set up authentication hook
    const {loginStatus, username} = AuthenticateUser();

    // allow login popup to be toggleable
    const toggleLoginPopup = () => {
      setLoginPopup(!loginPopup);
    };

    const logout = () => {
        // remove status and username from localstorage
        localStorage.removeItem("status");
        localStorage.removeItem("username");
        // refresh page to reflect changes
        setTimeout(() => {
            window.location.reload();
        }, 1000);
      };

    const directToHomepage = () => {
        // direct to homepage
        window.location.href = '/';

        // reload page
        window.reload();
    }

    return (
        <header>
            <div className="container">
                <div className="logo-box">
                    <img src="/imgs/LouiesRatingsLogo.png" alt="Logo" />
                </div>

                <div className='home-button'>
                    <button onClick={directToHomepage}>
                        <img src="/imgs/home.png" alt="Home Icon"/>
                    </button>
                </div>

                <Search/>

                <div className="profile-box">
                    <a className="popup-form" onClick={toggleLoginPopup}>
                        <img src="/imgs/profile.jpeg" alt="Profile Icon" />
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
                                <h2 className="username">@{username}</h2>
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
