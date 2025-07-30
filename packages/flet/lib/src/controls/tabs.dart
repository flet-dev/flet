import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

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

    var overlayColor = widget.control.getWidgetStateColor(
        "overlay_color", Theme.of(context),
        defaultValue: TabBarTheme.of(context).overlayColor);
    var indicatorBorderRadius =
        widget.control.getBorderRadius("indicator_border_radius");
    var indicatorBorderSide = widget.control
        .getBorderSide("indicator_border_side", Theme.of(context));
    var indicatorPadding =
        widget.control.getPadding("indicator_padding", EdgeInsets.zero)!;
    var indicatorColor = widget.control.getColor(
        "indicator_color",
        context,
        TabBarTheme.of(context).indicatorColor ??
            Theme.of(context).colorScheme.primary)!;
    var labelColor = widget.control.getColor(
        "label_color",
        context,
        TabBarTheme.of(context).labelColor ??
            Theme.of(context).colorScheme.primary);
    var unselectedLabelColor = widget.control.getColor(
        "unselected_label_color",
        context,
        TabBarTheme.of(context).unselectedLabelColor ??
            Theme.of(context).colorScheme.onSurface);
    var dividerColor = widget.control.getColor("divider_color", context) ??
        TabBarTheme.of(context).dividerColor;
    var themeIndicator =
        TabBarTheme.of(context).indicator as UnderlineTabIndicator?;
    var indicatorTabSize = widget.control.getBool("indicator_tab_size");
    var scrollable = widget.control.getBool("scrollable", true)!;
    var secondary = widget.control.getBool("secondary", false)!;
    var dividerHeight = widget.control.getDouble("divider_height");
    var enableFeedback = widget.control.getBool("enable_feedback");
    var indicatorWeight = widget.control.getDouble("indicator_thickness", 2.0)!;
    var tabAlignment = parseTabAlignment(
        widget.control.getString("tab_alignment"),
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

    var indicator = indicatorBorderRadius != null ||
            indicatorBorderSide != null ||
            indicatorPadding != null
        ? UnderlineTabIndicator(
            borderRadius: indicatorBorderRadius ??
                themeIndicator?.borderRadius ??
                const BorderRadius.only(
                    topLeft: Radius.circular(2), topRight: Radius.circular(2)),
            borderSide: indicatorBorderSide ??
                themeIndicator?.borderSide ??
                BorderSide(
                    width: themeIndicator?.borderSide.width ?? 2,
                    color: themeIndicator?.borderSide.color ?? indicatorColor),
            insets:
                indicatorPadding ?? themeIndicator?.insets ?? EdgeInsets.zero)
        : TabBarTheme.of(context).indicator;
    var indicatorSize = indicatorTabSize != null
        ? (indicatorTabSize
            ? TabBarIndicatorSize.tab
            : TabBarIndicatorSize.label)
        : TabBarTheme.of(context).indicatorSize;

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
          labelColor: labelColor,
          unselectedLabelColor: unselectedLabelColor,
          overlayColor: overlayColor,
          tabs: tabs,
          padding: padding,
          labelPadding: labelPadding,
          labelStyle: labelStyle,
          unselectedLabelStyle: unselectedLabelStyle,
          splashBorderRadius: splashBorderRadius,
          indicatorPadding: indicatorPadding,
          onTap: onTap);
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
          labelColor: labelColor,
          unselectedLabelColor: unselectedLabelColor,
          overlayColor: overlayColor,
          tabs: tabs,
          padding: padding,
          labelPadding: labelPadding,
          labelStyle: labelStyle,
          unselectedLabelStyle: unselectedLabelStyle,
          splashBorderRadius: splashBorderRadius,
          indicatorPadding: indicatorPadding,
          onTap: onTap);
    }

    return BaseControl(control: widget.control, child: tabBar);
  }
}
