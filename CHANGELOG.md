# Flet changelog

## 0.5.2

* Fix: Dispose controls only on session closed event
* Fix "There is no current event loop" error in auth module

## 0.5.1

* Fix `page` reference in `will_unmount` method.

## 0.5.0

* Fixed: Memory usage continues to increase. ([#1223](https://github.com/flet-dev/flet/issues/1223))
* Fixed: possible memory leak ([#969](https://github.com/flet-dev/flet/issues/969))
* Color values can contain opacity, e.g. `color=red,0.5` or `ft.colors.with_opacity(0.5, "red")`
* 1st class Flet charts based on fl_chart package ([#1255](https://github.com/flet-dev/flet/issues/1255))
* Pyodide 0.23
* Use named loggers in Python ([#1157](https://github.com/flet-dev/flet/issues/1157))
* Fix Contribution guide as PDM is no longer used ([#1124](https://github.com/flet-dev/flet/issues/1124))
* Added focus() method, focus and blur events to Elevated, Outlined, Text and Icon buttons ([#1079](https://github.com/flet-dev/flet/issues/1079))
* New Card props: color, shadow_color, surface_tint_color ([#1078](https://github.com/flet-dev/flet/issues/1078))
* Added WindowDragArea.maximizable property ([#1077](https://github.com/flet-dev/flet/issues/1077))
* Added Container.blur and Container.shadow properties ([#1076](https://github.com/flet-dev/flet/issues/1076))
* Add template for Q&A discussions ([#1070](https://github.com/flet-dev/flet/issues/1070))

## 0.4.2

* Fix reading versioninfo for PyInstaller 5.8.0
* Fix `Dropdown.disable` property

## 0.4.1

* Slider.round to round slider value on a label
* Fix page.client_storage.get_keys() timeout 
* Fix encode() import in PyInstaller integration
* Fix "ConnectionAbortedError" error on Windows
* Consistent licensing across the code - Apache 2.0
* Fix assets loading in a sub-directory app ([#1019](https://github.com/flet-dev/flet/issues/1019))
* Add --distpath option to flet pack and flet publish commands ([#1018](https://github.com/flet-dev/flet/issues/1018))
* Updating manifest.json when using flet publish ([#1014](https://github.com/flet-dev/flet/issues/1014))
* Fix "Address already in use" error on flet run hot reload ([#1007](https://github.com/flet-dev/flet/issues/1007))
* Force Python sub-process to run with UTF-8 encoding ([#1002](https://github.com/flet-dev/flet/issues/1002))
* Fix: View with content crashes in some routing scenarios ([#1001](https://github.com/flet-dev/flet/issues/1001))

## 0.4.0

* Changed re-connection logic to make hot reload work ([#971](https://github.com/flet-dev/flet/issues/971))
* Pyodide publishing fixes and improvements ([#953](https://github.com/flet-dev/flet/issues/953))
* feat: Add PaddingValue to __init__.py ([#936](https://github.com/flet-dev/flet/issues/936))
* Standalone Flet web apps with Pyodide ([#913](https://github.com/flet-dev/flet/issues/913))
* modified `tooltip` attribute from `prefere*` to `prefer*` ([#909](https://github.com/flet-dev/flet/issues/909))
* Fix unicode encoding in `FletTcpSocketServerProtocol`
* Fix relative assets path in desktop app
* PDM changed to Poetry
* Add `--hidden-import` option to `flet pack` command
* Add transparancy to matplotlib ([#889](https://github.com/flet-dev/flet/issues/889))
* Replace Fletd server for desktop apps with a light-weight Python shim ([#838](https://github.com/flet-dev/flet/issues/838))
* add default values in Border dataclass ([#883](https://github.com/flet-dev/flet/issues/883))
* Fix for issue in control.py when checking add command ([#835](https://github.com/flet-dev/flet/issues/835))
* Fix async pubsub ([#868](https://github.com/flet-dev/flet/issues/868))
* add: Border, BorderSide, Scale Offset, Rotate to `__init__.py` ([#866](https://github.com/flet-dev/flet/issues/866))
* Loading images from a local file ([#817](https://github.com/flet-dev/flet/issues/817))
* Asyncio support ([#799](https://github.com/flet-dev/flet/issues/799))
* Set filled=True when setting bgcolor in TextField ([#807](https://github.com/flet-dev/flet/issues/807))
* Page transition without animation ([#809](https://github.com/flet-dev/flet/issues/809))

## 0.3.2

* Fix `flet pack` command on Windows and macOS ([#795](https://github.com/flet-dev/flet/issues/795))

## 0.3.1

* Fixed Flutter package CHANGELOG and README.

## 0.3.0

* `flet pack` CLI to create app bundles with custom icons and metadata ([#770](https://github.com/flet-dev/flet/issues/770))
* Control comments ([#681](https://github.com/flet-dev/flet/issues/681))
* Fix MaterialState error in ButtonStyle ([#689](https://github.com/flet-dev/flet/issues/689))
* Flet CLI moved into separate module ([#679](https://github.com/flet-dev/flet/issues/679))
* Added BorderRadius to `__init__.py` ([#691](https://github.com/flet-dev/flet/issues/691))
* Added dense property to TextField and Dropdown controls ([#696](https://github.com/flet-dev/flet/issues/696))
* Correctly handle control replacement ([#710](https://github.com/flet-dev/flet/issues/710))
* Fix "replace" when moving children in the collection ([#711](https://github.com/flet-dev/flet/issues/711))
* Remove hard-coded colors in Markdown default code theme ([#731](https://github.com/flet-dev/flet/issues/731))
* Authorization should allow to override, such as request_token() methods ([#776](https://github.com/flet-dev/flet/issues/776))

## 0.2.4

* Use correct Flet viewer path when installed from a source package ([#675](https://github.com/flet-dev/flet/issues/675))
* add `ControlEvent` to `__init__.py` ([#657](https://github.com/flet-dev/flet/issues/657))
* fix: handle a few corner cases ([#503](https://github.com/flet-dev/flet/issues/503))

## 0.2.2

* Make `Control.offset` work without animation enabled ([#632](https://github.com/flet-dev/flet/issues/632))
* Added `Dropdown.alignment` property ([#630](https://github.com/flet-dev/flet/issues/630))
* Remove beartype runtime check for all `value` properties
* Fix `page.scroll` to allow None and strings
* Literals to Enums ([#626](https://github.com/flet-dev/flet/issues/626))
* `gapless_playback` is `True` by default for base64 images
* Ability to change border shape of FAB control ([#621](https://github.com/flet-dev/flet/issues/621))
* Added Slider's `on_change_start` and `on_change_end` events ([#620](https://github.com/flet-dev/flet/issues/620))
* DataTable control: 1-to-1 mapping to Flutter ([#583](https://github.com/flet-dev/flet/issues/583))
* Implemented `page.can_launch_url()` ([#582](https://github.com/flet-dev/flet/issues/582))
* Update project changelog from very beginning ([#581](https://github.com/flet-dev/flet/issues/581))
* Publish pre releases to pypi.org ([#579](https://github.com/flet-dev/flet/issues/579))
* Theming Slider control ([#573](https://github.com/flet-dev/flet/issues/573))

## 0.1.65

* Fixed: Floating Action Button now showing on top left ([#567](https://github.com/flet-dev/flet/issues/567))

## 0.1.64

* Using variable fonts ([#21](https://github.com/flet-dev/flet/issues/21))
* Old flet client app versions do not launch on Mac ([#161](https://github.com/flet-dev/flet/issues/161))
* NavigationBar control ([#193](https://github.com/flet-dev/flet/issues/193))
* `ResponsiveRow` control ([#227](https://github.com/flet-dev/flet/issues/227))
* Add code syntax highlighter to markdown ([#294](https://github.com/flet-dev/flet/issues/294))
* feature: add mouse scroll wheel event ([#354](https://github.com/flet-dev/flet/issues/354))
* Tooltip class ([#367](https://github.com/flet-dev/flet/issues/367))
* BottomSheet control ([#483](https://github.com/flet-dev/flet/issues/483))
* Fixed: Calling `update()` inside `Control.did_mount()` causes deadlock ([#489](https://github.com/flet-dev/flet/issues/489))
* Add `page.window_maximizable` ([#494](https://github.com/flet-dev/flet/issues/494))
* Add an ability to change font family of `TextField` ([#511](https://github.com/flet-dev/flet/issues/511))
* Feature: Theming Switch and Checkbox component ([#523](https://github.com/flet-dev/flet/issues/523))
* Change shape of AlertDialog ([#537](https://github.com/flet-dev/flet/issues/537))
* Fixed: Saving and retreiving a string value from client storage adds quotation marks ([#545](https://github.com/flet-dev/flet/issues/545))

## 0.1.63

* Matplotlib and Plotly Charts ([#509](https://github.com/flet-dev/flet/issues/509))
* make control a cooperative object ([#490](https://github.com/flet-dev/flet/issues/490))

## 0.1.62

* GestureDetector and other fixes ([#459](https://github.com/flet-dev/flet/issues/459))
* removed all problems except dart:html problem because it needs material html kind of thing ([#461](https://github.com/flet-dev/flet/issues/461))
* fix: ensure correct version is fetched in dev mode ([#443](https://github.com/flet-dev/flet/issues/443))
* Fix controls setter for empty list input ([#454](https://github.com/flet-dev/flet/issues/454))
* make ink=True behavior consistent with ink=False ([#427](https://github.com/flet-dev/flet/issues/427))

## 0.1.61

* Audio control ([#425](https://github.com/flet-dev/flet/issues/425))

## 0.1.60

* Authentication ([#335](https://github.com/flet-dev/flet/issues/335))
* Fix Flutter/Dart warnings ([#401](https://github.com/flet-dev/flet/issues/401), [#369](https://github.com/flet-dev/flet/issues/369), [#372](https://github.com/flet-dev/flet/issues/372))

## 0.1.59

* Fixes for Gallery ([#351](https://github.com/flet-dev/flet/issues/351))
* add data prop to PopupMenuItem [#327](https://github.com/flet-dev/flet/issues/327)

## 0.1.58

* Client storage ([#288](https://github.com/flet-dev/flet/issues/288))

## 0.1.57

* Container fixes ([#275](https://github.com/flet-dev/flet/pull/275))
* add error fix for those working with a source package ([#272](https://github.com/flet-dev/flet/pull/272))

## 0.1.56

* Windows: Clear FilePicker state before opening the dialog as it's blocking
* Reconnect with sessionID on desktop/mobile

## 0.1.55

* FilePicker and uploads ([#258](https://github.com/flet-dev/flet/pull/258))

## 0.1.54

Fix ElevatedButton regression ([9540beb](https://github.com/flet-dev/flet/commit/9540beb259b6d84d36a31da6799bad390861999d))

## [0.1.53](https://github.com/flet-dev/flet/releases/tag/v0.1.53)

* Desktop Flet app can be started with a hidden window
* New `page` properties to control window appearance and behavior
* New `Stack` properties
* Hot reload
* Platform details (`page.web`, `page.platform`)
* Customisable route transitions

## 0.1.52

* `RouteChangeEvent`, `ViewPopEvent`

## 0.1.51

* Fix container click event data object ([#198](https://github.com/flet-dev/flet/pull/198))
* Fix #196 bgcolor has no effect if FAB has a custom content ([#196](https://github.com/flet-dev/flet/pull/196))

## 0.1.50

* Linux ARM64 support for Flet runner app ([#189](https://github.com/flet-dev/flet/pull/189))
* Bugfix: Image control attribute src_base64 accepts str now ([#187](https://github.com/flet-dev/flet/pull/187))
* `ContainerTapEventData`
* Accessibility fixes ([#179](https://github.com/flet-dev/flet/pull/179))
* Fix button style updates

## 0.1.49

* Fix #173 - ValueError: mutable default ([#173](https://github.com/flet-dev/flet/pull/173))

## 0.1.48

* Fix container blend mode

## 0.1.47

* Remove `SnackBar.elevation`
* Implicit animations and AnimatedSwitcher control ([#162](https://github.com/flet-dev/flet/pull/162))
* Markdown and ShaderMask controls ([#160](https://github.com/flet-dev/flet/pull/160))
* Add slugify to utils ([#154](https://github.com/flet-dev/flet/pull/154))

## [0.1.46](https://github.com/flet-dev/flet/releases/tag/v0.1.46)

* New `Container` properties.
* New `ElevatedButton`, `OutlinedButton`, `TextButton` properties.
* New `IconButton` properties.
* New `ListTile` properties.
* New `Theme` properties.
* `hidden` value for `Column`, `Page`, `View`, `Row` and `View` controls - to enable scrolling but hide a scrollbar.
* New `TextField` and `Dropdown` properties.
* New `TextField` properties
* Fixed https://github.com/flet-dev/flet/issues/138 page.width and page.height are 0 on the first page load
* Fixed https://github.com/flet-dev/flet/issues/77 Allow partial theme updates
* Fixed https://github.com/flet-dev/flet/issues/140 Container on_click callback breaks containers without explicit size
* Fixed https://github.com/flet-dev/flet/issues/30 Assertion "lookup_hash_table" fails on ToDo App example
* Flutter SDK switched to `beta` channel.
* Fixed https://github.com/flet-dev/flet/issues/98 Changing app host/IP binding

## 0.1.43

* Switching between "hash" and "path" routing URL strategy ([#110](https://github.com/flet-dev/flet/pull/110))

## 0.1.42

* Navigation and Routing ([#95](https://github.com/flet-dev/flet/pull/95))

## 0.1.41

* Fix draggable.content_when_dragging

## 0.1.40

* Drag and Drop (https://github.com/flet-dev/flet/issues/62)
* Any control can be positioned absolutely inside Stack (https://github.com/flet-dev/flet/issues/60)
* Clickable Container (https://github.com/flet-dev/flet/issues/59)
* Added `page.pwa` property to detect if an app is running as PWA (https://github.com/flet-dev/flet/issues/58)

## 0.1.39

* Fix `UserControl._build()` call (https://github.com/flet-dev/flet/issues/52)

## 0.1.38

* Window Manager fix for Linux (https://github.com/flet-dev/flet/issues/44)

## 0.1.37

* Controlling application window (https://github.com/flet-dev/flet/issues/39)

## 0.1.36

* Page events allow multiple subscribers (https://github.com/flet-dev/flet/issues/38)
* page.rtl to control text directionality (https://github.com/flet-dev/flet/issues/37)

## 0.1.35

* Fix web_renderer arg
* Default webrenderer is canvaskit

## 0.1.34

* support "assets" dir for "onefile" PyInstaller
* Try packaging bin as data
* PyInstaller integration (https://github.com/flet-dev/flet/issues/34)

## 0.1.33

* Update control itself when isolated (https://github.com/flet-dev/flet/issues/31)

## 0.1.32

* Linux runner (https://github.com/flet-dev/flet/issues/29)

## 0.1.31

* User control (https://github.com/flet-dev/flet/issues/26)

## 0.1.30

* Upgraded to Flutter 3.0.2 (https://github.com/flet-dev/flet/issues/23)
* Custom fonts (https://github.com/flet-dev/flet/issues/22)

## 0.1.29

* PubSub (https://github.com/flet-dev/flet/issues/19)

## 0.1.28

* Support for Python 3.7 (https://github.com/flet-dev/flet/issues/16)
* Update logo-inkscape.svg
* Add executables to artifacts again
* Upload Fletd archives only, without binaries
* Fix links in Python SDK README (https://github.com/flet-dev/flet/issues/15)

## 0.1.27

* Fixed #10 (https://github.com/flet-dev/flet/issues/14)
* Row, Column and ListView spacing and scrolling improvements (https://github.com/flet-dev/flet/issues/13)
* Installing specific versions of Fletd and Flet apps for Python source distro (https://github.com/flet-dev/flet/issues/12)
* focus() method for TextField and Dropdown controls (https://github.com/flet-dev/flet/issues/11)

## 0.1.26

* Upload Flet client app to GitHub releases
* .focus() method for TextField and Dropdown
* Update fletd name to get download working (https://github.com/flet-dev/flet/issues/7)

## 0.1.25

* Sprint 1 (https://github.com/flet-dev/flet/pull/6)

## 0.1.24

* Fix expand for TextField and Dropdown

## 0.1.23

* app_store_connect_api_key with base64 key
* index.html with loading animation
* Upgrade Flutter 3.0.1
* Update AndroidManifest.xml
* Build to client's "build" folder
* Update Fastlane
* Building and publishing iOS Flutter app on AppVeyor

## 0.1.22

* TextField and Dropdown unlim size fix
* Python samples cleanup
* Merge pull request #5 from flet-dev/s1-ios
* Config flutter
* Fix FLET_PACKAGE_VERSION
* Fix iOS building for PR builds
* Restore complete yaml

## 0.1.20

* Row python examples
* More control examples
* Text max_lines

## 0.1.19

* Fix setting clipboard

## 0.1.18

* ListTile
* Card control
* Slight protocol optimization
* Control._set_attr_json
* Tabs selected_index
* Check collection controls for visibility
* NavigationRail selected_index
* NavigationRail control
* AppBar, NavigationRail - Python

## 0.1.17

* PopupMenuButton control
* Dividers example
* Filled buttons, dividers
* Filled elevated button
* Upgraded to Flutter 3.0
* Progress indicator samples
* Fix page size parsing
* page.content -> page.controls
* Expand can be True
* FAB
* bgColor for ImageButton
* CircleAvatar control added
* PWA icons all good
* Temp remove icons
* Large logo on an icon
* Icons updated
* Exponential reconnection logic, PWA icons
* Re-connecting flow

## 0.1.16

* Use canvaskit even on mobile for now
* Upgrade to Flutter 2.10.5
* Multiline textboxes done right

## 0.1.14

* Create a separate package for Alpine

## 0.1.13

* Add package for Alpine distro

## 0.1.12

* More general wheel package tags for Linux

## 0.1.11

* Icon browser done
* autofocus, on_focus, on_blur to Python classes
* Default Flet color theme
* autofocus, focus, blur to all form controls
* Remove tooltip from iconbutton
* ignoreChange sometimes
* Update container.dart
* Clipboard
* Make tooltip delay longer
* Tooltip property added to all visible controls
* Icons browser with outlined buttons

## 0.1.10

* GridView child_aspect_ratio
* Dynamic lazy building ListView and GridView controls
* Alignment parsing fixed

## 0.1.7

* App icons changed for web, windows and macos

## 0.1.5

* Open Flet client on Windows and MacOS only

## 0.1.4

* mkdir server/server/content