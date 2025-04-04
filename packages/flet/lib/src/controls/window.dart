import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:window_manager/window_manager.dart';

import '../extensions/control.dart';
import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/desktop.dart';

class WindowControl extends StatefulWidget {
  final Control control;
  const WindowControl({super.key, required this.control});

  @override
  State<WindowControl> createState() => _WindowControlState();
}

class _WindowControlState extends State<WindowControl> with WindowListener {
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
  bool? _skipTaskBar;
  double? _progressBar;
  bool? _ignoreMouseEvents;
  final Completer<void> _initWindowStateCompleter = Completer<void>();

  @override
  void initState() {
    debugPrint("Window.initState()");
    super.initState();
    _initWindowState();
  }

  Future<void> _initWindowState() async {
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

    // bind listeners
    windowManager.addListener(this);
    widget.control.addInvokeMethodListener(_invokeMethod);

    if (!_initWindowStateCompleter.isCompleted) {
      _initWindowStateCompleter.complete();
    }
  }

  @override
  void didChangeDependencies() {
    debugPrint("Window.didChangeDependencies: ${widget.control.id}");
    super.didChangeDependencies();
    var backend = FletBackend.of(context);
    if (_initWindowStateCompleter.isCompleted) {
      _updateWindow(backend);
    } else {
      _initWindowStateCompleter.future.then((_) {
        _updateWindow(backend);
      });
    }
  }

  @override
  void dispose() {
    debugPrint("Window.dispose()");
    windowManager.removeListener(this);
    widget.control.addInvokeMethodListener(_invokeMethod);
    super.dispose();
  }

  @override
  void didUpdateWidget(covariant WindowControl oldWidget) {
    debugPrint("Window.didUpdateWidget: ${widget.control.id}");
    super.didUpdateWidget(oldWidget);
    _updateWindow(FletBackend.of(context));
  }

