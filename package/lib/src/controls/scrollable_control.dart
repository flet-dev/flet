import 'dart:convert';

import 'package:flet/src/flet_control_backend.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../flet_app_services.dart';
import '../models/control.dart';
import '../utils/animations.dart';
import '../utils/desktop.dart';
import '../utils/numbers.dart';
import '../widgets/adjustable_scroll_controller.dart';

enum ScrollMode { none, auto, adaptive, always, hidden }

class ScrollableControl extends StatefulWidget {
  final Control control;
  final Widget child;
  final Axis scrollDirection;
  final ScrollController? scrollController;
  final FletControlBackend backend;

  const ScrollableControl(
      {super.key,
      required this.control,
      required this.child,
      required this.scrollDirection,
      this.scrollController,
      required this.backend});

  @override
  State<ScrollableControl> createState() => _ScrollableControlState();
}

class _ScrollableControlState extends State<ScrollableControl> {
  late final ScrollController _controller;
  late bool _ownController = false;
  String? _method;

  @override
  void initState() {
    super.initState();
    if (widget.scrollController != null) {
      _controller = widget.scrollController!;
    } else {
      _controller = (isWindowsDesktop()
          ? AdjustableScrollController()
          : ScrollController());
      _ownController = true;
    }
  }

  @override
  void dispose() {
    if (_ownController) {
      _controller.dispose();
    }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    ScrollMode scrollMode = ScrollMode.values.firstWhere(
        (m) =>
            m.name.toLowerCase() ==
            widget.control.attrString("scroll", "")!.toLowerCase(),
        orElse: () => ScrollMode.none);

    bool? thumbVisibility = scrollMode == ScrollMode.always ||
            (scrollMode == ScrollMode.adaptive &&
                !kIsWeb &&
                defaultTargetPlatform != TargetPlatform.iOS &&
                defaultTargetPlatform != TargetPlatform.android)
        ? true
        : null;

    var method = widget.control.attrString("method");

    if (widget.control.attrBool("autoScroll", false)!) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        _controller.animateTo(
          _controller.position.maxScrollExtent,
          duration: const Duration(seconds: 1),
          curve: Curves.ease,
        );
      });
    } else if (method != null && method != _method) {
      _method = method;
      debugPrint("ScrollableControl JSON method: $method");
      widget.backend.updateControlState(widget.control.id, {"method": ""});

      var mj = json.decode(method);
      var name = mj["n"] as String;
      var params = Map<String, dynamic>.from(mj["p"] as Map);

      if (name == "scroll_to") {
        var duration = parseInt(params["duration"]);
        var curve = params["curve"] != null
            ? parseCurve(params["curve"] as String)
            : Curves.ease;
        if (params["key"] != null) {
          WidgetsBinding.instance.addPostFrameCallback((_) {
            var key = FletAppServices.of(context).globalKeys[params["key"]];
            if (key != null) {
              var ctx = key.currentContext;
              if (ctx != null) {
                Scrollable.ensureVisible(ctx,
                    duration: duration > 0
                        ? Duration(milliseconds: duration)
                        : Duration.zero,
                    curve: curve);
              }
            }
          });
        } else if (params["offset"] != null) {
          WidgetsBinding.instance.addPostFrameCallback((_) {
            var offset = parseDouble(params["offset"]);
            if (offset < 0) {
              offset = _controller.position.maxScrollExtent + offset + 1;
            }
            if (duration < 1) {
              _controller.jumpTo(offset);
            } else {
              _controller.animateTo(
                offset,
                duration: Duration(milliseconds: duration),
                curve: curve,
              );
            }
          });
        } else if (params["delta"] != null) {
          WidgetsBinding.instance.addPostFrameCallback((_) {
            var delta = parseDouble(params["delta"]);
            var offset = _controller.position.pixels + delta;
            if (duration < 1) {
              _controller.jumpTo(offset);
            } else {
              _controller.animateTo(
                offset,
                duration: Duration(milliseconds: duration),
                curve: curve,
              );
            }
          });
        }
      }
    }

    return scrollMode != ScrollMode.none
        ? Scrollbar(
            thumbVisibility: thumbVisibility,
            trackVisibility: scrollMode == ScrollMode.hidden ? false : null,
            thickness: scrollMode == ScrollMode.hidden ? 0 : null,
            controller: _controller,
            child: SingleChildScrollView(
              controller: _controller,
              scrollDirection: widget.scrollDirection,
              child: widget.child,
            ))
        : widget.child;
  }
}
