import axios from 'axios'
import {Message} from 'element-ui'
import {updateAccess} from "@/api/tokens";
import LocalStorageService from "./LocalStorageService";

const localStorageService = LocalStorageService.getService();
export const baseURL = (() => {
    // eslint-disable-next-line
    const host = process.env.VUE_APP_BACK_END_HOST || "localhost"
    // eslint-disable-next-line
    const port = process.env.VUE_APP_BACK_END_PORT || "9090"
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
        const token = localStorageService.getAccessToken();
        if (token) {
            config.headers['Authorization'] = 'Bearer ' + token;
        }
        return config;
    },
    error => {
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
    }, error => {
        console.log('err' + error) // for debug
        const originalRequest = error.config;
        if (error.response.status === 401 && !originalRequest._retry && !originalRequest.url.includes('tokens/refresh')) {
            originalRequest._retry = true;
            const refreshToken = localStorageService.getRefreshToken();
            return updateAccess(
                {
                    "refresh": refreshToken
                }
            ).then(res => {
                if (res.status === 200) {
                    localStorageService.setToken(res.data);
                    axios.defaults.headers.common['Authorization'] = 'Bearer ' + res.data.access;
                    originalRequest.headers['Authorization'] = 'Bearer ' + res.data.access;
                    return axios(originalRequest);
                }
            }).catch(() => {
                location.reload()
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
