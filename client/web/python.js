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
        await pyodide.loadPackage("micropip");
        await pyodide.runPythonAsync(`
        import micropip
        await micropip.install('/python/flet_core-0.4.0.dev1069-py3-none-any.whl', pre=True)
        print("Imported flet-core")
        await micropip.install('/python/flet_pyodide-0.4.0.dev1069-py3-none-any.whl', pre=True)
        print("Imported flet-pyodide")
      `);
        pyodide.registerJsModule("flet_js", flet_js);
        console.log("Before fetching main script");
        let main_script = await (await fetch("/python/main.py")).text();
        console.log("After fetching main script");
        await pyodide.runPythonAsync(main_script);
        console.log("Loaded main program")
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