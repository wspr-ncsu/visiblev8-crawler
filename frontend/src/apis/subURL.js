import { request } from '@/utils/request'

// post result: url => json
/**
 * Sends a request to the server to check if the URL is valid.
 * @param {*} data_url The URL to check
 * @returns A promise that contains two values: a boolean indicating if the URL is valid, and a boolean indicating if the URL is cached
 */
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
