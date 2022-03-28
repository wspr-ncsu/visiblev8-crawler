import { request } from '@/utils/request'

// post result: url => json
export function sendURL(data) {
    return request({
        url: "/url",
        method: "post",
        data
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
