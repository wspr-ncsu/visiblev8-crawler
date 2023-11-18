import { CDPSession } from "puppeteer";
import { ObserverResult } from "./observeEvents";
declare type CaptureResponsesOptions = {
    captureMimeTypes: string[];
    saveResponses: boolean;
};
export declare const captureResponses: (client: CDPSession, { captureMimeTypes, saveResponses }: CaptureResponsesOptions) => (networkEvents: ObserverResult[]) => Promise<ObserverResult[]>;
export {};
