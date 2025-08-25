import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/animations.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/layout.dart';
import '../utils/misc.dart';
import '../utils/mouse.dart';
import '../utils/numbers.dart';
import '../utils/tabs.dart';
import '../utils/text.dart';
import '../utils/time.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

/// Default duration for tab animation if none is provided.
const Duration kDefaultTabAnimationDuration = Duration(milliseconds: 100);

class TabsControl extends StatefulWidget {
  final Control control;

  TabsControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<TabsControl> createState() => _TabsControlState();
}

class _TabsControlState extends State<TabsControl>
    with TickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    widget.control.addInvokeMethodListener(_invokeMethod);
    _initTabController();
  }

  @override
  void didUpdateWidget(TabsControl oldWidget) {
    super.didUpdateWidget(oldWidget);
    final animationDuration = widget.control
        .getDuration("animation_duration", kDefaultTabAnimationDuration)!;
    final newLength = widget.control.getInt("length", 0)!;
    final newSelectedIndex = widget.control.getInt("selected_index", 0)!;

    // Resolve Python-style negative index (e.g., -1 means last tab)
    final resolvedIndex =
        newSelectedIndex < 0 ? newLength + newSelectedIndex : newSelectedIndex;

    // Clamp the index to ensure it's within [0, length - 1]
    final selectedIndex = resolvedIndex.clamp(0, newLength - 1);

    // If the number of tabs has changed, we must recreate the controller
    if (newLength != _tabController.length) {
      // Save the current index before disposing the controller
      int currentIndex = _tabController.index;

      // Dispose of the old controller
      _tabController.dispose();

      // Update selected_index so we can preserve the current selection
      widget.control.updateProperties({"selected_index": currentIndex});

      // Re-initialize the TabController with the new length
      _initTabController(currentIndex);
    }

    // If the selected tab has changed, animate to the new tab
    else if (selectedIndex != _tabController.index) {
      _tabController.animateTo(
        selectedIndex,
        duration: animationDuration,
        curve: Curves.ease,
      );
    }
  }

  void _initTabController([int? index]) {
    final animationDuration = widget.control
        .getDuration("animation_duration", kDefaultTabAnimationDuration)!;
    final length = widget.control.getInt("length", 0)!;
    final selectedIndex = index ?? widget.control.getInt("selected_index", 0)!;

    // Support Python-style negative indices (e.g., -1 is the last tab)
    final resolvedIndex =
        selectedIndex < 0 ? length + selectedIndex : selectedIndex;

    // Clamp to ensure initialIndex is within [0, length - 1]
    final initialIndex = resolvedIndex.clamp(0, length - 1);

    _tabController = TabController(
      length: length,
      initialIndex: initialIndex,
      vsync: this,
      animationDuration: animationDuration,
    );
    _tabController.addListener(_handleTabSelection);
  }

  void _handleTabSelection() {
    if (!_tabController.indexIsChanging) {
      // Update the selected_index property to reflect the current tab
      widget.control.updateProperties({"selected_index": _tabController.index});
      widget.control.triggerEvent("change", _tabController.index);
    }
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("TabsControl.$name($args)");
    switch (name) {
      case "move_to":
        return _tabController.animateTo(
          args["index"],
          curve: parseCurve(args["curve"], Curves.ease)!,
          duration:
              parseDuration(args["duration"], kDefaultTabAnimationDuration)!,
        );
      default:
        throw Exception("Unknown Tabs method: $name");
    }
  }

  @override
  void dispose() {
    _tabController.removeListener(_handleTabSelection);
    widget.control.removeInvokeMethodListener(_invokeMethod);
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("TabsControl build: ${widget.control.id}");
    var content = widget.control.buildWidget("content");
    if (content == null) {
      return const ErrorControl("Tabs.content must be provided and visible");
    }

    return LayoutControl(control: widget.control, child: content);
  }
}

class TabBarViewControl extends StatelessWidget {
  final Control control;

  const TabBarViewControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("TabBarViewControl build: ${control.id}");

    // Find the TabController from the nearest TabsControl ancestor
    final tabsState = context.findAncestorStateOfType<_TabsControlState>();
    if (tabsState == null) {
      return const ErrorControl(
          "TabBarView must be used within a Tabs control");
    }

    final tabController = tabsState._tabController;

    Widget buildLayoutTabView() {
      return LayoutControl(
          control: control,
          child: TabBarView(
            controller: tabController,
            clipBehavior:
                control.getClipBehavior("clip_behavior", Clip.hardEdge)!,
            viewportFraction: control.getDouble("viewport_fraction", 1.0)!,
            children: control.buildWidgets("controls"),
          ));
    }

    // If expand property was set, we return the result directly.
    // Because having Expanded as direct child of LayoutBuilder is not allowed.
    if (control.getExpand("expand", 0)! > 0) {
      return buildLayoutTabView();
    }

    return LayoutBuilder(
      builder: (context, constraints) {
        final hasFixedHeight = control.getDouble("height") != null;
        final hasUnboundedHeight =
            constraints.maxHeight == double.infinity && !hasFixedHeight;

        if (hasUnboundedHeight) {
          return const ErrorControl(
            "Error displaying TabBarView: height is unbounded.",
            description:
                "Set a fixed height, a non-zero expand, or place it inside a control with bounded height.",
          );
        }

        return buildLayoutTabView();
      },
    );
  }
}

