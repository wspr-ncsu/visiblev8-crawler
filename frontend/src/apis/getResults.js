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

export function getGets(submission_id) {
    return request({
        url: `/submission/${submission_id}/gets`,
        method: "get"
    })
}


export function getGetsCount(submission_id) {
    return request({
        url: `/submission/${submission_id}/gets/count`,
        method: "get"
    })
}

export function getSets(submission_id) {
    return request({
        url: `/submission/${submission_id}/sets`,
        method: "get"
    })
}

export function getSetsCount(submission_id) {
    return request({
        url: `/submission/${submission_id}/sets/count`,
        method: "get"
    })
}

export function getConstructions(submission_id) {
    return request({
        url: `/submission/${submission_id}/constructions`,
        method: "get"
    })
}

export function getConstructionsCount(submission_id) {
    return request({
        url: `/submission/${submission_id}/constructions/count`,
        method: "get"
    })
}

export function getCalls(submission_id) {
    return request({
        url: `/submission/${submission_id}/calls`,
        method: "get"
    })
}

export function getCallsCount(submission_id) {
    return request({
        url: `/submission/${submission_id}/calls/count`,
        method: "get"
    })
}


export function getSource(submission_id, context) {
    return request({
        url: `/submission/${submission_id}/${context}/source`,
        method: "get"
    })
}
