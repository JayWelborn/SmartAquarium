import {createStore} from 'redux';
import {Provider} from 'react-redux';
import React from 'react';
import ReactDOM from 'react-dom';

import thermometer from './redux/reducers';
import {loadState, saveState} from './utils/localStorage';

import App from './App';


const persistedState = loadState();
const store = createStore(
  thermometer,
  persistedState
);
store.subscribe(() => {
  saveState(store.getState())
});

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('root')
);
