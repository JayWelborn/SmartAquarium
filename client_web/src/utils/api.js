function getApiRoot() {
    if (window.location.href.includes('localhost')) {
      return 'http://localhost:8000/api/';
    } else {
      return 'https://bingoapp.pythonanywhere.com/api/'
    }
  }
  
  const apiRoot = getApiRoot();
  
  /**
   * Makes api call to given endpoint with given method and headers
   *
   * @param {string}  endpoint api endpoint
   * @param {string}  method   http method
   * @param {object}  headers  headers for fetching
   * @return {json}            response to api call
   */
  function apiCall(endpoint, method, headers={}, body={}) {
  
    let request = {
      method: method,
      headers: headers,
      mode: 'cors'
    }
  
    if (method !== 'get') {
      request['body'] = body
    }
  
    return fetch(endpoint, request)
    .then(handleErrors)
    .then(response => {
      return response.json()
    })
  }
  
  function handleErrors(response) {
    if (!response.ok) {
      console.log(response.json())
      throw Error(response.statusText)
    }
    return response
  }
  
  export {apiCall, apiRoot};
  