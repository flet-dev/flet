self.pyodideUrl = null;
self.appPackageUrl = null;
self.micropipIncludePre = false;
self.pythonModuleName = null;
self.documentUrl = null;
self.initialized = false;
self.flet_js = {}; // namespace for Python global functions

// Flipped to true right before `runpy.run_module` runs the user app.
// Until then, stdout/stderr is bootstrap diagnostics ("Downloading app
// archive", micropip install logs, etc.) — those go to the dev console
// rather than the user-visible Console pane.
self.userAppRunning = false;
self.flet_js.userAppStarting = function () {
    self.userAppRunning = true;
};
self.sendPythonOutput = function (text, isStderr) {
    // No bridge yet, or not in user-code mode — surface in dev console.
    // The boot script registers `flet_js.send_python_output` after the
    // user-app deps are installed (msgpack typically rides in via flet);
    // if msgpack isn't available it stays unset and prints fall through
    // to the dev console silently.
    if (!self.userAppRunning || !(self.flet_js && self.flet_js.send_python_output)) {
        if (isStderr) {
            console.error(text);
        } else {
            console.log(text);
        }
        return;
    }
    // Pyodide invokes stdout/stderr hooks with the GIL released, so
    // calling back into Python synchronously throws NoGilError. Defer
    // to a microtask — by the time it runs, the GIL state is normal.
    queueMicrotask(function () {
        self.flet_js.send_python_output(text, isStderr);
    });
};

