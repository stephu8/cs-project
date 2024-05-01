import React from 'react';
import './header.css'; // Assuming you have a CSS file for styling

const Header = () => {
  return (
    <div className="header-container">
      <div className="logo">
        <img
          src="rutgers-img.png"
          alt="Rutgers Logo"
          className="logo-img"
        />
      </div>
    </div>
  );
};

export default Header;