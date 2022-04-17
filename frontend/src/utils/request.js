import axios from "axios"

export function request(config){
    
    // create axios instance
    const instance = axios.create({
        // timeout: 5000
    })

    instance.interceptors.request.use( config => {
        return config
    }, error => {
        console.log('request failed.  ${error}')
    })

    instance.interceptors.response.use( res => {
        return res
    }, error => {
        console.log(error)
    })

    return instance(config)
}