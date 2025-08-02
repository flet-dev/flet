import '../extensions/control.dart';
import '../utils/borders.dart';
import '../utils/edge_insets.dart';
import '../utils/misc.dart';
import '../utils/colors.dart';
import '../utils/numbers.dart';
import '../utils/tabs.dart';
import '../utils/text.dart';
import '../utils/time.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/mouse.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class TabsControl extends StatefulWidget {
  final Control control;

  TabsControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<TabsControl> createState() => _TabsControlState();
}

class _TabsControlState extends State<TabsControl>
    with TickerProviderStateMixin {
  @override
  Widget build(BuildContext context) {
    debugPrint("TabsControl build: ${widget.control.id}");

    var content = widget.control.buildWidget("content");

    if (content == null) {
      return const ErrorControl("Tabs.content must be provided and visible");
    }

    return ConstrainedControl(
        control: widget.control,
        child: DefaultTabController(
            length: widget.control.getInt("length", 0)!,
            initialIndex: widget.control.getInt("initial_index", 0)!,
            animationDuration: widget.control.getDuration(
                "animation_duration", const Duration(milliseconds: 50))!,
            child: content));
  }
}

class TabBarViewControl extends StatelessWidget {
  final Control control;

  const TabBarViewControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("TabBarViewControl build: ${control.id}");

    return ConstrainedControl(
        control: control,
        child: TabBarView(
          clipBehavior:
              control.getClipBehavior("clip_behavior", Clip.hardEdge)!,
          viewportFraction: control.getDouble("viewport_fraction", 1.0)!,
          children: control.buildWidgets("controls"),
        ));
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

    var overlayColor =
        widget.control.getWidgetStateColor("overlay_color", Theme.of(context));
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
    var indicatorWeight = widget.control.getDouble("indicator_thickness", 2.0)!;
    var tabAlignment = widget.control.getTabAlignment(
        "tab_alignment", scrollable ? TabAlignment.start : TabAlignment.fill)!;
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

    var indicator =
        widget.control.getUnderlineTabIndicator("indicator", Theme.of(context));
    var indicatorSize = widget.control.getTabBarIndicatorSize("indicator_size");
    var indicatorAnimation =
        widget.control.getTabIndicatorAnimation("indicator_animation");

    debugPrint("TabBar indicatorAnimation: ${indicator?.borderSide.color}");

    TabBar? tabBar;

    if (secondary) {
      tabBar = TabBar.secondary(
          // controller: _tabController,
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
          // controller: _tabController,
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
  }
}
