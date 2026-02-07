import 'dart:async';

import 'package:flutter/widgets.dart';
import 'package:window_manager/window_manager.dart';

import '../flet_backend.dart';
import '../flet_service.dart';
import '../utils/alignment.dart';
import '../utils/colors.dart';
import '../utils/desktop.dart';
import '../utils/numbers.dart';
import '../utils/platform.dart';
import '../utils/theme.dart';
import '../utils/window.dart';

class WindowService extends FletService with WindowListener {
  final Completer<void> _initWindowStateCompleter = Completer<void>();
  Future<void> _pendingWindowUpdate = Future.value();
  String? _title;
  Color? _bgColor;
  double? _width;
  double? _height;
  double? _minWidth;
  double? _minHeight;
  double? _maxWidth;
  double? _maxHeight;
  double? _top;
  double? _left;
  double? _opacity;
  double? _aspectRatio;
  Brightness? _brightness;
  bool? _minimizable;
  bool? _maximizable;
  bool? _fullScreen;
  bool? _movable;
  bool? _resizable;
  bool? _alwaysOnTop;
  bool? _alwaysOnBottom;
  bool? _preventClose;
  bool? _minimized;
  bool? _maximized;
  Alignment? _alignment;
  String? _badgeLabel;
  String? _icon;
  bool? _hasShadow;
  bool? _visible;
  bool? _focused;
  bool? _frameless;
  bool? _titleBarHidden;
  bool? _titleBarButtonsHidden;
  bool? _skipTaskBar;
  double? _progressBar;
  bool? _ignoreMouseEvents;
  bool _listenersAttached = false;

  WindowService({required super.control});

  @override
  void init() {
    super.init();
    if (!isDesktopPlatform()) {
      return;
    }
    debugPrint("WindowService(${control.id}).init");
    _initWindowState();
  }

  Future<void> _initWindowState() async {
    try {
      final windowState = await getWindowState();
      _width = windowState.width;
      _height = windowState.height;
      _top = windowState.top;
      _left = windowState.left;
      _opacity = windowState.opacity;
      _minimizable = windowState.minimizable;
      _maximizable = windowState.maximizable;
      _fullScreen = windowState.fullScreen;
      _resizable = windowState.resizable;
      _alwaysOnTop = windowState.alwaysOnTop;
      _preventClose = windowState.preventClose;
      _minimized = windowState.minimized;
      _maximized = windowState.maximized;
      _visible = windowState.visible;
      _focused = windowState.focused;
      _skipTaskBar = windowState.skipTaskBar;

      if (!_listenersAttached) {
        windowManager.addListener(this);
        control.addInvokeMethodListener(_invokeMethod);
        control.parent?.addListener(_onPageChanged);
        _listenersAttached = true;
      }

      if (!_initWindowStateCompleter.isCompleted) {
        _initWindowStateCompleter.complete();
      }

      _scheduleWindowUpdate();
    } catch (e) {
      debugPrint("Error initializing window state: $e");
    }
  }

  @override
  void update() {
    if (!isDesktopPlatform()) {
      return;
    }
    _scheduleWindowUpdate();
  }

  void _onPageChanged() {
    if (!isDesktopPlatform()) {
      return;
    }
    final title = control.parent?.getString("title");
    if (title != null && title != _title) {
      _scheduleWindowUpdate();
    }
  }

  void _scheduleWindowUpdate() {
    _pendingWindowUpdate = _pendingWindowUpdate.catchError((_) {}).then((_) {
      if (_initWindowStateCompleter.isCompleted) {
        return _updateWindow(control.backend);
      }
      return _initWindowStateCompleter.future
          .then((_) => _updateWindow(control.backend));
    });
  }

