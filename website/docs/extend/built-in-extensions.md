---
title: "Built-in Extensions"
---

Flet controls based on 3rd-party Flutter packages are published on PyPI as separate packages. Their source lives in the [`sdk/python/packages`](https://github.com/flet-dev/flet/tree/main/sdk/python/packages) folder of the Flet repository:

* [flet-ads](https://pypi.org/project/flet-ads/)
* [flet-audio](https://pypi.org/project/flet-audio/)
* [flet-audio-recorder](https://pypi.org/project/flet-audio-recorder/)
* [flet-camera](https://pypi.org/project/flet-camera/)
* [flet-charts](https://pypi.org/project/flet-charts/)
* [flet-code-editor](https://pypi.org/project/flet-code-editor/)
* [flet-color-pickers](https://pypi.org/project/flet-color-pickers/)
* [flet-datatable2](https://pypi.org/project/flet-datatable2/)
* [flet-flashlight](https://pypi.org/project/flet-flashlight/)
* [flet-geolocator](https://pypi.org/project/flet-geolocator/)
* [flet-lottie](https://pypi.org/project/flet-lottie/)
* [flet-local-auth](https://pypi.org/project/flet-local-auth/)
* [flet-map](https://pypi.org/project/flet-map/)
* [flet-permission-handler](https://pypi.org/project/flet-permission-handler/)
* [flet-rive](https://pypi.org/project/flet-rive/)
* [flet-secure-storage](https://pypi.org/project/flet-secure-storage/)
* [flet-spinkit](https://pypi.org/project/flet-spinkit/)
* [flet-video](https://pypi.org/project/flet-video/)
* [flet-webview](https://pypi.org/project/flet-webview/)

To use a built-in Flet extension in your project, add it to the `dependencies` section of your `pyproject.toml` file, for example:

```
dependencies = [
  "flet-audio",
  "flet>=1.0.0",
]
```
