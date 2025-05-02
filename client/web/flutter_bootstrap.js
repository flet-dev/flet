{{flutter_js}}
{{flutter_build_config}}

var loading = document.querySelector('#loading');

var config = {};
if (flet.webRenderer != "auto") {
    config.renderer = flet.webRenderer;
}
if (flet.noCdn) {
    config.canvasKitBaseUrl = flet.canvasKitBaseUrl;
}
_flutter.loader.load({
    config: config,
    serviceWorkerSettings: {
        serviceWorkerVersion: {{flutter_service_worker_version}},
    },
    onEntrypointLoaded: async function (engineInitializer) {
        loading.classList.add('main_done');
        const engine = await engineInitializer.initializeEngine({
            useColorEmoji: flet.useColorEmoji,
            multiViewEnabled: flet.multiView
        });

        loading.classList.add('init_done');
        flet.flutterApp = await engine.runApp();
        flet.flutterAppResolve(flet.flutterApp);

        window.setTimeout(function () {
            loading.remove();
        }, 200);
    }
});
