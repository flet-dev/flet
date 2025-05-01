{{flutter_js}}
{{flutter_build_config}}

var loading = document.querySelector('#loading');

var config = {};
if (fletConfig.webRenderer != "auto") {
    config.renderer = fletConfig.webRenderer;
}
if (fletConfig.noCdn) {
    config.canvasKitBaseUrl = fletConfig.canvasKitBaseUrl;
}
_flutter.loader.load({
    config: config,
    serviceWorkerSettings: {
        serviceWorkerVersion: {{flutter_service_worker_version}},
    },
    onEntrypointLoaded: async function (engineInitializer) {
        loading.classList.add('main_done');
        const engine = await engineInitializer.initializeEngine({
            useColorEmoji: fletConfig.useColorEmoji,
            multiViewEnabled: fletConfig.multiView
        });

        loading.classList.add('init_done');
        fletConfig.flutterApp = await engine.runApp();
        fletConfig.flutterAppResolve(fletConfig.flutterApp);

        window.setTimeout(function () {
            loading.remove();
        }, 200);
    }
});
