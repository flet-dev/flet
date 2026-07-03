import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';

import '../models/control.dart';
import '../utils/animations.dart';
import '../utils/keys.dart';
import '../utils/numbers.dart';
import '../utils/scrollbar.dart';
import '../utils/time.dart';
import '../widgets/flet_store_mixin.dart';

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
  final _ConstraintsHolder _outerConstraints = _ConstraintsHolder();

  // Auto-scroll: keep the view pinned to the bottom (end) while the user
  // hasn't scrolled away from it. Unlike a one-shot scroll on build, this
  // follows content that grows *in place* — e.g. streamed text appended to an
  // existing child — which does not rebuild this widget and so is otherwise
  // missed.
  static const double _autoScrollThreshold = 40.0;
  bool _pinnedToEnd = true;
  double _lastMaxScrollExtent = 0;
  bool _autoScrollScheduled = false;
  // When set (via the `auto_scroll_animation` property) auto-scroll animates
  // to the end with this duration/curve; otherwise it jumps instantly.
  ImplicitAnimationDetails? _autoScrollAnimation;

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
    _controller.addListener(_onScroll);
  }

  void _onScroll() {
    if (!_controller.hasClients) return;
    final pos = _controller.position;
    // "At the end" if within a small threshold of the max extent — so a
    // partially-visible last line still counts as pinned.
    _pinnedToEnd = pos.pixels >= pos.maxScrollExtent - _autoScrollThreshold;
  }

  void _scheduleScrollToEnd({bool force = false}) {
    if (_autoScrollScheduled) return;
    _autoScrollScheduled = true;
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _autoScrollScheduled = false;
      if (!mounted || !_controller.hasClients) return;
      final max = _controller.position.maxScrollExtent;
      _lastMaxScrollExtent = max;
      if (force || _pinnedToEnd) {
        final anim = _autoScrollAnimation;
        if (anim != null && anim.duration > Duration.zero) {
          _controller.animateTo(max,
              duration: anim.duration, curve: anim.curve);
        } else {
          _controller.jumpTo(max);
        }
        _pinnedToEnd = true;
      }
    });
  }

  // Wraps the scrollable so auto_scroll follows extent growth (streamed text,
  // inserted items) even when this widget itself does not rebuild.
  Widget _wrapAutoScroll(Widget child) {
    return NotificationListener<ScrollMetricsNotification>(
      onNotification: (notification) {
        final max = notification.metrics.maxScrollExtent;
        if (max > _lastMaxScrollExtent + 0.5 && _pinnedToEnd) {
          _scheduleScrollToEnd();
        }
        _lastMaxScrollExtent = max;
        return false;
      },
      child: child,
    );
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
    _controller.removeListener(_onScroll);
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
        widget.control.getScrollbarConfiguration("scroll");

    final autoScroll = widget.control.getBool("auto_scroll", false)!;
    if (autoScroll) {
      // Default to a 1s ease animation (the historical auto_scroll behavior);
      // set `auto_scroll_animation` to override, or to duration 0 for an
      // instant jump.
      _autoScrollAnimation = widget.control.getAnimation(
        "auto_scroll_animation",
        ImplicitAnimationDetails(
            duration: const Duration(seconds: 1), curve: Curves.ease),
      );
      // Re-pin on rebuild (e.g. an item added). Extent growth without a
      // rebuild is handled by the ScrollMetricsNotification listener in
      // _wrapAutoScroll.
      _scheduleScrollToEnd();
    }

    if (scrollConfiguration == null) {
      return autoScroll ? _wrapAutoScroll(widget.child) : widget.child;
    }

    Widget child = widget.child;
    if (widget.wrapIntoScrollableView) {
      // The pre-#6450 path used a plain SingleChildScrollView. PR #6450 added
      // a LayoutBuilder + ConstrainedBox(minHeight: parentMaxHeight) wrapper
      // so vertical alignment works in scrollable Page/View when content is
      // shorter than the viewport. LayoutBuilder, however, reports 0 for
      // intrinsic dimensions, which collapses any ancestor IntrinsicWidth /
      // IntrinsicHeight and leaves the layout perpetually dirty.
      //
      // Replicate the behavior with two cooperating RenderProxyBoxes that
      // forward intrinsic queries to their child. The outer reader captures
      // the parent's constraints during performLayout; the inner enforcer
      // reads them back and applies them as a min on the scroll-view child.
      child = SingleChildScrollView(
        controller: _controller,
        scrollDirection: widget.scrollDirection,
        child: _InnerConstraintsEnforcer(
          holder: _outerConstraints,
          scrollDirection: widget.scrollDirection,
          child: widget.child,
        ),
      );
    }

    Widget result = Scrollbar(
        thumbVisibility: scrollConfiguration.thumbVisibility,
        trackVisibility: scrollConfiguration.trackVisibility,
        thickness: scrollConfiguration.thickness,
        radius: scrollConfiguration.radius,
        interactive: scrollConfiguration.interactive,
        scrollbarOrientation: scrollConfiguration.orientation,
        controller: _controller,
        child: ScrollConfiguration(
          behavior: ScrollConfiguration.of(context).copyWith(scrollbars: false),
          child: child,
        ));

    if (widget.wrapIntoScrollableView) {
      result = _OuterConstraintsReader(
        holder: _outerConstraints,
        child: result,
      );
    }

    return autoScroll ? _wrapAutoScroll(result) : result;
  }
}

