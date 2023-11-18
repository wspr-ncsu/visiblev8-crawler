import { CDPSession, ResponseForRequest } from "puppeteer";
declare type Params = {
    requestId?: string;
    response?: ResponseForRequest;
};
export declare type ObserverResult = {
    method: string;
    params: Params;
};
export declare const observeEvents: (client: CDPSession, events: string[]) => (() => Promise<ObserverResult[]>);
export {};
