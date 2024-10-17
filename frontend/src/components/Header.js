import React from "react";
import { Link } from "react-router-dom";

const Header = ({ isAuthenticated }) => {
  return (
    <header>
      <h1>
        Anim<span>Guess</span>
      </h1>

      {isAuthenticated ? (
        <div>
          {/* favicon for profile */}
          <Link to="/profile">Profile</Link>
        </div>
      ) : (
        <div>
          <Link to="/login">
            <button className="login-btn">Log In</button>
          </Link>

          <Link to="/register">
            <button className="register-btn">Register</button>
          </Link>
        </div>
      )}
    </header>
  );
};

export default Header;
