import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/animations.dart';
import '../utils/layout.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
import '../utils/time.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class PageViewControl extends StatefulWidget {
  final Control control;

  PageViewControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<PageViewControl> createState() => _PageViewControlState();
}

class _PageViewControlState extends State<PageViewControl> {
  late PageController _pageController;
  late bool _keepPage;
  late double _viewportFraction;
  late int _initialPageValue;
  int? _currentPageProp;

  @override
  void initState() {
    super.initState();
    widget.control.addInvokeMethodListener(_invokeMethod);
    _readControllerConfig();
    _pageController =
        _createController(initialPage: _currentPageProp ?? _initialPageValue);
  }

  @override
  void didUpdateWidget(PageViewControl oldWidget) {
    super.didUpdateWidget(oldWidget);

    final newKeepPage = widget.control.getBool("keep_page", true)!;
    final newViewportFraction =
        widget.control.getDouble("viewport_fraction", 1.0)!;
    final newInitialPage = widget.control.getInt("initial_page", 0)!;
    final newCurrentPage = widget.control.getInt("current_page");

    final requiresRebuild = newKeepPage != _keepPage ||
        newViewportFraction != _viewportFraction ||
        (newCurrentPage == null &&
            _currentPageProp == null &&
            newInitialPage != _initialPageValue);

    if (requiresRebuild) {
      _keepPage = newKeepPage;
      _viewportFraction = newViewportFraction;
      _initialPageValue = newInitialPage;
      final targetPage = newCurrentPage ?? _resolveCurrentPage();
      _currentPageProp = newCurrentPage ?? targetPage;

      final oldController = _pageController;
      _pageController = _createController(initialPage: targetPage);
      oldController.dispose();
    } else if (newCurrentPage != null &&
        newCurrentPage != _currentPageProp &&
        _pageController.hasClients) {
      _currentPageProp = newCurrentPage;
      _pageController.jumpToPage(newCurrentPage);
    }
  }

  void _readControllerConfig() {
    _keepPage = widget.control.getBool("keep_page", true)!;
    _viewportFraction = widget.control.getDouble("viewport_fraction", 1.0)!;
    _initialPageValue = widget.control.getInt("initial_page", 0)!;
    _currentPageProp = widget.control.getInt("current_page");
  }

  PageController _createController({required int initialPage}) {
    return PageController(
      initialPage: initialPage,
      keepPage: _keepPage,
      viewportFraction: _viewportFraction,
    );
  }

  int _resolveCurrentPage() {
    if (_currentPageProp != null) {
      return _currentPageProp!;
    }
    if (_pageController.hasClients) {
      final page = _pageController.page;
      if (page != null) {
        return page.round();
      }
    }
    return _initialPageValue;
  }

  void _handlePageChanged(int index) {
    _currentPageProp = index;
    widget.control.updateProperties({"current_page": index});
    widget.control.triggerEvent("change", index);
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    final defaultAnimationDuration =
        widget.control.getDuration("animation_duration");
    final defaultAnimationCurve = widget.control.getCurve("animation_curve");

    switch (name) {
      case "go_to_page":
        final index = parseInt(args["index"]);
        final duration =
            parseDuration(args["duration"], defaultAnimationDuration);
        final curve = parseCurve(args["curve"], defaultAnimationCurve);

        if (index != null && duration != null && curve != null) {
          return _pageController.animateToPage(index,
              duration: duration, curve: curve);
        }
      case "jump_to_page":
        final index = parseInt(args["index"]);

        if (index != null) {
          return _pageController.jumpToPage(index);
        }
      case "jump_to":
        final value = parseDouble(args["value"]);

        if (value != null) {
          return _pageController.jumpTo(value);
        }
      case "next_page":
        final duration =
            parseDuration(args["duration"], defaultAnimationDuration);
        final curve = parseCurve(args["curve"], defaultAnimationCurve);

        if (duration != null && curve != null) {
          return _pageController.nextPage(duration: duration, curve: curve);
        }
      case "previous_page":
        final duration =
            parseDuration(args["duration"], defaultAnimationDuration);
        final curve = parseCurve(args["curve"], defaultAnimationCurve);

        if (duration != null && curve != null) {
          return _pageController.previousPage(duration: duration, curve: curve);
        }
      default:
        throw Exception("Unknown PageView method: $name");
    }
  }

  @override
  void dispose() {
    widget.control.removeInvokeMethodListener(_invokeMethod);
    _pageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("PageViewControl build: ${widget.control.id}");

    final horizontal = widget.control.getBool("horizontal", true)!;
    final pageView = PageView(
      controller: _pageController,
      scrollDirection: horizontal ? Axis.horizontal : Axis.vertical,
      reverse: widget.control.getBool("reverse", false)!,
      clipBehavior:
          widget.control.getClipBehavior("clip_behavior", Clip.hardEdge)!,
      padEnds: widget.control.getBool("pad_ends", true)!,
      allowImplicitScrolling:
          widget.control.getBool("implicit_scrolling", false)!,
      pageSnapping: widget.control.getBool("page_snapping", true)!,
      onPageChanged: _handlePageChanged,
      children: widget.control.buildWidgets("controls"),
    );

    Widget layoutChild =
        LayoutControl(control: widget.control, child: pageView);

    if (widget.control.getExpand("expand", 0)! > 0) {
      return layoutChild;
    }

    return LayoutBuilder(
      builder: (context, constraints) {
        final unbounded = horizontal
            ? (constraints.maxHeight == double.infinity &&
                widget.control.getDouble("height") == null)
            : (constraints.maxWidth == double.infinity &&
                widget.control.getDouble("width") == null);

        if (unbounded) {
          return ErrorControl(
            "Error displaying PageView: ${horizontal ? "height" : "width"} is unbounded.",
            description:
                "Set a fixed ${horizontal ? "height" : "width"}, a non-zero expand,"
                " or place it inside a control with bounded ${horizontal ? "height" : "width"}.",
          );
        }

        return layoutChild;
      },
    );
  }
}
