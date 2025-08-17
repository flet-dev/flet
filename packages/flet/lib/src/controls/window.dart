import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:window_manager/window_manager.dart';

import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/colors.dart';
import '../utils/desktop.dart';
import '../utils/numbers.dart';
import '../utils/platform.dart';
import '../utils/theme.dart';
import '../utils/window.dart';

class WindowControl extends StatefulWidget {
  final Control control;

  WindowControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

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
    _updateWindowAfterInit();
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
    _updateWindowAfterInit();
  }

  void _updateWindowAfterInit() {
    var backend = FletBackend.of(context);
    if (_initWindowStateCompleter.isCompleted) {
      _updateWindow(backend);
    } else {
      _initWindowStateCompleter.future.then((_) {
        _updateWindow(backend);
      });
    }
  }

  void _updateWindow(FletBackend backend) async {
    try {
      var title = widget.control.parent!.getString("title");
      var bgColor = widget.control.getColor("bgcolor", context);
      var width = widget.control.getDouble("width");
      var height = widget.control.getDouble("height");
      var minWidth = widget.control.getDouble("min_width");
      var minHeight = widget.control.getDouble("min_height");
      var maxWidth = widget.control.getDouble("max_width");
      var maxHeight = widget.control.getDouble("max_height");
      var top = widget.control.getDouble("top");
      var left = widget.control.getDouble("left");
      var fullScreen = widget.control.getBool("full_screen");
      var minimized = widget.control.getBool("minimized");
      var maximized = widget.control.getBool("maximized");
      var alignment = widget.control.getAlignment("alignment");
      var badgeLabel = widget.control.getString("badge_label");
      var icon = widget.control.getString("icon");
      var hasShadow = widget.control.getBool("shadow");
      var opacity = widget.control.getDouble("opacity");
      var aspectRatio = widget.control.getDouble("aspect_ratio");
      var brightness = widget.control.getBrightness("brightness");
      var minimizable = widget.control.getBool("minimizable");
      var maximizable = widget.control.getBool("maximizable");
      var alwaysOnTop = widget.control.getBool("always_on_top");
      var alwaysOnBottom = widget.control.getBool("always_on_bottom");
      var resizable = widget.control.getBool("resizable");
      var movable = widget.control.getBool("movable");
      var preventClose = widget.control.getBool("prevent_close");
      var titleBarHidden = widget.control.getBool("title_bar_hidden");
      var titleBarButtonsHidden =
          widget.control.getBool("title_bar_buttons_hidden", false)!;
      var visible = widget.control.getBool("visible");
      var focused = widget.control.getBool("focused");
      var skipTaskBar = widget.control.getBool("skip_task_bar");
      var frameless = widget.control.getBool("frameless");
      var progressBar = widget.control.getDouble("progress_bar");
      var ignoreMouseEvents = widget.control.getBool("ignore_mouse_events");

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
          (!isMacOSDesktop() ||
              (isMacOSDesktop() && maximized != true && minimized != true))) {
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
          (!isMacOSDesktop() ||
              (isMacOSDesktop() && maximized != true && minimized != true))) {
        await setWindowPosition(top, left);
        _top = top;
        _left = left;
      }

      // opacity
      if (opacity != null && opacity != _opacity) {
        await setWindowOpacity(opacity);
        _opacity = opacity;
      }

      // aspectRatio
      if (aspectRatio != null && aspectRatio != _aspectRatio) {
        await setWindowAspectRatio(aspectRatio);
        _aspectRatio = aspectRatio;
      }

      // brightness
      if (brightness != null && brightness != _brightness) {
        await setWindowBrightness(brightness);
        _brightness = brightness;
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
    getWindowState().then((state) {
      widget.control.backend.onWindowEvent(eventName, state);
    });
  }
}
