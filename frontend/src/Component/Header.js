import React from 'react';
import './Header.css';
import logoImage from '/github/dj_library/frontend/src/Component/picture/dj_logo_big.png'; // ロゴ画像のパスを指定してください



function Header() {
  return (
     <header className="header">
    <div className="header-left">
        <img src={logoImage} alt="Logo" className="logo-image rotating-logo" />
        <h1 className="title">STUDIO</h1>
    </div>
    <div className="header-right">
        <div className="menu-icon">
          <div className="menu-line"></div>
          <div className="menu-line"></div>
          <div className="menu-line"></div>
        </div>
      </div>
    </header>

  )
}


export default Header;