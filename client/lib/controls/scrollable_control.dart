import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

enum ScrollMode { none, auto, adaptive, always, hidden }

class ScrollableControl extends StatefulWidget {
  final Widget child;
  final Axis scrollDirection;
  final ScrollMode scrollMode;
  final bool autoScroll;

  const ScrollableControl(
      {Key? key,
      required this.child,
      required this.scrollDirection,
      required this.scrollMode,
      required this.autoScroll})
      : super(key: key);

  @override
  State<ScrollableControl> createState() => _ScrollableControlState();
}

class _ScrollableControlState extends State<ScrollableControl> {
  final ScrollController _controller = ScrollController();

  void _scrollDown() {
    _controller.animateTo(
      _controller.position.maxScrollExtent,
      duration: const Duration(seconds: 1),
      curve: Curves.fastOutSlowIn,
    );
  }

  @override
  Widget build(BuildContext context) {
    bool? thumbVisibility = widget.scrollMode == ScrollMode.always ||
            (widget.scrollMode == ScrollMode.adaptive &&
                !kIsWeb &&
                !Platform.isIOS &&
                !Platform.isAndroid)
        ? true
        : null;

    if (widget.autoScroll) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        _scrollDown();
      });
    }

    return Scrollbar(
        thumbVisibility: thumbVisibility,
        trackVisibility: widget.scrollMode == ScrollMode.hidden ? false : null,
        thickness: widget.scrollMode == ScrollMode.hidden ? 0 : null,
        controller: _controller,
        child: SingleChildScrollView(
          controller: _controller,
          child: widget.child,
          scrollDirection: widget.scrollDirection,
        ));
  }
}
