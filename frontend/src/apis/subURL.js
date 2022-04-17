import { request } from '@/utils/request'

// post result: url => json
export function sendurl(data_url) {
    
    return request({
        url: "/urlcheck",
        method: "post",
        headers: {
            "Content-type": "application/json"
        },
        dataType: 'json',
        data: {url: data_url},
    })
}

/**
 * Submits the URL to the server for processing.
 * @param {string} data_url the URL to be submitted
 * @param {boolean} rerun a true/false value to determine whether to rerun the URL
 * @returns the id of the URL
 */
export function submiturl(data_url, rerun) {
    
    return request({
        url: "/urlsubmit",
        method: "post",
        headers: {
            "Content-type": "application/json"
        },
        dataType: 'json',
        data: {
            url: data_url,
            rerun: rerun
        },
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
