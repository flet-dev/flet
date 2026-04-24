self.pyodideUrl = null;
self.appPackageUrl = null;
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

        # Execute app
        runpy.run_module(python_module_name, run_name="__main__")
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
        self.appPackageUrl = event.data.appPackageUrl;
        self.micropipIncludePre = event.data.micropipIncludePre;
        self.pythonModuleName = event.data.pythonModuleName;
        await self.initPyodide();
    } else {
        // message
        flet_js.send(event.data);
    }
};
