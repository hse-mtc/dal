import axios from 'axios'
import { MessageBox, Message } from 'element-ui'
import { updateAccess} from "@/api/tokens";
import store from '@/store'
import { getToken } from '@/utils/auth'
import LocalStorageService from "./LocalStorageService";
// LocalstorageService
const localStorageService = LocalStorageService.getService();
export const baseURL = (() => {
  let host = process.env.VUE_APP_BACK_END_HOST || "localhost"
  let port = process.env.VUE_APP_BACK_END_PORT || "9090"
  return "http://" + host + ":" + port + "/api"
})();

// create an axios instance
const service = axios.create({
  baseURL: baseURL,
  timeout: 10000, // request timeout
  // withCredentials: true, // send cookies when cross-domain requests
})

// request interceptor
service.interceptors.request.use(
  config => {
    // do something before request is sent

    // if (store.getters.token) {
    //   // let each request carry token
    //   // ['X-Token'] is a custom headers key
    //   // please modify it according to the actual situation
    //   config.headers['Authorization'] = 'Bearer ' + getToken()
    // }
    const token = localStorageService.getAccessToken();
    console.log(token, 'access token')
    if (token) {
      config.headers['Authorization'] = 'Bearer ' + token;
    }
    // config.headers['Content-Type'] = 'application/json';
    return config;
  },
  error => {
    // do something with request error
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

// response interceptor
service.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
  */

  /**
   * Determine the request status by custom code
   * Here is just an example
   * You can also judge the status by HTTP Status Code
   */
  response => {
    return response

    // if the custom code is not 20000, it is judged as an error.
    // if (res.code !== 20000) {
    //   Message({
    //     message: res.message || 'Error',
    //     type: 'error',
    //     duration: 5 * 1000
    //   })



      // // 50008: Illegal token; 50012: Other clients logged in; 50014: Token expired;
      // if (res.code === 50008 || res.code === 50012 || res.code === 50014) {
      //   // to re-login
      //   MessageBox.confirm('You have been logged out, you can cancel to stay on this page, or log in again', 'Confirm logout', {
      //     confirmButtonText: 'Re-Login',
      //     cancelButtonText: 'Cancel',
      //     type: 'warning'
      //   }).then(() => {
      //     store.dispatch('user/resetToken').then(() => {
      //       location.reload()
      //     })
      //   })
      // }
      // return Promise.reject(new Error(res.message || 'Error'))
  },
  error => {
    console.log('err' + error) // for debug

    const originalRequest = error.config;

    // if (error.response.status === 401) {
    //   this.$router.push('/login');
    //   return Promise.reject(error);
    // }

    if (error.response.status === 401 && !originalRequest._retry) {

      originalRequest._retry = true;
      const refreshToken = localStorageService.getRefreshToken();
      updateAccess(
          {
            "refresh": refreshToken
          }
      ).then(res => {
        if (res.status === 200) {
          localStorageService.setToken(res.data);
          axios.defaults.headers.common['Authorization'] = 'Bearer ' + localStorageService.getAccessToken();
          return axios(originalRequest);
        }
      })
    }

    Message({
      message: error.message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service
