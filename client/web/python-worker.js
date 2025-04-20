self.pyodideUrl = null;
self.micropipIncludePre = false;
self.pythonModuleName = null;
self.documentUrl = null;
self.initialized = false;
self.flet_js = {}; // namespace for Python global functions

self.initPyodide = async function () {
    try {
        importScripts(self.pyodideUrl);
        self.pyodide = await loadPyodide();
        self.pyodide.registerJsModule("flet_js", flet_js);
        flet_js.documentUrl = documentUrl;
        await self.pyodide.loadPackage("micropip");
        let pre = self.micropipIncludePre ? "True" : "False";
        await self.pyodide.runPythonAsync(`
        import flet_js, micropip, os, runpy, sys, traceback
        from pyodide.http import pyfetch

        py_args = flet_js.args.to_py() if flet_js.args else None
        print("Args:", py_args)
        
        if "script" not in py_args:
            print("Downloading app archive")
            response = await pyfetch("assets/app/app.zip")
            await response.unpack_archive()
        else:
            print("Saving script to a file")
            with open("${self.pythonModuleName}.py", "w") as f:
                f.write(py_args["script"]);
    
        pkgs_path = "__pypackages__"
        if os.path.exists(pkgs_path):
            print(f"Adding {pkgs_path} to sys.path")
            sys.path.insert(0, pkgs_path)
    
        if os.path.exists("requirements.txt"):
            with open("requirements.txt", "r") as f:
                deps = [line.rstrip() for line in f]
                print("Loading requirements.txt:", deps)
                await micropip.install(deps, pre=${pre})

        if "dependencies" in py_args:
            await micropip.install(py_args["dependencies"], pre=${pre})
    
        # Execute app
        runpy.run_module("${self.pythonModuleName}", run_name="__main__")
      `);
        await self.flet_js.start_connection(self.receiveCallback);
        self.postMessage("initialized");
    } catch (error) {
        self.postMessage(error.toString());
    }
};

self.receiveCallback = (message) => {
    self.postMessage(message.toJs());
}

self.onmessage = async (event) => {
    // run only once
    if (!self.initialized) {
        self.initialized = true;
        self.pyodideUrl = event.data.pyodideUrl;
        self.flet_js.args = event.data.args;
        self.documentUrl = event.data.documentUrl;
        self.micropipIncludePre = event.data.micropipIncludePre;
        self.pythonModuleName = event.data.pythonModuleName;
        await self.initPyodide();
    } else {
        // message
        flet_js.send(event.data);
    }
};