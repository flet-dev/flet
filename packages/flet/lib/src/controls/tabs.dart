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
  String? _tabsSnapshot;
  TabController? _tabController;
  int _selectedIndex = 0;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    debugPrint("Tabs.didChangeDependencies: ${widget.control.id}");
    _configureTabController();
  }

  @override
  void didUpdateWidget(covariant TabsControl oldWidget) {
    debugPrint("Tabs.didUpdateWidget: ${widget.control.id}");
    super.didUpdateWidget(oldWidget);
    _configureTabController();
  }

  @override
  void dispose() {
    debugPrint("Tabs.dispose: ${widget.control.id}");
    _tabController?.removeListener(_tabChanged);
    _tabController?.dispose();
    super.dispose();
  }

  void _tabChanged() {
    if (_tabController!.indexIsChanging == true) {
      return;
    }
    var index = _tabController!.index;
    if (_selectedIndex != index) {
      widget.control.updateProperties({"selected_index": index});
      widget.control.triggerEvent("change", index);
      _selectedIndex = index;
    }
  }

  void _configureTabController() {
    var tabs = widget.control.children("tabs");
    var tabsSnapshot = tabs.map((tab) => tab.id.toString()).join();
    if (tabsSnapshot != _tabsSnapshot) {
      _tabsSnapshot = tabsSnapshot;

      if (_tabController != null) {
        _tabController!.removeListener(_tabChanged);
        _tabController!.dispose();
      }
      _selectedIndex = 0;
      _tabController = TabController(
          initialIndex: _selectedIndex,
          length: tabs.length,
          animationDuration: widget.control.getDuration(
              "animation_duration", const Duration(milliseconds: 50))!,
          vsync: this);
      _tabController!.addListener(_tabChanged);
    }

    var selectedIndex = widget.control.getInt("selected_index", 0)!;

    debugPrint("selectedIndex: $selectedIndex");

    if (selectedIndex > -1 &&
        selectedIndex < _tabController!.length &&
        _selectedIndex != selectedIndex) {
      _selectedIndex = selectedIndex;
      _tabController!.index = selectedIndex;
    }
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("TabsControl build: ${widget.control.id}");

    // check if all tabs have no content
    bool emptyTabs = !widget.control
        .children("tabs")
        .any((tab) => tab.child("content") != null);

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
    var isScrollable = widget.control.getBool("scrollable", true)!;
    var secondary = widget.control.getBool("is_secondary", false)!;
    var dividerHeight = widget.control.getDouble("divider_height");
    var enableFeedback = widget.control.getBool("enable_feedback");
    var indicatorWeight = widget.control.getDouble("indicator_thickness", 2.0)!;
    var tabAlignment = parseTabAlignment(
        widget.control.getString("tab_alignment"),
        isScrollable ? TabAlignment.start : TabAlignment.fill)!;
    var mouseCursor =
        parseMouseCursor(widget.control.getString("mouse_cursor"));
    var clipBehavior =
        widget.control.getClipBehavior("clip_behavior", Clip.hardEdge)!;
    var padding = parseEdgeInsets(widget.control.getPadding("padding"));
    var labelPadding = widget.control.getPadding("label_padding");
    var labelStyle =
        widget.control.getTextStyle("label_text_style", Theme.of(context));
    var unselectedLabelStyle = widget.control
        .getTextStyle("unselected_label_text_style", Theme.of(context));
    var splashBorderRadius =
        widget.control.getBorderRadius("splash_border_radius");

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

    var tabs = widget.control.children("tabs").map((tab) {
      tab.notifyParent = true;
      var icon = tab.buildIconOrWidget("icon");
      var label = tab.buildTextOrWidget("label");

      return Tab(
        icon: icon,
        height: tab.getDouble("height"),
        iconMargin: tab.getMargin("icon_margin"),
        child: label,
      );
    }).toList();

    TabBar? tabBar;

    if (secondary) {
      tabBar = TabBar.secondary(
          tabAlignment: tabAlignment,
          controller: _tabController,
          isScrollable: isScrollable,
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
          tabAlignment: tabAlignment,
          controller: _tabController,
          isScrollable: isScrollable,
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

    if (emptyTabs) {
      return tabBar;
    }

    var child = Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        tabBar,
        Expanded(
            child: TabBarView(
                controller: _tabController,
                clipBehavior: clipBehavior,
                children: widget.control.children("tabs").map((tab) {
                  return tab.buildWidget("content") ?? const SizedBox.shrink();
                }).toList()))
      ],
    );

    return ConstrainedControl(control: widget.control, child: child);
  }
}