  Future<void> _updateWindow(FletBackend backend) async {
    if (!isDesktopPlatform()) {
      return;
    }
    try {
      var parent = control.parent;
      if (parent == null) {
        return;
      }
      var title = parent.getString("title");
      var bgColor = control.getColor("bgcolor", null);
      var width = control.getDouble("width");
      var height = control.getDouble("height");
      var minWidth = control.getDouble("min_width");
      var minHeight = control.getDouble("min_height");
      var maxWidth = control.getDouble("max_width");
      var maxHeight = control.getDouble("max_height");
      var top = control.getDouble("top");
      var left = control.getDouble("left");
      var fullScreen = control.getBool("full_screen");
      var minimized = control.getBool("minimized");
      var maximized = control.getBool("maximized");
      var alignment = control.getAlignment("alignment");
      var badgeLabel = control.getString("badge_label");
      var icon = control.getString("icon");
      var hasShadow = control.getBool("shadow");
      var opacity = control.getDouble("opacity");
      var aspectRatio = control.getDouble("aspect_ratio");
      var brightness = control.getBrightness("brightness");
      var minimizable = control.getBool("minimizable");
      var maximizable = control.getBool("maximizable");
      var alwaysOnTop = control.getBool("always_on_top");
      var alwaysOnBottom = control.getBool("always_on_bottom");
      var resizable = control.getBool("resizable");
      var movable = control.getBool("movable");
      var preventClose = control.getBool("prevent_close");
      var titleBarHidden = control.getBool("title_bar_hidden");
      var titleBarButtonsHidden =
          control.getBool("title_bar_buttons_hidden", false)!;
      var visible = control.getBool("visible");
      var focused = control.getBool("focused");
      var skipTaskBar = control.getBool("skip_task_bar");
      var frameless = control.getBool("frameless");
      var progressBar = control.getDouble("progress_bar");
      var ignoreMouseEvents = control.getBool("ignore_mouse_events");

      if (title != null && title != _title) {
        await setWindowTitle(title);
        _title = title;
      }

      if (bgColor != null && bgColor != _bgColor) {
        await setWindowBackgroundColor(bgColor);
        _bgColor = bgColor;
      }

      if ((width != null || height != null) &&
          (width != _width || height != _height) &&
          fullScreen != true &&
          (!isMacOSDesktop() ||
              (isMacOSDesktop() && maximized != true && minimized != true))) {
        await setWindowSize(width, height);
        _width = width;
        _height = height;
      }

      if ((minWidth != null || minHeight != null) &&
          (minWidth != _minWidth || minHeight != _minHeight)) {
        await setWindowMinSize(minWidth, minHeight);
        _minWidth = minWidth;
        _minHeight = minHeight;
      }

      if ((maxWidth != null || maxHeight != null) &&
          (maxWidth != _maxWidth || maxHeight != _maxHeight)) {
        await setWindowMaxSize(maxWidth, maxHeight);
        _maxWidth = maxWidth;
        _maxHeight = maxHeight;
      }

      if ((top != null || left != null) &&
          (top != _top || left != _left) &&
          fullScreen != true &&
          (!isMacOSDesktop() ||
              (isMacOSDesktop() && maximized != true && minimized != true))) {
        await setWindowPosition(top, left);
        _top = top;
        _left = left;
      }

      if (opacity != null && opacity != _opacity) {
        await setWindowOpacity(opacity);
        _opacity = opacity;
      }

      if (aspectRatio != null && aspectRatio != _aspectRatio) {
        await setWindowAspectRatio(aspectRatio);
        _aspectRatio = aspectRatio;
      }

      if (brightness != null && brightness != _brightness) {
        await setWindowBrightness(brightness);
        _brightness = brightness;
      }

      if (minimizable != null && minimizable != _minimizable) {
        await setWindowMinimizability(minimizable);
        _minimizable = minimizable;
      }

      if (minimized != _minimized) {
        if (minimized == true) {
          await minimizeWindow();
        } else if (minimized == false && maximized != true) {
          await restoreWindow();
        }
        _minimized = minimized;
      }

      if (maximizable != null && maximizable != _maximizable) {
        await setWindowMaximizability(maximizable);
        _maximizable = maximizable;
      }

      if (maximized != _maximized) {
        if (maximized == true) {
          await maximizeWindow();
        } else if (maximized == false) {
          await unmaximizeWindow();
        }
        _maximized = maximized;
      }

      if (alignment != null && alignment != _alignment) {
        await setWindowAlignment(alignment);
        _alignment = alignment;
      }

      if (badgeLabel != null && badgeLabel != _badgeLabel) {
        await setWindowBadgeLabel(badgeLabel);
        _badgeLabel = badgeLabel;
      }

      if (icon != null && icon != _icon) {
        var iconAssetSrc = backend.getAssetSource(icon);
        await setWindowIcon(iconAssetSrc.path);
        _icon = icon;
      }

      if (hasShadow != null && hasShadow != _hasShadow) {
        await setWindowShadow(hasShadow);
        _hasShadow = hasShadow;
      }

      if (resizable != null && resizable != _resizable) {
        await setWindowResizability(resizable);
        _resizable = resizable;
      }

      if (movable != null && movable != _movable) {
        await setWindowMovability(movable);
        _movable = movable;
      }

      if (fullScreen != null && fullScreen != _fullScreen) {
        await setWindowFullScreen(fullScreen);
        _fullScreen = fullScreen;
      }

      if (alwaysOnTop != null && alwaysOnTop != _alwaysOnTop) {
        await setWindowAlwaysOnTop(alwaysOnTop);
        _alwaysOnTop = alwaysOnTop;
      }

      if (alwaysOnBottom != null && alwaysOnBottom != _alwaysOnBottom) {
        await setWindowAlwaysOnBottom(alwaysOnBottom);
        _alwaysOnBottom = alwaysOnBottom;
      }

      if (preventClose != null && preventClose != _preventClose) {
        await setWindowPreventClose(preventClose);
        _preventClose = preventClose;
      }

      final effectiveTitleBarHidden =
          titleBarHidden ?? _titleBarHidden ?? false;
      if (effectiveTitleBarHidden != _titleBarHidden ||
          titleBarButtonsHidden != _titleBarButtonsHidden) {
        await setWindowTitleBarVisibility(
            effectiveTitleBarHidden, titleBarButtonsHidden);
        _titleBarHidden = effectiveTitleBarHidden;
        _titleBarButtonsHidden = titleBarButtonsHidden;
      }

      if (visible != null && visible != _visible) {
        if (visible == true) {
          await showWindow();
        } else {
          await hideWindow();
        }
        _visible = visible;
      }

      if (focused != null && focused != _focused) {
        if (focused == true) {
          await focusWindow();
        } else {
          await blurWindow();
        }
        _focused = focused;
      }

      if (frameless != null && frameless != _frameless) {
        if (frameless) {
          await setWindowFrameless();
        } else {
          // Restore non-frameless window chrome using cached state
          await setWindowTitleBarVisibility(
            _titleBarHidden ?? false,
            _titleBarButtonsHidden,
          );
        }
        _frameless = frameless;
      }

      if (progressBar != _progressBar) {
        // window_manager uses -1 to clear the native progress indicator.
        await setWindowProgressBar(progressBar ?? -1);
        _progressBar = progressBar;
      }

      if (skipTaskBar != null && skipTaskBar != _skipTaskBar) {
        await setWindowSkipTaskBar(skipTaskBar);
        _skipTaskBar = skipTaskBar;
      }

      if (ignoreMouseEvents != null &&
          ignoreMouseEvents != _ignoreMouseEvents) {
        await setIgnoreMouseEvents(ignoreMouseEvents);
        _ignoreMouseEvents = ignoreMouseEvents;
      }
    } catch (e) {
      debugPrint("Error updating window: $e");
    }
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    switch (name) {
      case "wait_until_ready_to_show":
        await waitUntilReadyToShow();
        break;
      case "to_front":
        windowToFront();
        break;
      case "center":
        await _pendingWindowUpdate;
        await centerWindow();
        break;
      case "close":
        await closeWindow();
        break;
      case "destroy":
        await destroyWindow();
        break;
      case "start_dragging":
        await startDraggingWindow();
        break;
      case "start_resizing":
        var edge = parseWindowResizeEdge(args["edge"]);
        if (edge != null) {
          await startResizingWindow(edge);
        }
        break;
      default:
        throw Exception("Unknown method Window.$name");
    }
  }

  @override
  void dispose() {
    if (_listenersAttached) {
      windowManager.removeListener(this);
      control.removeInvokeMethodListener(_invokeMethod);
      control.parent?.removeListener(_onPageChanged);
      _listenersAttached = false;
    }
    super.dispose();
  }

  @override
  void onWindowEvent(String eventName) {
    if (!isDesktopPlatform()) {
      return;
    }
    if (["resize", "resized", "move"].contains(eventName)) {
      return;
    }
    getWindowState().then((state) {
      _width = state.width;
      _height = state.height;
      _top = state.top;
      _left = state.left;
      _opacity = state.opacity;
      _minimized = state.minimized;
      _maximized = state.maximized;
      _minimizable = state.minimizable;
      _maximizable = state.maximizable;
      _fullScreen = state.fullScreen;
      _resizable = state.resizable;
      _alwaysOnTop = state.alwaysOnTop;
      _preventClose = state.preventClose;
      _visible = state.visible;
      _focused = state.focused;
      _skipTaskBar = state.skipTaskBar;

      control.backend.onWindowEvent(eventName, state);
    });
  }
}