class TabControl extends StatelessWidget {
  final Control control;

  const TabControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("TabControl build: ${control.id}");

    return BaseControl(
        control: control,
        child: Tab(
          icon: control.buildIconOrWidget("icon"),
          height: control.getDouble("height"),
          iconMargin: control.getMargin("icon_margin"),
          child: control.buildTextOrWidget("label"),
        ));
  }
}

class TabBarControl extends StatefulWidget {
  final Control control;

  const TabBarControl({super.key, required this.control});

  @override
  State<TabBarControl> createState() => _TabBarControlState();
}

class _TabBarControlState extends State<TabBarControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("TabBarControl build: ${widget.control.id}");

    // Find the TabController from the nearest TabsControl ancestor
    final tabsState = context.findAncestorStateOfType<_TabsControlState>();
    if (tabsState != null) {
      final tabController = tabsState._tabController;

      var overlayColor = widget.control
          .getWidgetStateColor("overlay_color", Theme.of(context));
      var indicatorPadding =
          widget.control.getPadding("indicator_padding", EdgeInsets.zero)!;
      var indicatorColor = widget.control.getColor("indicator_color", context);
      var labelColor = widget.control.getColor("label_color", context);
      var unselectedLabelColor =
          widget.control.getColor("unselected_label_color", context);
      var dividerColor = widget.control.getColor("divider_color", context);
      var scrollable = widget.control.getBool("scrollable", true)!;
      var secondary = widget.control.getBool("secondary", false)!;
      var dividerHeight = widget.control.getDouble("divider_height");
      var enableFeedback = widget.control.getBool("enable_feedback");
      var indicatorWeight =
          widget.control.getDouble("indicator_thickness", 2.0)!;
      var tabAlignment = widget.control.getTabAlignment("tab_alignment",
          scrollable ? TabAlignment.start : TabAlignment.fill)!;
      var mouseCursor =
          parseMouseCursor(widget.control.getString("mouse_cursor"));
      var padding = parseEdgeInsets(widget.control.getPadding("padding"));
      var labelPadding = widget.control.getPadding("label_padding");
      var labelStyle =
          widget.control.getTextStyle("label_text_style", Theme.of(context));
      var unselectedLabelStyle = widget.control
          .getTextStyle("unselected_label_text_style", Theme.of(context));
      var splashBorderRadius =
          widget.control.getBorderRadius("splash_border_radius");
      var tabs = widget.control.buildWidgets("tabs");

      void onTap(int index) {
        widget.control.triggerEvent("click", index);
      }

      void onHover(bool hovering, int? index) {
        widget.control
            .triggerEvent("hover", {"hovering": hovering, "index": index});
      }

      var indicator = widget.control
          .getUnderlineTabIndicator("indicator", Theme.of(context));
      var indicatorSize =
          widget.control.getTabBarIndicatorSize("indicator_size");
      var indicatorAnimation =
          widget.control.getTabIndicatorAnimation("indicator_animation");

      debugPrint("TabBar indicator: ${indicator?.borderSide}");

      TabBar? tabBar;

      if (secondary) {
        tabBar = TabBar.secondary(
            controller: tabController,
            tabAlignment: tabAlignment,
            isScrollable: scrollable,
            dividerHeight: dividerHeight,
            enableFeedback: enableFeedback,
            mouseCursor: mouseCursor,
            indicatorWeight: indicatorWeight,
            dividerColor: dividerColor,
            indicatorSize: indicatorSize,
            indicator: indicator,
            indicatorColor: indicatorColor,
            indicatorPadding: indicatorPadding,
            indicatorAnimation: indicatorAnimation,
            labelColor: labelColor,
            unselectedLabelColor: unselectedLabelColor,
            overlayColor: overlayColor,
            tabs: tabs,
            padding: padding,
            labelPadding: labelPadding,
            labelStyle: labelStyle,
            unselectedLabelStyle: unselectedLabelStyle,
            splashBorderRadius: splashBorderRadius,
            onTap: onTap,
            onHover: onHover);
      } else {
        tabBar = TabBar(
            controller: tabController,
            tabAlignment: tabAlignment,
            isScrollable: scrollable,
            dividerHeight: dividerHeight,
            enableFeedback: enableFeedback,
            mouseCursor: mouseCursor,
            indicatorWeight: indicatorWeight,
            dividerColor: dividerColor,
            indicatorSize: indicatorSize,
            indicator: indicator,
            indicatorColor: indicatorColor,
            indicatorPadding: indicatorPadding,
            indicatorAnimation: indicatorAnimation,
            labelColor: labelColor,
            unselectedLabelColor: unselectedLabelColor,
            overlayColor: overlayColor,
            tabs: tabs,
            padding: padding,
            labelPadding: labelPadding,
            labelStyle: labelStyle,
            unselectedLabelStyle: unselectedLabelStyle,
            splashBorderRadius: splashBorderRadius,
            onTap: onTap,
            onHover: onHover);
      }

      return BaseControl(control: widget.control, child: tabBar);
    } else {
      return const ErrorControl("TabBar must be used within a Tabs control");
    }
  }
}
