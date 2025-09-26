{{flutter_js}}
{{flutter_build_config}}

var loading = document.querySelector('#loading');

var flutterConfig = {
    multiViewEnabled: flet.multiView,
    entryPointBaseUrl: flet.entryPointBaseUrl,
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
        serviceWorkerVersion: {{flutter_service_worker_version}},
    },
    onEntrypointLoaded: async function (engineInitializer) {
        loading.classList.add('main_done');
        const engine = await engineInitializer.initializeEngine(flutterConfig);

        loading.classList.add('init_done');
        flet.flutterApp = await engine.runApp();
        flet.flutterAppResolve(flet.flutterApp);

        window.setTimeout(function () {
            loading.remove();
        }, 200);
    }
});
