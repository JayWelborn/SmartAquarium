import React, { Component } from 'react'
import { Navbar, Nav, NavItem, } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { LinkContainer } from 'react-router-bootstrap'

import LoginContainer from './LoginContainer'

/**
 * Page header. Displays a Bootstrap navbar and login/logout buttons
 */
export default class Header extends Component {
  render() {
    return (
      <Navbar fluid collapseOnSelect bg='light'>
        <LinkContainer to='/'>
          <Navbar.Brand>
            <img style={{ height: "50px" }} src="/assets/images/wordmark.svg" alt="" />
          </Navbar.Brand>
        </LinkContainer>
        <Navbar.Collapse>
          <Nav variant='tabs'>
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
        </Navbar.Collapse>
      </Navbar>
    );
  }
}
