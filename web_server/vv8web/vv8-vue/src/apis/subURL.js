import { request } from '@/utils/request'
import axios from "axios"

// post result: url => json
export function sendurl(data_url) {
    
    return request({
        url: "/url",
        method: "post",
        headers: {
            "Content-type": "application/json"
        },
        dataType: 'json',
        data: {url: "www.google.com"},
    })
}



// post url: url => bool: valid/cache
export function getResults(data) {
    return request({
        url: "/results",
        method: "post",
        data
    })
}
