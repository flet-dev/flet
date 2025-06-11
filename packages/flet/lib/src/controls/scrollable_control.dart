import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import '../utils/keys.dart';

class ScrollableControl extends StatefulWidget {
  final Control control;
  final Widget child;
  final Axis scrollDirection;
  final ScrollController? scrollController;

  ScrollableControl(
      {Key? key,
      required this.control,
      required this.child,
      required this.scrollDirection,
      this.scrollController})
      : super(key: ValueKey("control_${control.id}"));

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
    var offset = parseDouble(args["offset"]);
    var delta = parseDouble(args["delta"]);
    var scrollKey = parseKey(args["scroll_key"]);
    var globalKey = scrollKey != null
        ? widget.control.backend.globalKeys[scrollKey.toString()]
        : null;
    switch (name) {
      case "scroll_to":
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
      default:
        throw Exception("Unknown ScrollableControl method: $name");
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
    ScrollMode scrollMode =
        widget.control.getScrollMode("scroll", ScrollMode.none)!;

    if (widget.control.getBool("auto_scroll", false)!) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        _controller.animateTo(
          _controller.position.maxScrollExtent,
          duration: const Duration(seconds: 1),
          curve: Curves.ease,
        );
      });
    }
    return scrollMode != ScrollMode.none
        ? Scrollbar(
            // todo: create class ScrollBarConfiguration on Py end, for more customizability
            thumbVisibility: scrollMode == ScrollMode.always ||
                    (scrollMode == ScrollMode.adaptive && !isMobilePlatform())
                ? true
                : false,
            trackVisibility: scrollMode == ScrollMode.hidden ? false : null,
            thickness: scrollMode == ScrollMode.hidden
                ? 0
                : isMobilePlatform()
                    ? 4.0
                    : null,
            //interactive: true,
            controller: _controller,
            child: SingleChildScrollView(
              controller: _controller,
              scrollDirection: widget.scrollDirection,
              child: widget.child,
            ))
        : widget.child;
  }
}
