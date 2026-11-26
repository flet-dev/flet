// Pyodide URL is injected per build by flet-web's patch_index.py
// (sets flet.pyodideUrl). Falls back to the local pyodide/ directory that
// flet build web / flet publish drop next to the page.
let _apps = {};
let _documentUrl = document.URL;

// This method is called from Dart on backend.connect()
// dartOnMessage is called on backend.onMessage
// it accepts "data" of type JSUint8Array
// options.isolated runs the worker isolated from the page (FletBackend.isolated).
globalThis.jsConnect = async function (appId, args, dartOnMessage, options) {
    let app = {
        "dartOnMessage": dartOnMessage
    };
    console.log(`Starting up Python worker: ${appId}, args: ${args}`);
    _apps[appId] = app;
    const workerUrl = "python-worker.js";
    const isolated = !!(options && options.isolated);

    let init = {
        // `.mjs` is the ES-module variant. python-worker.js loads it via
        // dynamic `import()`. The legacy `.js` variant relied on
        // `importScripts`, which a module worker doesn't have.
        pyodideUrl: flet.pyodideUrl || "pyodide/pyodide.mjs",
        args: args,
        documentUrl: _documentUrl,
        appPackageUrl: flet.appPackageUrl,
        micropipIncludePre: flet.micropipIncludePre,
        pythonModuleName: flet.pythonModuleName
    };

    if (isolated) {
        init = _absoluteUrls(init);
        app.worker = await _startIsolatedWorker(workerUrl, _designatedUrls(init));
    } else {
        // Module worker (type: "module") is required by Pyodide >= 0.29 — the
        // runtime throws "Classic web workers are not supported" inside any
        // worker where `importScripts` is callable. Module workers don't have
        // `importScripts`, so the check passes. Older Pyodide lines (0.27.x)
        // accept module workers too, so this is forward-compatible across all
        // supported Python versions (3.12 → Pyodide 0.27.7, 3.13 → 0.29.4,
        // 3.14 → 314.0.0).
        app.worker = new Worker(workerUrl, { type: "module" });
    }

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
    app.worker.postMessage(init);

    await pythonInitialized;

    if (error) {
        console.error("Python worker init error:", error);
        await jsDisconnect(appId);
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
        // Transfer the converted array's actual buffer. On Wasm, converting
        // the Dart packet's buffer separately would produce a different copy.
        // The sender must not access data after this call.
        app.worker.postMessage(data, [data.buffer]);
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

// --- Isolated workers ------------------------------------------------------
//
// An isolated app's Python runs in a worker inside a hidden
// `<iframe sandbox="allow-scripts">` without `allow-same-origin`, so the
// worker has an opaque origin: no cookies, IndexedDB, Cache Storage or OPFS
// of the page's origin, and the `blob:` URLs it makes aren't the page's. It
// reaches the page only through Flet's protocol, relayed below.
//
// - A module worker made from a `blob:` URL doesn't start inside a sandboxed
//   frame, so it's a classic one: the host fetches python-worker.js as text
//   (same origin) and the relay starts it from a blob, after _ISOLATED_PRELUDE.
// - An opaque origin gets a fresh HTTP cache partition each time, so plain
//   downloads (Pyodide, wheels, the app package) go through the host (the
//   fetch proxy), from and into the page's cache.

// Runs in the isolated worker before python-worker.js.
const _ISOLATED_PRELUDE = `
// Pyodide refuses a worker that has importScripts, as a classic one does.
self.importScripts = undefined;
(() => {
    const realFetch = self.fetch.bind(self);
    const pending = new Map();
    let nextId = 0;
    // Plain downloads go through the page; anything with a method, body or
    // headers of its own (an API call) goes out from here, as this origin.
    self.fetch = (input, init) => {
        const request = input instanceof Request ? input : null;
        const url = request ? request.url : String(input);
        const method = ((init && init.method) || (request && request.method) || "GET").toUpperCase();
        const headers = new Headers((init && init.headers) || (request && request.headers) || undefined);
        if (method !== "GET" || (init && init.body) || [...headers].length > 0 || !/^https?:/i.test(url)) {
            return realFetch(input, init);
        }
        const id = ++nextId;
        return new Promise((resolve, reject) => {
            pending.set(id, { resolve, reject, input, init });
            self.postMessage({ __fletFetch: { id, url } });
        });
    };
    self.addEventListener("message", (event) => {
        const reply = event.data && event.data.__fletFetched;
        if (!reply) return;
        event.stopImmediatePropagation();
        const p = pending.get(reply.id);
        pending.delete(reply.id);
        if (!p) return;
        if (reply.refused) {
            // The page won't fetch it for us: fetch it as this origin.
            realFetch(p.input, p.init).then(p.resolve, p.reject);
        } else if (reply.error) {
            p.reject(new TypeError(reply.error));
        } else {
            const noBody = [101, 204, 205, 304].includes(reply.status);
            p.resolve(new Response(noBody ? null : reply.body,
                { status: reply.status, statusText: reply.statusText, headers: reply.headers }));
        }
    });
})();
`;

// The sandboxed frame's page: starts the worker and relays messages both ways.
const _ISOLATED_RELAY = `<!doctype html><script>
    let worker = null;
    function transfer(data) {
        if (data instanceof Uint8Array) return [data.buffer];
        if (data && data.__fletFetched && data.__fletFetched.body) return [data.__fletFetched.body];
        return [];
    }
    addEventListener("message", (event) => {
        if (event.source !== parent) return;
        const data = event.data;
        if (worker === null) {
            if (!data || !data.__fletStart) return;
            const url = URL.createObjectURL(new Blob([data.__fletStart.source], { type: "text/javascript" }));
            worker = new Worker(url);
            worker.onmessage = (m) => parent.postMessage(m.data, "*", transfer(m.data));
            worker.onerror = (e) => {
                e.preventDefault();
                parent.postMessage(String(e.message || "The Python worker failed to start."), "*");
            };
            worker.postMessage(data.__fletStart.init);
            return;
        }
        worker.postMessage(data, transfer(data));
    });
    parent.postMessage({ __fletReady: true }, "*");
<\/script>`;

// Starts an isolated worker; returns an object that stands in for the Worker.
async function _startIsolatedWorker(workerUrl, designatedUrls) {
    const source = await (await fetch(workerUrl)).text();
    const frame = document.createElement("iframe");
    frame.setAttribute("sandbox", "allow-scripts");
    frame.setAttribute("aria-hidden", "true");
    frame.tabIndex = -1;
    frame.style.display = "none";
    frame.srcdoc = _ISOLATED_RELAY;

    let started = false;
    let onReady;
    const ready = new Promise((resolve) => onReady = resolve);
    const worker = {
        onmessage: null,
        onerror: null,
        postMessage(data, transfer) {
            if (!frame.contentWindow) return;
            if (!started) {
                // The first message is the worker's init.
                started = true;
                frame.contentWindow.postMessage(
                    { __fletStart: { source: _ISOLATED_PRELUDE + source, init: data } }, "*");
                return;
            }
            frame.contentWindow.postMessage(data, "*", transfer || []);
        },
        terminate() {
            removeEventListener("message", onMessage);
            frame.remove();
        },
    };
    function onMessage(event) {
        // Only our frame; its origin is opaque ("null"), so check the source.
        if (event.source !== frame.contentWindow) return;
        const data = event.data;
        if (data && data.__fletReady) {
            onReady();
        } else if (data && data.__fletFetch) {
            _proxyFetch(data.__fletFetch.url, designatedUrls).then((reply) =>
                worker.postMessage({ __fletFetched: { id: data.__fletFetch.id, ...reply } },
                    reply.body ? [reply.body] : []));
        } else if (worker.onmessage) {
            worker.onmessage({ data });
        }
    }
    addEventListener("message", onMessage);
    document.body.appendChild(frame);
    await ready;
    return worker;
}

// Fetches a plain download for an isolated worker, from the page's HTTP cache.
// Never with credentials. Cross-origin URLs, and of the page's own origin
// only what the page itself chose: the app package and the Python runtime.
// Anything else is refused, and the worker fetches it as its own origin.
async function _proxyFetch(url, designatedUrls) {
    let u;
    try {
        u = new URL(url);
    } catch (e) {
        return { refused: true };
    }
    const sameOrigin = u.origin === location.origin;
    if (!/^https?:$/.test(u.protocol) ||
        (sameOrigin && !designatedUrls.some((d) => d.endsWith("/") ? u.href.startsWith(d) : u.href === d))) {
        return { refused: true };
    }
    try {
        const r = await fetch(u.href, { credentials: "omit" });
        const body = await r.arrayBuffer();
        return { status: r.status, statusText: r.statusText, headers: [...r.headers], body };
    } catch (e) {
        return { error: String(e) };
    }
}

// An isolated worker runs from a blob: URLs it gets must be absolute.
function _absoluteUrls(init) {
    const abs = (url) => url ? new URL(url, document.baseURI).href : url;
    const args = Object.assign({}, init.args || {});
    if (args.app_package_url) args.app_package_url = abs(args.app_package_url);
    return Object.assign({}, init, {
        pyodideUrl: abs(init.pyodideUrl),
        appPackageUrl: abs(init.appPackageUrl),
        args: args,
    });
}

// Same-origin URLs the proxy may fetch: chosen by the page, not the app.
function _designatedUrls(init) {
    const urls = [init.appPackageUrl, init.args && init.args.app_package_url].filter(Boolean);
    if (init.pyodideUrl) {
        // The runtime's folder, when the page serves it itself (--no-cdn).
        urls.push(init.pyodideUrl.slice(0, init.pyodideUrl.lastIndexOf("/") + 1));
    }
    return urls;
}
