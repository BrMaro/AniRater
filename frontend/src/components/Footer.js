import React from 'react';

const Footer = () => {
    return (
        <footer style={footerStyle}>
            <p>&copy; 2024 Anime Guessing Game. All rights reserved.</p>
            <p>
                Follow us on 
                <a href="https://twitter.com/" style={linkStyle}> Twitter</a>, 
                <a href="https://facebook.com/" style={linkStyle}> Facebook</a>, and 
                <a href="https://instagram.com/" style={linkStyle}> Instagram</a>.
            </p>
        </footer>
    );
};

const footerStyle = {
    backgroundColor: '#2C2C2C', 
    color: '#FFF',
    textAlign: 'center',
    padding: '10px',
    position: 'fixed',
    left: '0',
    bottom: '0',
    width: '100%',
};

const linkStyle = {
    marginLeft: '5px',
    color: '#FFF',
    textDecoration: 'none',
};

export default Footer;
