const defaultPyodideUrl = "https://cdn.jsdelivr.net/pyodide/v0.27.5/full/pyodide.js";

let _apps = {};
let _documentUrl = document.URL;

// This method is called from Dart on backend.connect()
// dartOnMessage is called on backend.onMessage
// it accepts "data" of type JSUint8Array
globalThis.jsConnect = async function(appId, dartOnMessage) {
    let app = {
        "dartOnMessage": dartOnMessage
    };
    _apps[appId] = app;
    app.worker = new Worker("python-worker.js");

    app.worker.onmessage = (event) => {
        if (event.data == "initialized") {
            app.onPythonInitialized();
        } else {
            app.dartOnMessage(event.data);
        }
    };

    let pythonInitialized = new Promise((resolveCallback) => app.onPythonInitialized = resolveCallback);

    // initialize worker
    app.worker.postMessage({
        pyodideUrl: globalThis.pyodideUrl ?? defaultPyodideUrl,
        _documentUrl,
        micropipIncludePre,
        pythonModuleName
    });

    await pythonInitialized;
    console.log(`Pyodide engine initialized for app: ${appId}`);
}

// Called from Dart on backend.send
// data is a message serialized to JSUint8Array
globalThis.jsSend = async function(appId, data) {
    var app = _apps[appId];
    if (app) {
        app.worker.postMessage(data);
    }
}