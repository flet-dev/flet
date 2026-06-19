// Pyodide URL is injected per build by flet-web's patch_index.py
// (sets flet.pyodideUrl). Falls back to the local pyodide/ directory that
// flet build web / flet publish drop next to the page.
let _apps = {};
let _documentUrl = document.URL;

// This method is called from Dart on backend.connect()
// dartOnMessage is called on backend.onMessage
// it accepts "data" of type JSUint8Array
globalThis.jsConnect = async function (appId, args, dartOnMessage) {
    let app = {
        "dartOnMessage": dartOnMessage
    };
    console.log(`Starting up Python worker: ${appId}, args: ${args}`);
    _apps[appId] = app;
    // Module worker (type: "module") is required by Pyodide >= 0.29 — the
    // runtime throws "Classic web workers are not supported" inside any
    // worker where `importScripts` is callable. Module workers don't have
    // `importScripts`, so the check passes. Older Pyodide lines (0.27.x)
    // accept module workers too, so this is forward-compatible across all
    // supported Python versions (3.12 → Pyodide 0.27.7, 3.13 → 0.29.4,
    // 3.14 → 314.0.0).
    app.worker = new Worker(
        (flet.entrypointBaseUrl.endsWith("/") ?
            flet.entrypointBaseUrl.slice(0, -1) : flet.entrypointBaseUrl) + "/python-worker.js",
        { type: "module" });

    var error;
    app.worker.onmessage = (event) => {
        if (typeof event.data === "string") {
            if (event.data != "initialized") {
                error = event.data;
            }
            app.onPythonInitialized();
        } else {
            app.dartOnMessage(event.data);
        }
    };

    let pythonInitialized = new Promise((resolveCallback) => app.onPythonInitialized = resolveCallback);

    // initialize worker
    app.worker.postMessage({
        // `.mjs` is the ES-module variant. python-worker.js (now a module
        // worker) loads it via dynamic `import()`. The legacy `.js`
        // variant relied on `importScripts`, which doesn't exist in a
        // module worker.
        pyodideUrl: flet.pyodideUrl || "pyodide/pyodide.mjs",
        args: args,
        documentUrl: _documentUrl,
        appPackageUrl: flet.appPackageUrl,
        micropipIncludePre: flet.micropipIncludePre,
        pythonModuleName: flet.pythonModuleName
    });

    await pythonInitialized;

    if (error) {
        console.log("Python worker init error:", error);
        throw error;
    } else {
        console.log(`Python worker initialized: ${appId}`);
    }
}

// Called from Dart on backend.send
// data is a message serialized to JSUint8Array
globalThis.jsSend = async function (appId, data) {
    if (appId in _apps) {
        const app = _apps[appId];
        app.worker.postMessage(data);
    }
}

// Called from Dart on channel.disconnect
globalThis.jsDisconnect = async function (appId) {
    if (appId in _apps) {
        console.log(`Terminating Python worker: ${appId}`);
        const app = _apps[appId];
        delete _apps[appId];
        app.worker.terminate();
        app.worker.onmessage = null;
        app.worker.onerror = null;
    }
}
