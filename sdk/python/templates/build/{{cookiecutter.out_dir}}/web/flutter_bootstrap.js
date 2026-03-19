{{ '{{flutter_js}}' }}
{{ '{{flutter_build_config}}' }}

var flutterConfig = {
    multiViewEnabled: flet.multiView,
    assetBase: flet.assetBase
};
if (flet.webRenderer != "auto") {
    flutterConfig.renderer = flet.webRenderer;
}
if (flet.noCdn) {
    flutterConfig.canvasKitBaseUrl = flet.canvasKitBaseUrl;
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
