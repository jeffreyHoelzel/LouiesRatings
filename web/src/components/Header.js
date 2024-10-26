import { useState } from 'react';
import Search from './Search';
import Login from './Login';
import Authenticate from './Authenticate';


// make a header component for the website that contains the logo, search bar, and profile icon
const Header = () => {
    // set up use state for displaying login popup
    const [loginPopup, setLoginPopup] = useState(false);
    // set up authentication hook
    const {loginStatus, username} = Authenticate();

    // allow popup to be toggleable
    const toggleLoginPopup = () => {
      setLoginPopup(!loginPopup);
    };

    // TODO: we should add a route to the logo to lead to main!
    return (
        <header>
            <div className="container">
                <div className="logo-box">
                    <a href="#">
                        <img src="imgs/logo.png" alt="Logo" />
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
                                    <p>*name of user*</p>
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
