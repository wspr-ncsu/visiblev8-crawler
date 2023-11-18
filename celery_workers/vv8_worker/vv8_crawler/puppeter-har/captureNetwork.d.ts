import { Page } from "puppeteer";
import { Har } from "har-format";
declare type CaptureOptions = {
    saveResponses?: boolean;
    captureMimeTypes?: string[];
};
declare type StopFn = () => Promise<Har>;
export declare function captureNetwork(page: Page, { saveResponses, captureMimeTypes, }?: CaptureOptions): Promise<StopFn>;
export {};