/// Carries box constraints from [_OuterConstraintsReader] (outside the scroll
/// view) to [_InnerConstraintsEnforcer] (inside it) within a single layout
/// pass. Holds a reference to the inner enforcer so the outer reader can
/// mark it dirty when its incoming constraints change — without that, the
/// inner enforcer would skip re-layout on window resize because the
/// constraints it sees from SingleChildScrollView (unbounded in scroll axis)
/// don't change.
class _ConstraintsHolder {
  BoxConstraints? value;
  RenderObject? listener;
}

class _OuterConstraintsReader extends SingleChildRenderObjectWidget {
  const _OuterConstraintsReader({required this.holder, super.child});
  final _ConstraintsHolder holder;

  @override
  RenderObject createRenderObject(BuildContext context) =>
      _RenderOuterConstraintsReader(holder);

  @override
  void updateRenderObject(
      BuildContext context, _RenderOuterConstraintsReader renderObject) {
    renderObject.holder = holder;
  }
}

class _RenderOuterConstraintsReader extends RenderProxyBox {
  _RenderOuterConstraintsReader(this.holder);
  _ConstraintsHolder holder;

  @override
  void performLayout() {
    final changed = holder.value != constraints;
    holder.value = constraints;
    if (changed && holder.listener != null) {
      // Force the inner enforcer to re-run performLayout in this layout pass.
      // invokeLayoutCallback enables mutations during layout — without it,
      // markNeedsLayout asserts.
      invokeLayoutCallback<BoxConstraints>((_) {
        holder.listener?.markNeedsLayout();
      });
    }
    super.performLayout();
  }
}

class _InnerConstraintsEnforcer extends SingleChildRenderObjectWidget {
  const _InnerConstraintsEnforcer({
    required this.holder,
    required this.scrollDirection,
    super.child,
  });
  final _ConstraintsHolder holder;
  final Axis scrollDirection;

  @override
  RenderObject createRenderObject(BuildContext context) =>
      _RenderInnerConstraintsEnforcer(holder, scrollDirection);

  @override
  void updateRenderObject(
      BuildContext context, _RenderInnerConstraintsEnforcer renderObject) {
    renderObject
      ..holder = holder
      ..scrollDirection = scrollDirection;
  }
}

class _RenderInnerConstraintsEnforcer extends RenderProxyBox {
  _RenderInnerConstraintsEnforcer(this.holder, this.scrollDirection);
  _ConstraintsHolder holder;
  Axis scrollDirection;

  @override
  void attach(PipelineOwner owner) {
    super.attach(owner);
    holder.listener = this;
  }

  @override
  void detach() {
    if (holder.listener == this) holder.listener = null;
    super.detach();
  }

  @override
  void performLayout() {
    if (child == null) {
      size = computeSizeForNoChild(constraints);
      return;
    }
    BoxConstraints childConstraints = constraints;
    final outer = holder.value;
    if (outer != null) {
      if (scrollDirection == Axis.vertical && outer.hasBoundedHeight) {
        childConstraints =
            childConstraints.copyWith(minHeight: outer.maxHeight);
      } else if (scrollDirection == Axis.horizontal && outer.hasBoundedWidth) {
        childConstraints =
            childConstraints.copyWith(minWidth: outer.maxWidth);
      }
    }
    child!.layout(childConstraints, parentUsesSize: true);
    size = child!.size;
  }
}
