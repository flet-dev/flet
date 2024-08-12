importScripts("https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js");

self.pythonModuleName = null;
self.initialized = false;
self.flet_js = {}; // namespace for Python global functions

self.initPyodide = async function () {
    self.pyodide = await loadPyodide();
    self.pyodide.registerJsModule("flet_js", flet_js);
    flet_js.documentUrl = documentUrl;
    await self.pyodide.runPythonAsync(`
    import sys, runpy, traceback
    from pyodide.http import pyfetch
    response = await pyfetch("assets/app/app.zip")
    await response.unpack_archive()
    sys.path.append("__pypackages__")
    try:
        runpy.run_module("${self.pythonModuleName}", run_name="__main__")
    except Exception as e:
        traceback.print_exception(e)
  `);
    await self.flet_js.start_connection(self.receiveCallback);
    self.postMessage("initialized");
};

self.receiveCallback = (message) => {
    self.postMessage(message);
}

self.onmessage = async (event) => {
    // run only once
    if (!self.initialized) {
        self.initialized = true;
        self.documentUrl = event.data.documentUrl;
        self.pythonModuleName = event.data.pythonModuleName;
        await self.initPyodide();
    } else {
        // message
        flet_js.send(event.data);
    }
};