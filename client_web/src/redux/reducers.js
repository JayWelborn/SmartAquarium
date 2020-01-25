import {
  LOG_USER_IN, LOG_USER_OUT, UPDATE_USER, UPDATE_PROFILE
} from './actions'


/**
 * App initilaizes an empty state
 * @type {Object}
 */
const initialState = {
  userLoggedIn: false,
  currentUser: {},
  currentProfile: {},
  token: null,
}

/**
 * Reducer for using actions to update app state
 *
 * @param  {object} state  current state of app
 * @param  {object} action redux action to update state
 */
export default function thermometer(state = initialState, action) {

  switch (action.type) {

    case LOG_USER_IN:
      return Object.assign({}, state, {
        userLoggedIn: true,
        currentUser: action.payload.user,
        currentProfile: action.payload.profile,
        token: action.payload.token,
      })

    case LOG_USER_OUT:
      return initialState

    case UPDATE_USER:
      return Object.assign({}, state, {
        currentUser: action.payload.user
      })

    case UPDATE_PROFILE:
      return Object.assign({}, state, {
        currentProfile: action.payload.profile
      })

    default:
      return state
  }
}