self.initPyodide = async function () {
    try {
        importScripts(self.pyodideUrl);
        self.pyodide = await loadPyodide({
            stdout: (text) => self.sendPythonOutput(text, false),
            stderr: (text) => self.sendPythonOutput(text, true),
        });
        self.pyodide.registerJsModule("flet_js", flet_js);
        self.pyodide.globals.set("app_package_url", self.appPackageUrl);
        self.pyodide.globals.set("python_module_name", self.pythonModuleName);
        self.pyodide.globals.set("micropip_include_pre", self.micropipIncludePre);
        flet_js.documentUrl = documentUrl;
        await self.pyodide.runPythonAsync(`
        import flet_js, os, runpy, sys, traceback
        from pyodide.http import pyfetch

        py_args = flet_js.args.to_py() if flet_js.args else None

        if "app_package_url" in py_args:
            app_package_url = py_args["app_package_url"]

        if "python_module_name" in py_args:
            python_module_name = py_args["python_module_name"]

        if python_module_name is None:
            python_module_name = "main"

        if "micropip_include_pre" in py_args:
            micropip_include_pre = py_args["micropip_include_pre"]

        if micropip_include_pre is None:
            micropip_include_pre = False

        print("python_module_name:", python_module_name)
        print("micropip_include_pre:", micropip_include_pre)

        if "script" not in py_args:
            print("Downloading app archive")
            response = await pyfetch(app_package_url)
            # Pick format from the URL's path extension. Pyodide's
            # filename-based sniff trips over query strings like
            # ?v=42. We only support zip and tar.gz (matching what
            # our server and "flet publish" emit).
            from urllib.parse import urlparse
            _archive_path = urlparse(app_package_url).path.lower()
            if _archive_path.endswith(".zip"):
                _archive_format = "zip"
            elif _archive_path.endswith((".tar.gz", ".tgz")):
                _archive_format = "gztar"
            else:
                raise ValueError(
                    f"Unsupported app package URL: {app_package_url} "
                    "(expected .zip or .tar.gz)"
                )
            await response.unpack_archive(format=_archive_format)
        else:
            print("Saving script to a file")
            with open(f"{python_module_name}.py", "w") as f:
                f.write(py_args["script"]);

        pkgs_path = "__pypackages__"
        if os.path.exists(pkgs_path):
            print(f"Adding {pkgs_path} to sys.path")
            sys.path.insert(0, pkgs_path)

        async def ensure_micropip():
            try:
                import micropip
            except ImportError:
                import pyodide_js
                await pyodide_js.loadPackage("micropip")
                import micropip
            return micropip

        if os.path.exists("requirements.txt"):
            with open("requirements.txt", "r") as f:
                deps = [
                    line
                    for req in f
                    if (line := req.strip()) and not line.startswith("#")
                ]
                if deps:
                    micropip = await ensure_micropip()
                    print("Loading requirements.txt:", deps)
                    await micropip.install(deps, pre=micropip_include_pre)

        if os.path.exists("pyproject.toml"):
            import tomllib
            with open("pyproject.toml", "rb") as f:
                pyproject = tomllib.load(f)
            project_deps = list(
                pyproject.get("project", {}).get("dependencies", []) or []
            )
            web_deps = list(
                pyproject.get("tool", {})
                .get("flet", {})
                .get("web", {})
                .get("dependencies", [])
                or []
            )
            # [tool.flet.web].dependencies overrides [project].dependencies
            # by package name — install in order so the web-specific specs
            # win through micropip's last-writer-wins dedupe.
            pyproject_deps = project_deps + web_deps
            if pyproject_deps:
                micropip = await ensure_micropip()
                print("Loading pyproject.toml deps:", pyproject_deps)
                await micropip.install(pyproject_deps, pre=micropip_include_pre)

        if "dependencies" in py_args:
            micropip = await ensure_micropip()
            await micropip.install(py_args["dependencies"], pre=micropip_include_pre)

        # Install the python_output bridge using msgpack from the
        # already-loaded user deps (typically pulled in via flet). If
        # msgpack isn't around — apps that don't depend on flet — skip
        # silently; stdout/stderr just stays in the dev console.
        try:
            import msgpack as _msgpack

            def _send_python_output(text, is_stderr):
                flet_js.receive_callback(
                    _msgpack.packb(
                        [7, {"text": text, "is_stderr": bool(is_stderr)}]
                    )
                )

            flet_js.send_python_output = _send_python_output
        except ImportError:
            pass

        # Flip the worker into "user code" mode so stdout/stderr starts
        # flowing to the host page's Console pane instead of dev console.
        flet_js.userAppStarting()

        # Execute app. Treat a clean SystemExit (exit() / exit(0)) as
        # normal termination so the no-UI path below kicks in instead
        # of surfacing a Pyodide traceback. Non-zero codes propagate as
        # Script errors.
        try:
            runpy.run_module(python_module_name, run_name="__main__")
        except SystemExit as _exit:
            if _exit.code not in (None, 0):
                raise
      `);
        // `start_connection` is registered by `PyodideConnection.__init__`,
        // which only runs when the user app calls `ft.run(...)`. If the
        // script finished without it (e.g. a print-only test program),
        // surface a friendly message instead of a cryptic TypeError.
        // The `__flet_no_ui__:` sentinel lets host pages render a
        // neutral message rather than a Script error panel.
        if (typeof self.flet_js.start_connection !== "function") {
            self.postMessage(
                "__flet_no_ui__:Script finished without starting a Flet UI.\n" +
                "Add ft.run(main) at the end of your script to display the app."
            );
            return;
        }
        await self.flet_js.start_connection(self.receiveCallback);
        self.postMessage("initialized");
    } catch (error) {
        self.postMessage(error.toString());
    }
};

self.receiveCallback = (message) => {
    self.postMessage(message.toJs());
}
// Same channel as `receiveCallback`, exposed under `flet_js` so the
// Python python_output shim can post pre-encoded msgpack frames.
self.flet_js.receive_callback = self.receiveCallback;

self.onmessage = async (event) => {
    // run only once
    if (!self.initialized) {
        self.initialized = true;
        self.pyodideUrl = event.data.pyodideUrl;
        self.flet_js.args = event.data.args;
        self.documentUrl = event.data.documentUrl;
        self.appPackageUrl = event.data.appPackageUrl;
        self.micropipIncludePre = event.data.micropipIncludePre;
        self.pythonModuleName = event.data.pythonModuleName;
        await self.initPyodide();
    } else {
        // message
        flet_js.send(event.data);
    }
};
