import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../flet_control_backend.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/controls_view_model.dart';
import '../utils/alignment.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/icons.dart';
import '../utils/material_state.dart';
import '../utils/mouse.dart';
import 'create_control.dart';

class TabsControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const TabsControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<TabsControl> createState() => _TabsControlState();
}

class _TabsControlState extends State<TabsControl>
    with TickerProviderStateMixin {
  String? _tabsSnapshot;
  TabController? _tabController;
  int _selectedIndex = 0;

  @override
  void dispose() {
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
      debugPrint("Selected index: $index");
      widget.backend.updateControlState(
          widget.control.id, {"selectedindex": index.toString()});
      widget.backend
          .triggerControlEvent(widget.control.id, "change", index.toString());
      _selectedIndex = index;
    }
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("TabsControl build: ${widget.control.id}");
    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    bool? adaptive =
        widget.control.attrBool("adaptive") ?? widget.parentAdaptive;

    // keep only visible tabs
    widget.children.retainWhere((c) => c.isVisible);

    var tabs = StoreConnector<AppState, ControlsViewModel>(
        distinct: true,
        converter: (store) => ControlsViewModel.fromStore(
            store, widget.children.map((c) => c.id)),
        builder: (content, viewModel) {
          var tabsSnapshot =
              viewModel.controlViews.map((c) => c.control.id).join();
          if (tabsSnapshot != _tabsSnapshot) {
            _tabsSnapshot = tabsSnapshot;

            if (_tabController != null) {
              _tabController!.removeListener(_tabChanged);
              _tabController!.dispose();
            }
            _tabController = TabController(
                length: viewModel.controlViews.length,
                animationDuration: Duration(
                    milliseconds:
                        widget.control.attrInt("animationDuration", 50)!),
                vsync: this);
            _tabController!.addListener(_tabChanged);
          }

          var selectedIndex = widget.control.attrInt("selectedIndex", 0)!;

          if (selectedIndex > -1 &&
              selectedIndex < _tabController!.length &&
              _selectedIndex != selectedIndex) {
            _selectedIndex = selectedIndex;
            _tabController!.index = selectedIndex;
          }

          // check if all tabs have no content
          bool emptyTabs = !viewModel.controlViews
              .any((t) => t.children.any((c) => c.name == "content"));

          var overlayColorStr = widget.control.attrString("overlayColor");
          dynamic overlayColor;
          if (overlayColorStr != null) {
            overlayColor = getMaterialStateProperty<Color?>(
                    json.decode(overlayColorStr),
                    (jv) =>
                        HexColor.fromString(Theme.of(context), jv as String),
                    null) ??
                TabBarTheme.of(context).overlayColor;
          }

          var indicatorBorderRadius =
              parseBorderRadius(widget.control, "indicatorBorderRadius");
          var indicatorBorderSide = parseBorderSide(
              Theme.of(context), widget.control, "indicatorBorderSide");
          var indicatorPadding =
              parseEdgeInsets(widget.control, "indicatorPadding");

          var indicatorColor =
              widget.control.attrColor("indicatorColor", context) ??
                  TabBarTheme.of(context).indicatorColor ??
                  Theme.of(context).colorScheme.primary;
          var labelColor = widget.control.attrColor("labelColor", context) ??
              TabBarTheme.of(context).labelColor ??
              Theme.of(context).colorScheme.primary;
          var unselectedLabelColor =
              widget.control.attrColor("unselectedLabelColor", context) ??
                  TabBarTheme.of(context).unselectedLabelColor ??
                  Theme.of(context).colorScheme.onSurface;
          var dividerColor =
              widget.control.attrColor("dividerColor", context) ??
                  TabBarTheme.of(context).dividerColor;

          var themeIndicator =
              TabBarTheme.of(context).indicator as UnderlineTabIndicator?;
          var indicatorTabSize = widget.control.attrBool("indicatorTabSize");
          var isScrollable = widget.control.attrBool("scrollable", true)!;
          var secondary = widget.control.attrBool("isSecondary", false)!;
          var dividerHeight = widget.control.attrDouble("dividerHeight");
          var enableFeedback = widget.control.attrBool("enableFeedback");
          var indicatorWeight =
              widget.control.attrDouble("indicatorThickness", 2.0)!;
          var tabAlignment = parseTabAlignment(widget.control, "tabAlignment",
              isScrollable ? TabAlignment.start : TabAlignment.fill);
          var mouseCursor =
              parseMouseCursor(widget.control.attrString("mouseCursor"));
          var clipBehavior = Clip.values.firstWhere(
              (e) =>
                  e.name.toLowerCase() ==
                  widget.control.attrString("clipBehavior", "")!.toLowerCase(),
              orElse: () => Clip.hardEdge);

          var indicator = indicatorBorderRadius != null ||
                  indicatorBorderSide != null ||
                  indicatorPadding != null
              ? UnderlineTabIndicator(
                  borderRadius: indicatorBorderRadius ??
                      themeIndicator?.borderRadius ??
                      const BorderRadius.only(
                          topLeft: Radius.circular(2),
                          topRight: Radius.circular(2)),
                  borderSide: indicatorBorderSide ??
                      themeIndicator?.borderSide ??
                      BorderSide(
                          width: themeIndicator?.borderSide.width ?? 2,
                          color: themeIndicator?.borderSide.color ??
                              indicatorColor),
                  insets: indicatorPadding ??
                      themeIndicator?.insets ??
                      EdgeInsets.zero)
              : TabBarTheme.of(context).indicator;
          var indicatorSize = indicatorTabSize != null
              ? (indicatorTabSize
                  ? TabBarIndicatorSize.tab
                  : TabBarIndicatorSize.label)
              : TabBarTheme.of(context).indicatorSize;

          var tabs = viewModel.controlViews.map((tabView) {
            var text = tabView.control.attrString("text");
            var icon = parseIcon(tabView.control.attrString("icon", "")!);
            var tabContentCtrls = tabView.children
                .where((c) => c.name == "tab_content" && c.isVisible);

            Widget tabChild;
            List<Widget> widgets = [];
            if (tabContentCtrls.isNotEmpty) {
              tabChild = createControl(
                  widget.control, tabContentCtrls.first.id, disabled,
                  parentAdaptive: adaptive);
            } else {
              if (icon != null) {
                widgets.add(Icon(icon));
                if (text != null) {
                  widgets.add(const SizedBox(width: 8));
                }
              }
              if (text != null) {
                widgets.add(Text(text));
              }
              tabChild = Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: widgets);
            }
            return Tab(child: tabChild);
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
                tabs: tabs);
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
                tabs: tabs);
          }

          debugPrint("tabs.length: ${tabBar.tabs.length}");

          if (emptyTabs) {
            return tabBar;
          }

          return Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              tabBar,
              Expanded(
                  child: TabBarView(
                      controller: _tabController,
                      clipBehavior: clipBehavior,
                      children: viewModel.controlViews.map((tabView) {
                        var contentCtrls = tabView.children
                            .where((c) => c.name == "content" && c.isVisible);
                        if (contentCtrls.isEmpty) {
                          return const SizedBox.shrink();
                        }
                        return createControl(
                            widget.control, contentCtrls.first.id, disabled,
                            parentAdaptive: adaptive);
                      }).toList()))
            ],
          );
        });

    return constrainedControl(context, tabs, widget.parent, widget.control);
  }
}
