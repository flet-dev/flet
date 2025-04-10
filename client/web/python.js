const defaultPyodideUrl = "https://cdn.jsdelivr.net/pyodide/v0.27.5/full/pyodide.js";
const pythonWorker = new Worker("python-worker.js");

let _onPythonInitialized = null;
let pythonInitialized = new Promise((onSuccess) => _onPythonInitialized = onSuccess);
let _onReceivedCallback = null;

pythonWorker.onmessage = (event) => {
    if (event.data == "initialized") {
        _onPythonInitialized();
    } else {
        _onReceivedCallback(event.data);
    }
};

documentUrl = document.URL;

// initialize worker
pythonWorker.postMessage({
    pyodideUrl: globalThis.pyodideUrl ?? defaultPyodideUrl,
    documentUrl,
    micropipIncludePre,
    pythonModuleName
});

globalThis.jsConnect = async function(receiveCallback) {
    _onReceivedCallback = receiveCallback;
    await pythonInitialized;
    console.log("Pyodide engine initialized!");
}

globalThis.jsSend = async function(data) {
    pythonWorker.postMessage(data);
}