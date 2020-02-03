import React, { Component } from 'react';
import {Button} from 'react-bootstrap';

/**
 * Component to display a logout button
 */
export default class LogOut extends Component {

  /**
   * Class constructor
   *
   * @param  {object} props component's properties
   */
  constructor(props){
    super(props);

    // see Redux/actions.js
    this.logUserOut = this.props.logUserOut.bind(this)
  }

  render() {
    return (
      <Button bsStyle="primary" onClick={this.logUserOut}>
        Log Out
      </Button>
    );
  }
}
