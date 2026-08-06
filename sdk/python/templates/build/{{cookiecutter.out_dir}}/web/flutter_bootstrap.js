{{ '{{flutter_js}}' }}
{{ '{{flutter_build_config}}' }}

var flutterConfig = {
    multiViewEnabled: flet.multiView,
    assetBase: flet.assetBase
};
if (flet.webRenderer != "auto") {
    flutterConfig.renderer = flet.webRenderer;
}
// Keyed off the values themselves, not off `flet.noCdn`: a host serving its
// own copy of the runtime can point these anywhere without pretending the app
// was built with `--no-cdn`. Left unset, Flutter falls back to gstatic for
// CanvasKit and to Google Fonts for the Noto fallbacks.
if (flet.canvasKitBaseUrl) {
    flutterConfig.canvasKitBaseUrl = flet.canvasKitBaseUrl;
}
if (flet.fontFallbackBaseUrl) {
    flutterConfig.fontFallbackBaseUrl = flet.fontFallbackBaseUrl;
}

_flutter.loader.load({
    config: flutterConfig,
    serviceWorkerSettings: {
        serviceWorkerVersion: {{ '{{flutter_service_worker_version}}' }},
    },
    onEntrypointLoaded: async function (engineInitializer) {
        const engine = await engineInitializer.initializeEngine(flutterConfig);
        flet.flutterApp = await engine.runApp();
        flet.flutterAppResolve(flet.flutterApp);
    }
});
