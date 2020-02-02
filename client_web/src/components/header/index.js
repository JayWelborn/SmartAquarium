import React, { Component } from 'react'
import { Navbar, Nav, NavItem, } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'

import { connect } from 'react-redux';


import LoginContainer from './LoginContainer'

/**
 * Make container's props equal to app's state
 *
 * @param  {object} state application state
 * @return {object}       unaltered state
 */
function mapStateToProps(state) {
  return state
}

/**
 * Page header. Displays a Bootstrap navbar and login/logout buttons
 */
function Header(props) {
  return (
    <Navbar collapseOnSelect expand='md' bg='light'>
      <LinkContainer to='/'>
        <Navbar.Brand>
          <img style={{ height: "50px" }} src="/assets/images/wordmark.svg" alt="" />
        </Navbar.Brand>
      </LinkContainer>
      <Navbar.Toggle aria-controls='basic-navbar-nav' />
      <Navbar.Collapse>
        <Nav className='mr-auto'>
          <LinkContainer exact to='/'>
            <Nav.Link eventKey={1}>
              Home
            </Nav.Link>
          </LinkContainer>
          <LinkContainer exact to='/about'>
            <Nav.Link eventKey={2}>
              About
            </Nav.Link>
          </LinkContainer>
        </Nav>
        {/* Pull Right items */}
        <Nav>
          <NavItem>
            <LoginContainer/>
          </NavItem>
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
}

export default connect(mapStateToProps)(Header)
