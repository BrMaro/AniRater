import React from "react";
import Header from './Header';
import Footer from './Footer';

const BaseLayout = ({ children, isAuthenticated }) => { // Fixed prop name typo
  return (
    <div className="base-layout">
      <Header isAuthenticated={isAuthenticated} />
      <main className="main-content">
        {children}
      </main>
      <Footer />
    </div>
  );
};

export default BaseLayout;