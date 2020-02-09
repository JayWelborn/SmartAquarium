import React, {Component} from 'react'
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
class Header extends Component {
  render() {
    let navLinks;
    if (this.props.userLoggedIn) {
      navLinks = [
        <LinkContainer key={1} exact to='/thermometers'>
          <Nav.Link active={false}>
            My Thermometers
          </Nav.Link>
        </LinkContainer>,
        <LinkContainer key={2} exact to='/new-thermometer'>
          <Nav.Link active={false}>
            New Thermometers
          </Nav.Link>
        </LinkContainer>
      ];
    } else {
      navLinks = [
        <LinkContainer key={1} exact to='/login'>
          <Nav.Link active={false}>
            Log In
          </Nav.Link>
        </LinkContainer>,
        <LinkContainer key={2} exact to='/register'>
          <Nav.Link active={false}>
            Register
          </Nav.Link>
        </LinkContainer>
      ];
    }

    return (
      <Navbar collapseOnSelect expand='md' bg='light'>
        <LinkContainer exact to='/'>
          <Nav.Link active={false}>
            <Navbar.Brand>
              <img style={{ height: "40px" }} src="/assets/images/wordmark.svg" alt="" />
            </Navbar.Brand>
          </Nav.Link>
        </LinkContainer>
        <Navbar.Toggle aria-controls='basic-navbar-nav' />
        <Navbar.Collapse>
          <Nav className='mr-auto'>
            <LinkContainer exact to='/'>
              <Nav.Link active={false}>
                Home
              </Nav.Link>
            </LinkContainer>
            <LinkContainer exact to='/about'>
              <Nav.Link active={false}>
                About
              </Nav.Link>
            </LinkContainer>
            {navLinks}
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
}
export default connect(mapStateToProps)(Header)