  void _updateWindow(FletBackend backend) async {
    try {
      var title = widget.control.parent!.get<String>("title");
      var bgColor = widget.control.getColor("bgcolor", context);
      var width = widget.control.get<double>("width");
      var height = widget.control.get<double>("height");
      var minWidth = widget.control.get<double>("min_width");
      var minHeight = widget.control.get<double>("min_height");
      var maxWidth = widget.control.get<double>("max_width");
      var maxHeight = widget.control.get<double>("max_height");
      var top = widget.control.get<double>("top");
      var left = widget.control.get<double>("left");
      var center = widget.control.get<String>("center");
      var fullScreen = widget.control.get<bool>("full_screen");
      var minimized = widget.control.get<bool>("minimized");
      var maximized = widget.control.get<bool>("maximized");
      var alignment = parseAlignment(widget.control, "alignment");
      var badgeLabel = widget.control.get<String>("badge_label");
      var icon = widget.control.get<String>("icon");
      var hasShadow = widget.control.get<bool>("shadow");
      var opacity = widget.control.get<double>("opacity");
      var minimizable = widget.control.get<bool>("minimizable");
      var maximizable = widget.control.get<bool>("maximizable");
      var alwaysOnTop = widget.control.get<bool>("always_on_top");
      var alwaysOnBottom = widget.control.get<bool>("always_on_bottom");
      var resizable = widget.control.get<bool>("resizable");
      var movable = widget.control.get<bool>("movable");
      var preventClose = widget.control.get<bool>("prevent_close");
      var titleBarHidden = widget.control.get<bool>("title_bar_hidden");
      var titleBarButtonsHidden =
          widget.control.get<bool>("title_bar_buttons_hidden", false)!;
      var visible = widget.control.get<bool>("visible");
      var focused = widget.control.get<bool>("focused");
      var skipTaskBar = widget.control.get<bool>("skip_task_bar");
      var frameless = widget.control.get<bool>("frameless");
      var progressBar = widget.control.get<double>("progress_bar");
      var ignoreMouseEvents = widget.control.get<bool>("ignore_mouse_events");

      // title
      if (title != null && title != _title) {
        setWindowTitle(title);
        _title = title;
      }

      // bgColor
      if (bgColor != null && bgColor != _bgColor) {
        setWindowBackgroundColor(bgColor);
        _bgColor = bgColor;
      }

      // size
      if ((width != null || height != null) &&
          (width != _width || height != _height) &&
          fullScreen != true &&
          (defaultTargetPlatform != TargetPlatform.macOS ||
              (defaultTargetPlatform == TargetPlatform.macOS &&
                  widget.control.get<bool>("maximized") != true &&
                  widget.control.get<bool>("minimized") != true))) {
        await setWindowSize(width, height);
        _width = width;
        _height = height;
      }

      // min size
      if ((minWidth != null || minHeight != null) &&
          (minWidth != _minWidth || minHeight != _minHeight)) {
        await setWindowMinSize(minWidth, minHeight);
        _minWidth = minWidth;
        _minHeight = minHeight;
      }

      // max size
      if ((maxWidth != null || maxHeight != null) &&
          (maxWidth != _maxWidth || maxHeight != _maxHeight)) {
        await setWindowMaxSize(maxWidth, maxHeight);
        _maxWidth = maxWidth;
        _maxHeight = maxHeight;
      }

      // position
      if ((top != null || left != null) &&
          (top != _top || left != _left) &&
          fullScreen != true &&
          (center == null || center == "") &&
          (defaultTargetPlatform != TargetPlatform.macOS ||
              (defaultTargetPlatform == TargetPlatform.macOS &&
                  widget.control.get<bool>("maximized") != true &&
                  widget.control.get<bool>("minimized") != true))) {
        await setWindowPosition(top, left);
        _top = top;
        _left = left;
      }

      // opacity
      if (opacity != null && opacity != _opacity) {
        await setWindowOpacity(opacity);
        _opacity = opacity;
      }

      // minimizable
      if (minimizable != null && minimizable != _minimizable) {
        await setWindowMinimizability(minimizable);
        _minimizable = minimizable;
      }

      // minimized
      if (minimized != _minimized) {
        if (minimized == true) {
          await minimizeWindow();
        } else if (minimized == false && maximized != true) {
          await restoreWindow();
        }
        _minimized = minimized;
      }

      // maximizable
      if (maximizable != null && maximizable != _maximizable) {
        await setWindowMaximizability(maximizable);
        _maximizable = maximizable;
      }

      // maximized
      if (maximized != _maximized) {
        if (maximized == true) {
          await maximizeWindow();
        } else if (maximized == false) {
          await unmaximizeWindow();
        }
        _maximized = maximized;
      }

      // alignment
      if (alignment != null && alignment != _alignment) {
        await setWindowAlignment(alignment);
        _alignment = alignment;
      }

      // badge label
      if (badgeLabel != null && badgeLabel != _badgeLabel) {
        await setWindowBadgeLabel(badgeLabel);
        _badgeLabel = badgeLabel;
      }

      // icon
      if (icon != null && icon != _icon) {
        var iconAssetSrc = backend.getAssetSource(icon);
        await setWindowIcon(iconAssetSrc.path);
        _icon = icon;
      }

      // has shadow
      if (hasShadow != null && hasShadow != _hasShadow) {
        await setWindowShadow(hasShadow);
        _hasShadow = hasShadow;
      }

      // resizable
      if (resizable != null && resizable != _resizable) {
        await setWindowResizability(resizable);
        _resizable = resizable;
      }

      // movable
      if (movable != null && movable != _movable) {
        await setWindowMovability(movable);
        _movable = movable;
      }

      // full screen
      if (fullScreen != null && fullScreen != _fullScreen) {
        await setWindowFullScreen(fullScreen);
        _fullScreen = fullScreen;
      }

      // always on top
      if (alwaysOnTop != null && alwaysOnTop != _alwaysOnTop) {
        await setWindowAlwaysOnTop(alwaysOnTop);
        _alwaysOnTop = alwaysOnTop;
      }

      // always on bottom
      if (alwaysOnBottom != null && alwaysOnBottom != _alwaysOnBottom) {
        await setWindowAlwaysOnBottom(alwaysOnBottom);
        _alwaysOnBottom = alwaysOnBottom;
      }

      // prevent close
      if (preventClose != null && preventClose != _preventClose) {
        await setWindowPreventClose(preventClose);
        _preventClose = preventClose;
      }

      // title bar hidden
      if (titleBarHidden != null && titleBarHidden != _titleBarHidden) {
        await setWindowTitleBarVisibility(
            titleBarHidden, titleBarButtonsHidden);
        _titleBarHidden = titleBarHidden;
      }

      // visible
      if (visible != _visible) {
        if (visible == true) {
          await showWindow();
        } else {
          await hideWindow();
        }
        _visible = visible;
      }

      // focused
      if (focused != _focused) {
        if (focused == true) {
          await focusWindow();
        } else {
          await blurWindow();
        }
        _focused = focused;
      }

      // frameless
      if (frameless != null && frameless != _frameless && frameless == true) {
        await setWindowFrameless();
        _frameless = frameless;
      }

      // progress bar
      if (progressBar != null && progressBar != _progressBar) {
        await setWindowProgressBar(progressBar);
        _progressBar = progressBar;
      }

      // skip task bar
      if (skipTaskBar != null && skipTaskBar != _skipTaskBar) {
        await setWindowSkipTaskBar(skipTaskBar);
        _skipTaskBar = skipTaskBar;
      }

      // ignore mouse events
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
        await centerWindow();
        break;
      case "close":
        await closeWindow();
        break;
      case "destroy":
        await destroyWindow();
        break;
      default:
        throw Exception("Unknown method ${widget.control.type}.$name");
    }
  }

  @override
  Widget build(BuildContext context) {
    return const SizedBox.shrink();
  }

  @override
  void onWindowEvent(String eventName) {
    if (["resize", "resized", "move"].contains(eventName)) return;

    var backend = FletBackend.of(context);
    getWindowState().then((wmd) {
      backend.onWindowEvent(eventName, wmd);
    });
  }
}
