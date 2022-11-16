# Flet changelog

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

## [0.1.0](https://pypi.org/project/flet/0.1.0) - Mar 30, 2022
