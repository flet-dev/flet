{{flutter_js}}
{{flutter_build_config}}

var loading = document.querySelector('#loading');
_flutter.loader.load({
    serviceWorkerSettings: {
        serviceWorkerVersion: {{flutter_service_worker_version}},
    },
    onEntrypointLoaded: async function (engineInitializer) {
        loading.classList.add('main_done');
        const appRunner = await engineInitializer.initializeEngine({useColorEmoji: useColorEmoji});

        loading.classList.add('init_done');
        await appRunner.runApp();

        window.setTimeout(function () {
            loading.remove();
        }, 200);
    }
});