import React from 'react';
import Search from './Search';
import { Link } from 'react-router-dom';

// make a header component for the website that contains the logo, search bar, and profile icon
const Header = () => {

    // TODO: we should add a route to the logo to lead to main!
    return (
        <header>
            <div className="container">
                <div className="logo-box">
                    <Link to="/">
                        <img src="/imgs/logo.png" alt="Logo" />
                    </Link>
                </div>

                <Search/>

                <div className="profile-box">
                    <a href="#">
                        <img src="/imgs/profile.jpeg" alt="Profile Icon" />
                    </a>
                </div>
            </div>
        </header>
    );
};

export default Header;
