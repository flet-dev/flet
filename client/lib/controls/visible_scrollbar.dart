import 'package:flutter/material.dart';

class VisibleScrollbar extends StatefulWidget {
  final Widget child;

  const VisibleScrollbar({Key? key, required this.child}) : super(key: key);

  @override
  State<VisibleScrollbar> createState() => _VisibleScrollbarState();
}

class _VisibleScrollbarState extends State<VisibleScrollbar> {
  final ScrollController _controller = ScrollController();

  @override
  Widget build(BuildContext context) {
    return Scrollbar(
        isAlwaysShown: true, controller: _controller, child: widget.child);
  }
}
