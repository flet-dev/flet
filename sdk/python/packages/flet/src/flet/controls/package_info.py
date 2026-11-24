from datetime import datetime
from typing import Optional

from flet.controls.base_control import value

__all__ = ["PackageInfo"]


@value(kw_only=True)
class PackageInfo:
    """
    Package metadata of the running application, as returned by
    :meth:`flet.Page.get_package_info`.

    For an app packaged with `flet build`, :attr:`version` and
    :attr:`build_number` are the values the app was built with: the
    `--build-version` and `--build-number` options, falling back to
    `project.version` (or `tool.poetry.version`) and `tool.flet.build_number`
    in `pyproject.toml`, and then to the defaults `1.0.0` and `1`.

    Note:
        Metadata comes from the Flutter client that renders the app, not from
        the Python program. When the app is not packaged with `flet build`, it
        describes that client:

        - **`flet run`** - the Flet desktop client.
        - **`flet run --android` or `--ios`** - the Flet app on the device
            that runs the program.
        - **Web** (`flet run --web`, a web server, or `flet publish`) - the
            Flet web client, read from its `version.json`. A
            `flet build web` app returns its own metadata.

        Values that a platform doesn't provide are empty strings, or `None`
        for optional fields.
    """

    app_name: str
    """
    The application name shown to users.

    - **iOS/macOS** - `CFBundleDisplayName`, falling back to `CFBundleName`.
    - **Android** - `application/label` in `AndroidManifest.xml`.
    - **Web/Linux** - `app_name` from the build's `version.json`.
    - **Windows** - `ProductName` of the executable.
    """

    package_name: str
    """
    The application's package or bundle identifier.

    - **iOS/macOS** - bundle identifier, for example `"com.mycompany.myapp"`.
    - **Android** - `applicationId`, for example `"com.mycompany.myapp"`.
    - **Web/Linux** - `package_name` from the build's `version.json`.
    - **Windows** - `InternalName` of the executable.
    """

    version: str
    """
    The application version shown to users, for example `"1.2.3"`.

    - **iOS/macOS** - `CFBundleShortVersionString`.
    - **Android** - `versionName`.
    - **Web/Linux** - `version` from the build's `version.json`.
    - **Windows** - `ProductVersion` of the executable, without the build number.
    """

    build_number: str
    """
    The build number, an internal version identifier, for example `"42"`.

    - **iOS/macOS** - `CFBundleVersion`. On iOS, it equals :attr:`version`
        when the app has no build number.
    - **Android** - `versionCode`.
    - **Web/Linux** - `build_number` from the build's `version.json`.
    - **Windows** - the build number part of the executable's `ProductVersion`.
    """

    build_signature: str
    """
    The SHA-256 signature (hex) of the key the app was signed with.

    Android only; an empty string on other platforms.
    """

    installer_store: Optional[str] = None
    """
    Identifies the store the application was installed from.

    - **Android** - package name of the installer, for example
        `"com.android.vending"` for Google Play; `None` if the app was sideloaded.
    - **iOS** - `"com.apple"`, `"com.apple.testflight"` for TestFlight
        builds, or `"com.apple.simulator"` in the iOS Simulator.
    - **Other platforms** - `None`.
    """

    install_time: Optional[datetime] = None
    """
    The time the application was installed.

    - **Android** - `PackageManager.firstInstallTime`.
    - **iOS** - creation time of the app's documents directory.
    - **macOS** - creation time of the app's documents directory when
        sandboxed, otherwise the last modification time of the app bundle.
    - **Windows/Linux** - creation time of the app executable, falling back to
        its last modification time.
    - **Web** - `None`.
    """

    update_time: Optional[datetime] = None
    """
    The time the application was last updated.

    - **Android** - `PackageManager.lastUpdateTime`.
    - **iOS/macOS** - last modification time of the app bundle.
    - **Windows/Linux** - last modification time of the app executable.
    - **Web** - `None`.
    """
