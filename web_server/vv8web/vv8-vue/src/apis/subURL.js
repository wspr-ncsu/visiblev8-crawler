import { request } from '@/utils/request'

// post result: url => json
export default function sendURL(data) {
    return request({
        url: "/url",
        method: "post",
        data
    })
}



// post url: url => bool: valid/cache
export default function getResults(data) {
    return request({
        url: "/results",
        method: "post",
        data
    })
}
