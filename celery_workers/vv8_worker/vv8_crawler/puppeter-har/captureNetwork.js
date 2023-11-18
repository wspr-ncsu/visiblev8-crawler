"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var __spreadArray = (this && this.__spreadArray) || function (to, from) {
    for (var i = 0, il = from.length, j = to.length; i < il; i++, j++)
        to[j] = from[i];
    return to;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.captureNetwork = void 0;
var chrome_har_1 = require("chrome-har");
var observeEvents_1 = require("./observeEvents");
var captureResponses_1 = require("./captureResponses");
var pageEventsToObserve = [
    "Page.loadEventFired",
    "Page.domContentEventFired",
    "Page.frameStartedLoading",
    "Page.frameAttached",
    "Page.frameScheduledNavigation",
];
var networkEventsToObserve = [
    "Network.requestWillBeSent",
    "Network.requestServedFromCache",
    "Network.dataReceived",
    "Network.responseReceived",
    "Network.resourceChangedPriority",
    "Network.loadingFinished",
    "Network.loadingFailed",
];
function captureNetwork(page, _a) {
    var _b = _a === void 0 ? {} : _a, _c = _b.saveResponses, saveResponses = _c === void 0 ? false : _c, _d = _b.captureMimeTypes, captureMimeTypes = _d === void 0 ? ["text/html", "application/json"] : _d;
    return __awaiter(this, void 0, void 0, function () {
        var client, stopPageEventCapturing, stopNetworkEventCapturing, stopRequestCapturing;
        return __generator(this, function (_e) {
            switch (_e.label) {
                case 0: return [4 /*yield*/, page.target().createCDPSession()];
                case 1:
                    client = _e.sent();
                    return [4 /*yield*/, client.send("Page.enable")];
                case 2:
                    _e.sent();
                    return [4 /*yield*/, client.send("Network.enable")];
                case 3:
                    _e.sent();
                    stopPageEventCapturing = observeEvents_1.observeEvents(client, pageEventsToObserve);
                    stopNetworkEventCapturing = observeEvents_1.observeEvents(client, networkEventsToObserve);
                    stopRequestCapturing = captureResponses_1.captureResponses(client, {
                        captureMimeTypes: captureMimeTypes,
                        saveResponses: saveResponses,
                    });
                    return [2 /*return*/, function getHar() {
                            return __awaiter(this, void 0, void 0, function () {
                                var pageEvents, networkEvents, _a;
                                return __generator(this, function (_b) {
                                    switch (_b.label) {
                                        case 0: return [4 /*yield*/, stopPageEventCapturing()];
                                        case 1:
                                            pageEvents = _b.sent();
                                            _a = stopRequestCapturing;
                                            return [4 /*yield*/, stopNetworkEventCapturing()];
                                        case 2: return [4 /*yield*/, _a.apply(void 0, [_b.sent()])];
                                        case 3:
                                            networkEvents = _b.sent();
                                            return [4 /*yield*/, client.detach()];
                                        case 4:
                                            _b.sent();
                                            return [2 /*return*/, chrome_har_1.harFromMessages(__spreadArray(__spreadArray([], pageEvents), networkEvents), {
                                                    includeTextFromResponseBody: saveResponses,
                                                })];
                                    }
                                });
                            });
                        }];
            }
        });
    });
}
exports.captureNetwork = captureNetwork;
