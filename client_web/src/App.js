import React from 'react';
import {connect} from 'react-redux';
import {BrowserRouter} from 'react-router-dom';

import Header from './components/header';
import Main from './components/Main.js';


function mapStateToProps(state) {
  return {
    userLoggedIn: state.userLoggedIn,
    user: state.currentUser,
    profile: state.currentProfile
  }
}

function App(props) {
  let user = props.user;
  return (
    <BrowserRouter>
      <Header />
      <Main />
    </BrowserRouter>
  );
}

export default connect(mapStateToProps)(App);
