import {apiCall, apiRoot} from './api'

const loginURL = apiRoot + 'api-auth/login/'
const userURL = apiRoot + 'api-auth/user/'


/**
 * Utility function to log a user in. Makes approppriate
 * API calls, and updates redux store with user info for
 * access by all components
 *
 * @param  {string}  username
 * @param  {string}  password
 * @param {function} logUserIn redux action generator to log
 *                             user in and update state
 */
export function login(username, password, logUserIn) {
  let method = 'post'
  let header = new Headers({
    'Content-Type': 'application/json'
  })
  let body = JSON.stringify({
    username: username,
    password: password,
  })

  // initial api call to log user in
  apiCall(loginURL, method, header, body)
  .then(loginData => {
    const token = loginData.key

    method = 'get'
    header = new Headers({
      'Content-Type': 'application/json',
      'Authorization': 'Token ' + token,
    })
    // get user data for newly authenticated user
    apiCall(userURL, method, header, {})
    .then(user => {
      // get user's profile data
      apiCall(user.profile, method, header, {})
      .then(profile => {
        // update app state to represent logged in user
        logUserIn(user, profile, loginData.key)
      })
    })
  })
  .catch(error => {
    console.log(error)
  })
}
