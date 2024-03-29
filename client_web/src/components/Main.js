import React from 'react';
import {Switch, Route} from 'react-router-dom';

import About from './home/about';
import Home from './home';
import login from './registration/login';
import register from './registration/register';


export default function Main(props) {
  return(
    <Switch>
      <Route exact path='/' component={Home} />
      <Route path='/about' component={About} />
      <Route path='/login' component={login} />
      <Route path='/register' component={register} />
    </Switch>
  );
};
