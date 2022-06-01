import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

enum ScrollMode { none, auto, adaptive, always }

class ScrollableControl extends StatefulWidget {
  final Widget child;
  final Axis scrollDirection;
  final ScrollMode scrollMode;

  const ScrollableControl(
      {Key? key,
      required this.child,
      required this.scrollDirection,
      required this.scrollMode})
      : super(key: key);

  @override
  State<ScrollableControl> createState() => _ScrollableControlState();
}

class _ScrollableControlState extends State<ScrollableControl> {
  final ScrollController _controller = ScrollController();

  @override
  Widget build(BuildContext context) {
    bool isAlwaysShown = widget.scrollMode == ScrollMode.always ||
        (widget.scrollMode == ScrollMode.adaptive &&
            !kIsWeb &&
            !Platform.isIOS &&
            !Platform.isAndroid);

    return Scrollbar(
        isAlwaysShown: isAlwaysShown,
        controller: _controller,
        child: SingleChildScrollView(
          controller: _controller,
          child: widget.child,
          scrollDirection: widget.scrollDirection,
        ));
  }
}
