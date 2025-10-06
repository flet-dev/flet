Flet controls based on 3rd-party Flutter packages that used to be a part of Flet repository, now have been moved to separate repos and published on pypi:

* [flet-ads](https://pypi.org/project/flet-ads/)
* [flet-audio](https://pypi.org/project/flet-audio/)
* [flet-audio-recorder](https://pypi.org/project/flet-audio-recorder/)
* [flet-charts](https://pypi.org/project/flet-charts/)
* [flet-datatable2](https://pypi.org/project/flet-datatable2/)
* [flet-flashlight](https://pypi.org/project/flet-flashlight/)
* [flet-geolocator](https://pypi.org/project/flet-geolocator/)
* [flet-lottie](https://pypi.org/project/flet-lottie/)
* [flet-map](https://pypi.org/project/flet-map/)
* [flet-permission-handler](https://pypi.org/project/flet-permission-handler/)
* [flet-rive](https://pypi.org/project/flet-rive/)
* [flet-video](https://pypi.org/project/flet-video/)
* [flet-webview](https://pypi.org/project/flet-webview/)

To use a built-in Flet extension in your project, add it to the `dependencies` section of your `pyproject.toml` file, for example:

```
dependencies = [
  "flet-audio",
  "flet>=0.26.0",
]
```
