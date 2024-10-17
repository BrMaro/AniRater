import React from "react";
import Header from './Header';
import Footer from './Footer';

const BaseLayout = ({ children, isAunthenticated}) => {
  return (
    <div>
      <Header isAuthenticated={isAunthenticated}/>
      <main>
        {children} 
      </main>
      <Footer />
    </div>
  );
};

export default BaseLayout;