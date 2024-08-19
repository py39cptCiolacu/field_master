import React from 'react';
import { MDBNavbar, MDBContainer, MDBNavbarBrand, MDBNavbarNav, MDBNavbarItem, MDBNavbarLink, MDBNavbarToggler, MDBIcon, MDBCollapse } from 'mdb-react-ui-kit';
import './Navbar.css';
import logo from '../assets/logo.png';  // Importă logo-ul

export default function Navbar({ isAuthenticated, username, setIsAuthenticated, setUsername }) {
  const [showNav, setShowNav] = React.useState(false);

  return (
    <MDBNavbar expand='lg' light className='custom-navbar'>
      <MDBContainer fluid>
        <MDBNavbarBrand href='/'>
          {/* Adăugarea logo-ului */}
          <img src={logo} alt="Logo" className="logo-image" />
          FieldMaster
        </MDBNavbarBrand>
        <MDBNavbarToggler
          type='button'
          data-target='#navbarToggleExternalContent'
          aria-controls='navbarToggleExternalContent'
          aria-expanded='false'
          aria-label='Toggle navigation'
          onClick={() => setShowNav(!showNav)}
        >
          <MDBIcon icon='bars' fas />
        </MDBNavbarToggler>
        <MDBCollapse navbar show={showNav}>
          <MDBNavbarNav right fullWidth={false} className='mb-2 mb-lg-0'>
            <MDBNavbarItem className='custom-nav-link'>
              <MDBNavbarLink href='/' style={{color:'white'}}>Home</MDBNavbarLink>
            </MDBNavbarItem>
            {isAuthenticated ? (
              <>
                <MDBNavbarItem className='custom-nav-link'>
                  <MDBNavbarLink href='/user_profile' style={{color:'white'}}>User Profile</MDBNavbarLink>
                </MDBNavbarItem>
                <MDBNavbarItem className='custom-nav-link'>
                  <MDBNavbarLink href='/map' style={{color:'white'}}>Add Land</MDBNavbarLink>
                </MDBNavbarItem>
                <MDBNavbarItem className='custom-nav-link'>
                  <MDBNavbarLink href='/analysis' style={{color:'white'}}>Get Suggestion</MDBNavbarLink>
                </MDBNavbarItem>
                <MDBNavbarItem className='custom-nav-link'>
                  <MDBNavbarLink href='/logout' style={{color:'white'}}>Log Out</MDBNavbarLink>
                </MDBNavbarItem>
              </>
            ) : (
              <>
                <MDBNavbarItem className='custom-nav-link'>
                  <MDBNavbarLink href='/login' style={{color:'white'}}>Login</MDBNavbarLink>
                </MDBNavbarItem>
                <MDBNavbarItem className='custom-nav-link'>
                  <MDBNavbarLink href='/register' style={{color:'white'}}>Register</MDBNavbarLink>
                </MDBNavbarItem>
              </>
            )}
          </MDBNavbarNav>
        </MDBCollapse>

        <div className='d-flex ms-auto align-items-center'>
          <span className='navbar-text' style={{color:'white'}}>
            {isAuthenticated ? username : 'Guest'}
          </span>
        </div>
      </MDBContainer>
    </MDBNavbar>
  );
}
