// <id>/gets
// <id>/gets/count
// <id>/sets
// <id>/sets/count
// <id>/objects
// <id>/objects/count
// <id>/calls
// <id>/calls/count
// <id>/source text/<context id> 

import { request } from '@/utils/request'

/**
 * Creates a request to the server to get the Get Requests for a given URL.
 * @param {*} submission_id the id of the URL to get the Get Requests for
 * @returns the Get Requests for the given URL
 */
export function getGets(submission_id) {
    return request({
        url: `/submission/${submission_id}/gets`,
        method: "get"
    })
}

/**
 * Creates a request to the server to get the number of Get Requests for a given URL.
 * @param {*} submission_id the id of the URL to get the number of Get Requests for
 * @returns the number of Get Requests for the given URL
 */
export function getGetsCount(submission_id) {
    return request({
        url: `/submission/${submission_id}/gets/count`,
        method: "get"
    })
}

/**
 * Creates a request to the server to get the Set Requests for a given URL.
 * @param {*} submission_id the id of the URL to get the Set Requests for
 * @returns the Set Requests for the given URL
 */
export function getSets(submission_id) {
    return request({
        url: `/submission/${submission_id}/sets`,
        method: "get"
    })
}

/**
 * Requests the number of Set Requests for a given URL.
 * @param {*} submission_id the id of the URL to get the number of Set Requests for
 * @returns the number of Set Requests for the given URL
 */
export function getSetsCount(submission_id) {
    return request({
        url: `/submission/${submission_id}/sets/count`,
        method: "get"
    })
}

/**
 * Requests the Objects for a given URL.
 * @param {*} submission_id the id of the URL to get the Objects for
 * @returns the Objects for the given URL
 */
export function getConstructions(submission_id) {
    return request({
        url: `/submission/${submission_id}/constructions`,
        method: "get"
    })
}

/**
 * Returns the number of Objects for a given URL.
 * @param {*} submission_id the id of the URL to get the number of Objects for
 * @returns the number of Objects for the given URL
 */
export function getConstructionsCount(submission_id) {
    return request({
        url: `/submission/${submission_id}/constructions/count`,
        method: "get"
    })
}

/**
 * Requests the Function Calls for a given URL.
 * @param {*} submission_id the id of the URL to get the Function Calls for
 * @returns the Function Calls for the given URL
 */
export function getCalls(submission_id) {
    return request({
        url: `/submission/${submission_id}/calls`,
        method: "get"
    })
}

/**
 * Requests the number of Function Calls for a given URL.
 * @param {*} submission_id the id of the URL to get the number of Function Calls for
 * @returns the number of Function Calls for the given URL
 */
export function getCallsCount(submission_id) {
    return request({
        url: `/submission/${submission_id}/calls/count`,
        method: "get"
    })
}

/**
 * Get the source text for a given submission id and context id.
 * @param {*} submission_id The id of the URL to get the source text for
 * @param {*} context The execution context to get the source text for
 * @returns the source text for the given URL and context
 */
export function getSource(submission_id, context) {
    return request({
        url: `/submission/${submission_id}/${context}/source`,
        method: "get"
    })
}

/**
 * Gets the 10 most recent submissions.
 * @returns a list of the 10 most recent submissions
 */
export function getHistory() {
    return request({
        url: `/history`
    })
}

/**
 * Gets the execution tree for a URL
 * @param {*} submission_id the id of the URL to get the execution tree for
 * @returns The execution tree for the given URL
 */
export function getTree(submission_id) {
    return request({
        url: `/submission/${submission_id}/executiontree`
    })
}