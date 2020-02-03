export const LOG_USER_IN = 'LOG_USER_IN'
export const LOG_USER_OUT = 'LOG_USER_OUT'
export const UPDATE_USER = 'UPDATE_USER'
export const UPDATE_PROFILE = 'UPDATE_PROFILE'

/**
 * Create new action to log in a given user
 *
 * @param  {object} user    user's info
 * @param  {object} profile user's profile info
 * @param  {string} token   user's authentication token
 */
export function logUserIn(user, profile, token) {
  return {
    type: LOG_USER_IN,
    payload: {
      user: user,
      profile: profile,
      token: token,
    }
  }
}

export function logUserOut() {
  return {
    type: LOG_USER_OUT,
    payload: {}
  }
}

export function updateProfile(profile) {
  return {
    type: UPDATE_PROFILE,
    payload: {
      profile: profile
    }
  }
}

export function updateUser(user) {
  return {
    type: UPDATE_USER,
    payload: {
      user: user
    }
  }
}
