import React from 'react';

import {Button, Jumbotron} from 'react-bootstrap';
import {LinkContainer} from 'react-router-bootstrap';

import Panel from './panel';


export default function Home(props) {
  const infoPanels = [
    {
      'iconUrl': '/assets/images/originals/Fish_Dark.svg',
      'header': 'Fish',
      'text': '<p>Your aquarium probably has fish in it. Do you want to make sure your fish are ' +
              'comfortable? Of course you do.</p><p>Fish love water at just the right temperature. ' +
              'You wouldn\'t bathe in a boiling tar pit, so don\'t make your fish</p>'
    },
    {
      'iconUrl': '/assets/images/originals/Water_Medium.svg',
      'header': 'Water',
      'text': '<p>Your aquarium is almost definitely full of water. To check the temperature of ' +
              'water, you have to have a thermometer.</p><p>You might already have one, but how do ' +
              'you know if your wtaer is just right while you\'re away from home?</p>'
    },
    {
      'iconUrl': '/assets/images/originals/SmartPhone_Light.svg',
      'header': 'Phone',
      'text': '<p>Now, with this fancy thermometer, you can check your aquarium\'s temperature ' +
              'on your phone. How does it work? You don\'t care.</p><p>That\'s why I\'m here. ' +
              'Don\'t worry about it. I got you. Building cool tech is my thing.</p>'
    },
  ];
  let panelComponents = infoPanels.map((panel, index) =>
    <Panel url={panel.iconUrl} header={panel.header} text={panel.text} key={index}/>
  );
  return(
    <div className='home'>
      <Jumbotron fluid>
        <img className='logo' src='/assets/images/logo/white-on-transparent.svg' alt='Thermometer Logo'/>
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
      <section className='info-panels'>
        {panelComponents}
      </section>
      <section className='inverted'>
        <div className='detail-info'>
          <img src='/assets/images/thermometer.jpg' alt='thermometer' />
          <div className='detail-info-text'>
            <h3>This is What it Looks Like</h3>
            <p>
              Once one of these actually exists, this is where I'd put a picture of it.
              If you've read this far, you deserve to see it. I think also there should be
              a paragraph here with as few words as possible explaining how it works right here.
            </p>
            <p>
              Here will be the tech specs, weight, height, and that junk. Right now we're just
              filling space for reference.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
};
