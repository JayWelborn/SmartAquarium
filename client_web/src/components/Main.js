import React from 'react';
import {Switch, Route} from 'react-router-dom';

import home from './home';
import about from './about';


export default function Main(props) {
  return(
    <Switch>
      <Route exact path='/' component={home} />
      <Route path='/about' component={about} />
    </Switch>
  );
};
