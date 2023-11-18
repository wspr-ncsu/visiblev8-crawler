"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
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
Object.defineProperty(exports, "__esModule", { value: true });
exports.captureResponses = void 0;
var captureResponses = function (client, _a) {
    var captureMimeTypes = _a.captureMimeTypes, saveResponses = _a.saveResponses;
    var _b = resolvableFactory(), createResolvable = _b[0], getResponses = _b[1];
    var callback = function (params) { return __awaiter(void 0, void 0, void 0, function () {
        var response, requestId, resolve;
        return __generator(this, function (_a) {
            if (!saveResponses) {
                return [2 /*return*/];
            }
            response = params.response, requestId = params.requestId;
            // Response body is unavailable for redirects, no-content, image, audio and video responses
            if (response.status === 204 ||
                response.headers.location != null ||
                !(captureMimeTypes.includes(response.mimeType) || captureMimeTypes.includes("*"))) {
                return [2 /*return*/];
            }
            resolve = createResolvable();
            client.on("Network.loadingFinished", function (params) { return __awaiter(void 0, void 0, void 0, function () {
                var _a, _b;
                var _c;
                return __generator(this, function (_d) {
                    switch (_d.label) {
                        case 0:
                            if (params.requestId !== requestId) {
                                return [2 /*return*/];
                            }
                            _a = resolve;
                            _c = {};
                            _b = requestId;
                            return [4 /*yield*/, extractResponseContent(client, requestId)];
                        case 1:
                            _a.apply(void 0, [(_c[_b] = _d.sent(),
                                    _c)]);
                            return [2 /*return*/];
                    }
                });
            }); });
            return [2 /*return*/];
        });
    }); };
    client.on("Network.responseReceived", callback);
    var dispose = function () { return client.off("Network.responseReceived", callback); };
    return function (networkEvents) { return __awaiter(void 0, void 0, void 0, function () {
        var responses;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    dispose();
                    return [4 /*yield*/, getResponses()];
                case 1:
                    responses = _a.sent();
                    return [2 /*return*/, networkEvents.map(function (event) {
                            var _a = event.params, requestId = _a.requestId, response = _a.response;
                            if (!requestId || !response) {
                                return event;
                            }
                            var body = responses[requestId];
                            if (!body) {
                                return event;
                            }
                            return __assign(__assign({}, event), { params: __assign(__assign({}, event.params), { response: __assign(__assign({}, response), { body: body }) }) });
                        })];
            }
        });
    }); };
};
exports.captureResponses = captureResponses;
var extractResponseContent = function (client, requestId) { return __awaiter(void 0, void 0, void 0, function () {
    var responseBody, e_1;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                _a.trys.push([0, 2, , 3]);
                return [4 /*yield*/, client.send("Network.getResponseBody", {
                        requestId: requestId,
                    })
                    // Set the response so `chrome-har` can add it to the HAR
                ];
            case 1:
                responseBody = _a.sent();
                // Set the response so `chrome-har` can add it to the HAR
                return [2 /*return*/, Buffer.from(responseBody.body, responseBody.base64Encoded ? "base64" : undefined).toString()];
            case 2:
                e_1 = _a.sent();
                return [3 /*break*/, 3];
            case 3: return [2 /*return*/];
        }
    });
}); };
var resolvableFactory = function () {
    var promises = [];
    var createResolvable = function () {
        var resolverRef = { current: null };
        var promise = new Promise(function (resolve) {
            resolverRef.current = resolve;
        });
        var resolver = function (response) {
            if (!resolverRef.current) {
                setTimeout(resolver, 1);
            }
            else {
                resolverRef.current(response);
            }
        };
        promises.push(promise);
        return resolver;
    };
    var getResults = function () { return __awaiter(void 0, void 0, void 0, function () {
        var results;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, Promise.all(promises)];
                case 1:
                    results = _a.sent();
                    return [2 /*return*/, results.reduce(function (combinedResults, result) { return (__assign(__assign({}, combinedResults), result)); }, {})];
            }
        });
    }); };
    return [createResolvable, getResults];
};
