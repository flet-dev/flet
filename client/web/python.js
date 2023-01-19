const pyodideUrl = "https://cdn.jsdelivr.net/pyodide/v0.22.0/full/pyodide.js";
let flet_js = {}; // namespace for Python global functions

function loadScript(url, callback) {
    // Adding the script tag to the head as suggested before
    var head = document.head;
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = url;

    // Then bind the event to the callback function.
    // There are several events for cross browser compatibility.
    script.onreadystatechange = callback;
    script.onload = callback;

    // Fire the loading
    head.appendChild(script);
}

let pyodideReady = new Promise((resolve) => {
    loadScript(pyodideUrl, async () => {
        let pyodide = await loadPyodide();
        pyodide.registerJsModule("flet_js", flet_js);
        await pyodide.loadPackage("micropip");
        await pyodide.runPythonAsync(`
        import micropip
        import os

        from pyodide.http import pyfetch
        response = await pyfetch("/app.tar.gz")
        await response.unpack_archive()
        if os.path.exists("requirements.txt"):
            with open("requirements.txt", "r") as f:
                deps = [line.rstrip() for line in f]
                print("Loading requirements.txt:", deps)
                await micropip.install(deps)
      `);
        pyodide.pyimport(pythonModuleName);
        resolve(pyodide);
    });
});

async function jsConnect() {
    await pyodideReady;
    await flet_js.start_connection();
}

async function jsSend(data) {
    flet_js.send(data)
}

async function jsReceive() {
    return await flet_js.receive_async();
}