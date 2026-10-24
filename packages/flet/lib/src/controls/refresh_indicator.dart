import 'dart:async';

import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/numbers.dart';
import '../widgets/error.dart';
import 'base_controls.dart';
import 'control_widget.dart';

class RefreshIndicatorControl extends StatefulWidget {
  final Control control;

  RefreshIndicatorControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<RefreshIndicatorControl> createState() =>
      _RefreshIndicatorControlState();
}

class _RefreshIndicatorControlState extends State<RefreshIndicatorControl> {
  final GlobalKey<RefreshIndicatorState> _refreshKey =
      GlobalKey<RefreshIndicatorState>();

  Completer<void>? _refreshCompleter;

  @override
  void initState() {
    super.initState();
    widget.control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void dispose() {
    if (_refreshCompleter != null && !_refreshCompleter!.isCompleted) {
      _refreshCompleter!.complete();
    }
    _refreshCompleter = null;
    widget.control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("RefreshIndicator.$name($args)");
    switch (name) {
      case "finish_refresh":
        if (_refreshCompleter != null && !_refreshCompleter!.isCompleted) {
          _refreshCompleter!.complete();
        }
        _refreshCompleter = null;
        return null;
      default:
        throw Exception("Unknown RefreshIndicator method: $name");
    }
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("RefreshIndicatorControl build: ${widget.control.id}");

    final content = widget.control.buildWidget("content");
    if (content == null) {
      return const ErrorControl(
        "RefreshIndicator requires a 'content' child.",
      );
    }

    final displacement = widget.control.getDouble("displacement", 40.0)!;
    final edgeOffset = widget.control.getDouble("edge_offset", 0.0)!;
    final color = widget.control.getColor("color", context);
    final backgroundColor = widget.control.getColor("background_color", context);
    final handleNestedScrolls = widget.control.getBool("handle_nested_scrolls", false)!;
    final ScrollNotificationPredicate notificationPredicate =
        handleNestedScrolls
            ? (notification) => true
            : defaultScrollNotificationPredicate;

    final semanticsLabel = widget.control.getString("semantics_label");
    final semanticsValue = widget.control.getString("semantics_value");
    final strokeWidth = widget.control.getDouble("stroke_width", 2.0)!;
    final elevation = widget.control.getDouble("elevation", 2.0)!;
    final triggerMode = widget.control.getRefreshIndicatorTriggerMode("trigger_mode", RefreshIndicatorTriggerMode.onEdge)!;

    final hasOnStatusChange =
        widget.control.hasEventHandler("status_change");

    final Widget refreshIndicator = RefreshIndicator(
      key: _refreshKey,
      displacement: displacement,
      edgeOffset: edgeOffset,
      onStatusChange: hasOnStatusChange
          ? (RefreshIndicatorStatus status) {
              widget.control.triggerEvent("status_change", status.name);
            }
          : null,

      onRefresh: () async {
        widget.control.triggerEvent("refresh", null);
        _refreshCompleter = Completer<void>();
        try {
          await _refreshCompleter!.future;
        } finally {
          _refreshCompleter = null;
        }
      },
      color: color,
      backgroundColor: backgroundColor,
      notificationPredicate: notificationPredicate,
      semanticsLabel: semanticsLabel,
      semanticsValue: semanticsValue,
      strokeWidth: strokeWidth,
      triggerMode: triggerMode,
      elevation: elevation,
      child: content,
    );

    return LayoutControl(control: widget.control, child: refreshIndicator);
  }
}