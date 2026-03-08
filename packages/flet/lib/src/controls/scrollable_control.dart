import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/animations.dart';
import '../utils/keys.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
import '../utils/platform.dart';
import '../utils/time.dart';
import '../widgets/flet_store_mixin.dart';

class _ScrollbarConfiguration {
  final ScrollMode mode;
  final bool? thumbVisibility;
  final bool? trackVisibility;
  final double? thickness;
  final Radius? radius;
  final bool? interactive;
  final ScrollbarOrientation? orientation;

  const _ScrollbarConfiguration({
    required this.mode,
    this.thumbVisibility,
    this.trackVisibility,
    this.thickness,
    this.radius,
    this.interactive,
    this.orientation,
  });

  factory _ScrollbarConfiguration.fromValue(dynamic value) {
    if (value is Map) {
      final modeValue = value["mode"] ?? value["scroll_mode"];
      final parsedRadius = parseDouble(value["radius"]);
      return _ScrollbarConfiguration(
        mode: parseScrollMode(
                modeValue is String ? modeValue : null, ScrollMode.auto) ??
            ScrollMode.auto,
        thumbVisibility: parseBool(value["thumb_visibility"]),
        trackVisibility: parseBool(value["track_visibility"]),
        thickness: parseDouble(value["thickness"]),
        radius: parsedRadius != null ? Radius.circular(parsedRadius) : null,
        interactive: parseBool(value["interactive"]),
        orientation: _parseScrollbarOrientation(value["orientation"]),
      );
    }

    return _ScrollbarConfiguration(
      mode: parseScrollMode(value is String ? value : null, ScrollMode.none) ??
          ScrollMode.none,
    );
  }

  bool get enabled => mode != ScrollMode.none;

  bool get effectiveThumbVisibility {
    final defaultValue = (mode == ScrollMode.always ||
            (mode == ScrollMode.adaptive && !isMobilePlatform())) &&
        mode != ScrollMode.hidden;
    return thumbVisibility ?? defaultValue;
  }

  double? get effectiveThickness {
    if (thickness != null) {
      return thickness;
    }
    return mode == ScrollMode.hidden
        ? 0
        : isMobilePlatform()
            ? 4.0
            : null;
  }
}

ScrollbarOrientation? _parseScrollbarOrientation(dynamic value,
    [ScrollbarOrientation? defaultValue]) {
  if (value is! String) {
    return defaultValue;
  }
  switch (value.toLowerCase()) {
    case "left":
      return ScrollbarOrientation.left;
    case "right":
      return ScrollbarOrientation.right;
    case "top":
      return ScrollbarOrientation.top;
    case "bottom":
      return ScrollbarOrientation.bottom;
    default:
      return defaultValue;
  }
}

class ScrollableControl extends StatefulWidget {
  final Control control;
  final Widget child;
  final Axis scrollDirection;
  final ScrollController? scrollController;
  final bool wrapIntoScrollableView;

  ScrollableControl(
      {Key? key,
      required this.control,
      required this.child,
      required this.scrollDirection,
      this.scrollController,
      this.wrapIntoScrollableView = false})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<ScrollableControl> createState() => _ScrollableControlState();
}

class _ScrollableControlState extends State<ScrollableControl>
    with FletStoreMixin {
  late final ScrollController _controller;
  late bool _ownController = false;

  @override
  void initState() {
    super.initState();
    widget.control.addInvokeMethodListener(_invokeMethod);
    if (widget.scrollController != null) {
      _controller = widget.scrollController!;
    } else {
      _controller = ScrollController();
      _ownController = true;
    }
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("ScrollableControl.$name($args)");
    switch (name) {
      case "scroll_to":
        var offset = parseDouble(args["offset"]);
        var delta = parseDouble(args["delta"]);
        var scrollKey = parseKey(args["scroll_key"]);
        var globalKey = scrollKey != null
            ? widget.control.backend.globalKeys[scrollKey.toString()]
            : null;
        var duration = parseDuration(args["duration"], Duration.zero)!;
        var curve = parseCurve(args["curve"], Curves.ease)!;
        if (globalKey != null) {
          var ctx = globalKey.currentContext;
          if (ctx != null) {
            Scrollable.ensureVisible(ctx, duration: duration, curve: curve);
          }
        } else if (offset != null) {
          if (offset < 0) {
            offset = _controller.position.maxScrollExtent + offset + 1;
          }
          if (duration.inMilliseconds < 1) {
            _controller.jumpTo(offset);
          } else {
            _controller.animateTo(offset, duration: duration, curve: curve);
          }
        } else if (delta != null) {
          var offset = _controller.position.pixels + delta;
          if (duration.inMilliseconds < 1) {
            _controller.jumpTo(offset);
          } else {
            _controller.animateTo(offset, duration: duration, curve: curve);
          }
        }
    }
  }

  @override
  void dispose() {
    if (_ownController) {
      _controller.dispose();
    }
    widget.control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("ScrollableControl build: ${widget.control.id}");
    final scrollConfiguration =
        _ScrollbarConfiguration.fromValue(widget.control.get("scroll"));

    if (widget.control.getBool("auto_scroll", false)!) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        _controller.animateTo(
          _controller.position.maxScrollExtent,
          duration: const Duration(seconds: 1),
          curve: Curves.ease,
        );
      });
    }
    return scrollConfiguration.enabled
        ? Scrollbar(
            thumbVisibility: scrollConfiguration.effectiveThumbVisibility,
            trackVisibility: scrollConfiguration.trackVisibility,
            thickness: scrollConfiguration.effectiveThickness,
            radius: scrollConfiguration.radius,
            interactive: scrollConfiguration.interactive,
            scrollbarOrientation: scrollConfiguration.orientation,
            controller: _controller,
            child: ScrollConfiguration(
              behavior:
                  ScrollConfiguration.of(context).copyWith(scrollbars: false),
              child: widget.wrapIntoScrollableView
                  ? SingleChildScrollView(
                      controller: _controller,
                      scrollDirection: widget.scrollDirection,
                      child: widget.child,
                    )
                  : widget.child,
            ))
        : widget.child;
  }
}
