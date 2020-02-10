import React from 'react';

import {Button, Jumbotron} from 'react-bootstrap';
import {LinkContainer} from 'react-router-bootstrap';


export default function Home(props) {
  return(
    <div className='home'>
      <Jumbotron fluid>
        <img class='logo' src='/assets/images/logo/white-on-transparent.svg' alt='Thermometer Logo'/>
        <h1>Aquatherm</h1>
        <h3>Healthy Fish Make Happy Fish</h3>
        <div className="buttons">
          <LinkContainer to='/login'>
            <Button className='call-to-action'>
              Log In
            </Button>
          </LinkContainer>
          <LinkContainer to='/register'>
            <Button className='call-to-action'>
              Register
            </Button>
          </LinkContainer>
        </div>
      </Jumbotron>
    </div>
  );
};
