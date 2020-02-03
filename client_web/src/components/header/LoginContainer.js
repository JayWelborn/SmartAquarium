import React, { Component }    from 'react';
import {connect}               from 'react-redux'
import {logUserIn, logUserOut} from '../../redux/actions'

import Login  from './Login'
import LogOut from './LogOut'

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
 * Map app's dispatch methods to current component
 *
 * @param  {dispatch} dispatch method to dispatch actions
 * @return {object}            object mapping of dispatched methods
 */
function mapDispatchToProps(dispatch) {
  return {
    logUserIn: (username, password, token) => {
      dispatch(logUserIn(username, password, token))
    },
    logUserOut: () => {
      dispatch(logUserOut())
    },
  }
}

/**
 * Container for displaying either LogIn or LogOut components depending
 * on app's state
 */
class LoginContainer extends Component {

  /**
   * Bind methods to current isntance
   *
   * @param  {object} props object properties
   */
  constructor(props){
      super(props);

      this.logUserIn = this.props.logUserIn.bind(this)
      this.logUserOut = this.props.logUserOut.bind(this)
  }

  /**
   * If user is logged in, render a LogOut button. If no user
   * logged in, render a LogIn form.
   *
   * @return {component} appropriate component for login or logout
   */
  render() {
    if (this.props.userLoggedIn) {
      return (
        <LogOut logUserOut={this.logUserOut} />
      )
    } else {
      return (
        <Login logUserIn={this.logUserIn} />
      )
    }
  }
}

/**
 * Map Redux state to LoginContainer component
 */
export default connect(mapStateToProps, mapDispatchToProps)(LoginContainer)
