import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/animations.dart';
import '../utils/numbers.dart';
import '../utils/others.dart';
import '../utils/time.dart';
import '../widgets/flet_store_mixin.dart';

class ScrollableControl extends StatefulWidget {
  final Control control;
  final Widget child;
  final Axis scrollDirection;
  final ScrollController? scrollController;

  const ScrollableControl(
      {super.key,
      required this.control,
      required this.child,
      required this.scrollDirection,
      this.scrollController});

  @override
  State<ScrollableControl> createState() => _ScrollableControlState();
}

class _ScrollableControlState extends State<ScrollableControl>
    with FletStoreMixin {
  late final ScrollController _controller;
  late bool _ownController = false;
  String? _method;

  @override
  void initState() {
    super.initState();
    if (widget.scrollController != null) {
      _controller = widget.scrollController!;
    } else {
      _controller = ScrollController();
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
    debugPrint("ScrollableControl build: ${widget.control.id}");
    return withPagePlatform((context, platform) {
      ScrollMode scrollMode =
          parseScrollMode(widget.control.getString("scroll"), ScrollMode.none)!;

      var method = widget.control.getString("method");

      if (widget.control.getBool("auto_scroll", false)!) {
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
        FletBackend.of(context)
            .updateControl(widget.control.id, {"method": ""});

        var mj = json.decode(method);
        var name = mj["n"] as String;
        var params = Map<String, dynamic>.from(mj["p"] as Map);

        if (name == "scroll_to") {
          var duration = parseDuration(params["duration"], Duration.zero)!;
          var curve = parseCurve(params["curve"], Curves.ease)!;
          if (params["key"] != null) {
            WidgetsBinding.instance.addPostFrameCallback((_) {
              var key = FletBackend.of(context).globalKeys[params["key"]];
              if (key != null) {
                var ctx = key.currentContext;
                if (ctx != null) {
                  Scrollable.ensureVisible(ctx,
                      duration: duration, curve: curve);
                }
              }
            });
          } else if (params["offset"] != null) {
            WidgetsBinding.instance.addPostFrameCallback((_) {
              var offset = parseDouble(params["offset"], 0)!;
              if (offset < 0) {
                offset = _controller.position.maxScrollExtent + offset + 1;
              }
              if (duration.inMilliseconds < 1) {
                _controller.jumpTo(offset);
              } else {
                _controller.animateTo(offset, duration: duration, curve: curve);
              }
            });
          } else if (params["delta"] != null) {
            WidgetsBinding.instance.addPostFrameCallback((_) {
              var delta = parseDouble(params["delta"], 0)!;
              var offset = _controller.position.pixels + delta;
              if (duration.inMilliseconds < 1) {
                _controller.jumpTo(offset);
              } else {
                _controller.animateTo(offset, duration: duration, curve: curve);
              }
            });
          }
        }
      }

      return scrollMode != ScrollMode.none
          ? Scrollbar(
              thumbVisibility: scrollMode == ScrollMode.always ||
                      (scrollMode == ScrollMode.adaptive &&
                          !kIsWeb &&
                          platform != TargetPlatform.iOS &&
                          platform != TargetPlatform.android)
                  ? true
                  : false,
              trackVisibility: scrollMode == ScrollMode.hidden ? false : null,
              thickness: scrollMode == ScrollMode.hidden
                  ? 0
                  : platform == TargetPlatform.iOS ||
                          platform == TargetPlatform.android
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
    });
  }
}
