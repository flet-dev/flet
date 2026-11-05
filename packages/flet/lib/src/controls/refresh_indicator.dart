import 'dart:async';

import 'package:material_ui/material_ui.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class RefreshIndicatorControl extends StatefulWidget {
  final Control control;

  RefreshIndicatorControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<RefreshIndicatorControl> createState() =>
      _RefreshIndicatorControlState();
}

class _RefreshIndicatorControlState extends State<RefreshIndicatorControl> {
  final GlobalKey<RefreshIndicatorState> _refreshIndicatorKey =
      GlobalKey<RefreshIndicatorState>();

  /// Completes when Python's `on_refresh` handler returns, which hides the
  /// progress indicator.
  Completer<void>? _refreshCompleter;

  @override
  void initState() {
    super.initState();
    widget.control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void dispose() {
    _finishRefresh();
    widget.control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }

  void _finishRefresh() {
    _refreshCompleter?.complete();
    _refreshCompleter = null;
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("RefreshIndicator.$name($args)");
    switch (name) {
      case "show":
        // `show` doesn't wait for the refresh it starts: that ends only once the
        // `on_refresh` handler returns, which can outlast the method call's timeout.
        unawaited(_refreshIndicatorKey.currentState
            ?.show(atTop: args["at_top"] ?? true));
      case "finish_refresh":
        _finishRefresh();
      default:
        throw Exception("Unknown RefreshIndicator method: $name");
    }
  }

  /// Waits for Python's `on_refresh` handler, which is only told about the
  /// refresh when it is set; without one there is nothing to wait for.
  Future<void> _onRefresh() {
    if (!widget.control.hasEventHandler("refresh")) {
      return Future.value();
    }
    _finishRefresh();
    final completer = Completer<void>();
    _refreshCompleter = completer;
    widget.control.triggerEvent("refresh");
    return completer.future;
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("RefreshIndicator build: ${widget.control.id}");

    final content = widget.control.buildWidget("content");
    if (content == null) {
      return const ErrorControl("RefreshIndicator.content must be visible");
    }

    final refreshIndicator = RefreshIndicator(
      key: _refreshIndicatorKey,
      displacement: widget.control.getDouble("displacement", 40.0)!,
      edgeOffset: widget.control.getDouble("edge_offset", 0.0)!,
      color: widget.control.getColor("color", context),
      backgroundColor: widget.control.getColor("bgcolor", context),
      strokeWidth: widget.control.getDouble("stroke_width", 2.0)!,
      elevation: widget.control.getDouble("elevation", 2.0)!,
      triggerMode: widget.control.getRefreshIndicatorTriggerMode(
          "trigger_mode", RefreshIndicatorTriggerMode.onEdge)!,
      notificationPredicate:
          widget.control.getBool("handle_nested_scrolls", false)!
              ? (notification) => true
              : defaultScrollNotificationPredicate,
      semanticsLabel: widget.control.getString("semantics_label"),
      semanticsValue: widget.control.getString("semantics_value"),
      onRefresh: _onRefresh,
      child: _alwaysScrollable(context, content),
    );

    return LayoutControl(control: widget.control, child: refreshIndicator);
  }

  /// Lets [content] be pulled even when it is too short to scroll.
  ///
  /// A pull is a scroll past the top, and Flet's scrollable controls only
  /// scroll when their content overflows, so a short or empty list couldn't be
  /// refreshed. This keeps the platform's own physics, such as bouncing on
  /// iOS, for scrollables that don't set theirs.
  Widget _alwaysScrollable(BuildContext context, Widget content) {
    final behavior = ScrollConfiguration.of(context);
    return ScrollConfiguration(
      behavior: behavior.copyWith(
        physics: AlwaysScrollableScrollPhysics(
            parent: behavior.getScrollPhysics(context)),
      ),
      child: content,
    );
  }
}
