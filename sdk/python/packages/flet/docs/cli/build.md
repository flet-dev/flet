---
title: build
sidebar_label: build
---

This command is used to package a Flet application for distribution. You can find it's guide [here](/docs/publish).

```
usage: flet build [-h] [-v] [--arch TARGET_ARCH [TARGET_ARCH ...]]
                  [--exclude EXCLUDE [EXCLUDE ...]] [-o OUTPUT_DIR] [--clear-cache]
                  [--project PROJECT_NAME] [--description DESCRIPTION] [--product PRODUCT_NAME]
                  [--org ORG_NAME] [--bundle-id BUNDLE_ID] [--company COMPANY_NAME]
                  [--copyright COPYRIGHT]
                  [--android-adaptive-icon-background ANDROID_ADAPTIVE_ICON_BACKGROUND]
                  [--splash-color SPLASH_COLOR] [--splash-dark-color SPLASH_DARK_COLOR]
                  [--no-web-splash] [--no-ios-splash] [--no-android-splash]
                  [--ios-team-id IOS_TEAM_ID] [--ios-export-method IOS_EXPORT_METHOD]
                  [--ios-provisioning-profile IOS_PROVISIONING_PROFILE]
                  [--ios-signing-certificate IOS_SIGNING_CERTIFICATE] [--base-url BASE_URL]
                  [--web-renderer {canvaskit,html}] [--use-color-emoji]
                  [--route-url-strategy {path,hash}]
                  [--pwa-background-color PWA_BACKGROUND_COLOR]
                  [--pwa-theme-color PWA_THEME_COLOR] [--split-per-abi] [--compile-app]
                  [--compile-packages] [--cleanup-app]
                  [--cleanup-app-files [CLEANUP_APP_FILES ...]] [--cleanup-packages]
                  [--cleanup-package-files [CLEANUP_PACKAGE_FILES ...]]
                  [--flutter-build-args [FLUTTER_BUILD_ARGS ...]]
                  [--source-packages SOURCE_PACKAGES [SOURCE_PACKAGES ...]]
                  [--info-plist INFO_PLIST [INFO_PLIST ...]]
                  [--macos-entitlements MACOS_ENTITLEMENTS [MACOS_ENTITLEMENTS ...]]
                  [--android-features ANDROID_FEATURES [ANDROID_FEATURES ...]]
                  [--android-permissions ANDROID_PERMISSIONS [ANDROID_PERMISSIONS ...]]
                  [--android-meta-data ANDROID_META_DATA [ANDROID_META_DATA ...]]
                  [--permissions {location,camera,microphone,photo_library} [{location,camera,microphone,photo_library} ...]]
                  [--deep-linking-scheme DEEP_LINKING_SCHEME]
                  [--deep-linking-host DEEP_LINKING_HOST]
                  [--android-signing-key-store ANDROID_SIGNING_KEY_STORE]
                  [--android-signing-key-store-password ANDROID_SIGNING_KEY_STORE_PASSWORD]
                  [--android-signing-key-password ANDROID_SIGNING_KEY_PASSWORD]
                  [--android-signing-key-alias ANDROID_SIGNING_KEY_ALIAS]
                  [--build-number BUILD_NUMBER] [--build-version BUILD_VERSION]
                  [--module-name MODULE_NAME] [--template TEMPLATE] [--template-dir TEMPLATE_DIR]
                  [--template-ref TEMPLATE_REF] [--show-platform-matrix] [--no-rich-output]
                  [--skip-flutter-doctor]
                  {macos,linux,windows,web,apk,aab,ipa} [python_app_path]

Build an executable app or install bundle.

positional arguments:
  {macos,linux,windows,web,apk,aab,ipa}
                        the type of a package or target platform to build
  python_app_path       path to a directory with a Python program

options:
  -h, --help            show this help message and exit
  -v, --verbose         -v for detailed output and -vv for more detailed
  --arch TARGET_ARCH [TARGET_ARCH ...]
                        package for specific architectures only. Used with Android and macOS
                        builds only.
  --exclude EXCLUDE [EXCLUDE ...]
                        exclude files and directories from a Python app package
  -o OUTPUT_DIR, --output OUTPUT_DIR
                        where to put resulting executable or bundle (default is
                        <python_app_directory>/build/<target_platform>)
  --clear-cache         clear build cache
  --project PROJECT_NAME
                        project name for executable or bundle
  --description DESCRIPTION
                        the description to use for executable or bundle
  --product PRODUCT_NAME
                        project display name that is shown in window titles and about app dialogs
  --org ORG_NAME        org name in reverse domain name notation, e.g. "com.mycompany" - combined
                        with project name and used as an iOS and Android bundle ID
  --bundle-id BUNDLE_ID
                        bundle ID for the application, e.g. "com.mycompany.app-name" - used as an
                        iOS, Android, macOS and Linux bundle ID
  --company COMPANY_NAME
                        company name to display in about app dialogs
  --copyright COPYRIGHT
                        copyright text to display in about app dialogs
  --android-adaptive-icon-background ANDROID_ADAPTIVE_ICON_BACKGROUND
                        the color which will be used to fill out the background of the adaptive
                        icon
  --splash-color SPLASH_COLOR
                        background color of app splash screen on iOS, Android and web
  --splash-dark-color SPLASH_DARK_COLOR
                        background color in dark mode of app splash screen on iOS, Android and
                        web
  --no-web-splash       disable web app splash screen
  --no-ios-splash       disable iOS app splash screen
  --no-android-splash   disable Android app splash screen
  --ios-team-id IOS_TEAM_ID
                        team ID to sign iOS bundle (ipa only)
  --ios-export-method IOS_EXPORT_METHOD
                        export method for iOS app. Default is "debugging"
  --ios-provisioning-profile IOS_PROVISIONING_PROFILE
                        provisioning profile name or UUID that used to sign and export iOS app
  --ios-signing-certificate IOS_SIGNING_CERTIFICATE
                        provide a certificate name, SHA-1 hash, or automatic selector to use for
                        signing iOS app bundle
  --base-url BASE_URL   base URL for the app (web only)
  --web-renderer {canvaskit,html}
                        renderer to use (web only)
  --use-color-emoji     enables color emojis with CanvasKit renderer (web only)
  --route-url-strategy {path,hash}
                        URL routing strategy (web only)
  --pwa-background-color PWA_BACKGROUND_COLOR
                        an initial background color for your web application
  --pwa-theme-color PWA_THEME_COLOR
                        default color for your web application's user interface
  --split-per-abi       whether to split the APKs per ABIs.
  --compile-app         compile app's .py files to .pyc
  --compile-packages    compile site packages' .py files to .pyc
  --cleanup-app         remove unnecessary app files upon packaging
  --cleanup-app-files [CLEANUP_APP_FILES ...]
                        the list of globs to delete extra app files and directories
  --cleanup-packages    remove unnecessary package files upon packaging
  --cleanup-package-files [CLEANUP_PACKAGE_FILES ...]
                        the list of globs to delete extra package files and directories
  --flutter-build-args [FLUTTER_BUILD_ARGS ...]
                        additional arguments for flutter build command
  --source-packages SOURCE_PACKAGES [SOURCE_PACKAGES ...]
                        the list of Python packages to install from source distributions
  --info-plist INFO_PLIST [INFO_PLIST ...]
                        the list of "<key>=<value>|True|False" pairs to add to Info.plist for
                        macOS and iOS builds
  --macos-entitlements MACOS_ENTITLEMENTS [MACOS_ENTITLEMENTS ...]
                        the list of "<key>=<value>|True|False" entitlements for macOS builds
  --android-features ANDROID_FEATURES [ANDROID_FEATURES ...]
                        the list of "<feature_name>=True|False" features to add to
                        AndroidManifest.xml
  --android-permissions ANDROID_PERMISSIONS [ANDROID_PERMISSIONS ...]
                        the list of "<permission_name>=True|False" permissions to add to
                        AndroidManifest.xml
  --android-meta-data ANDROID_META_DATA [ANDROID_META_DATA ...]
                        the list of "<name>=<value>" app meta-data entries to add to
                        AndroidManifest.xml
  --permissions {location,camera,microphone,photo_library} [{location,camera,microphone,photo_library} ...]
                        the list of cross-platform permissions for iOS, Android and macOS apps
  --deep-linking-scheme DEEP_LINKING_SCHEME
                        deep linking URL scheme to configure for iOS and Android builds, i.g.
                        "https" or "myapp"
  --deep-linking-host DEEP_LINKING_HOST
                        deep linking URL host for iOS and Android builds
  --android-signing-key-store ANDROID_SIGNING_KEY_STORE
                        path to an upload keystore .jks file for Android apps
  --android-signing-key-store-password ANDROID_SIGNING_KEY_STORE_PASSWORD
                        Android signing store password
  --android-signing-key-password ANDROID_SIGNING_KEY_PASSWORD
                        Android signing key password
  --android-signing-key-alias ANDROID_SIGNING_KEY_ALIAS
                        Android signing key alias. Default is "upload".
  --build-number BUILD_NUMBER
                        build number - an identifier used as an internal version number
  --build-version BUILD_VERSION
                        build version - a "x.y.z" string used as the version number shown to
                        users
  --module-name MODULE_NAME
                        python module name with an app entry point
  --template TEMPLATE   a directory containing Flutter bootstrap template, or a URL to a git
                        repository template
  --template-dir TEMPLATE_DIR
                        relative path to a Flutter bootstrap template in a repository
  --template-ref TEMPLATE_REF
                        the branch, tag or commit ID to checkout after cloning the repository
                        with Flutter bootstrap template
  --show-platform-matrix
                        displays the build platform matrix in a table, then exits
  --no-rich-output      disables rich output and uses plain text instead
  --skip-flutter-doctor
                        whether to skip running Flutter doctor in failed builds
```
