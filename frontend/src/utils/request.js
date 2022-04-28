import axios from "axios"

/**
 * Creates a new request object.
 * @param {*} config The request configuration.
 * @returns A new request object.
 */
export function request(config){
    
    // create axios instance
    const instance = axios.create({
        // timeout: 5000
    })

    instance.interceptors.request.use( config => {
        return config
    }, error => {
        console.log(`request failed.  ${error}`)
    })

    instance.interceptors.response.use( res => {
        return res
    }, error => {
        console.log(error)
    })

    return instance(config)
}