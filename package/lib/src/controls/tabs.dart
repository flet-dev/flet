import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/controls_view_model.dart';
import '../protocol/update_control_props_payload.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/icons.dart';
import '../utils/material_state.dart';
import 'create_control.dart';

class TabsControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const TabsControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  State<TabsControl> createState() => _TabsControlState();
}

class _TabsControlState extends State<TabsControl>
    with TickerProviderStateMixin {
  List<String> _tabsIndex = [];
  TabController? _tabController;
  int _selectedIndex = 0;
  dynamic _dispatch;

  @override
  void initState() {
    super.initState();
    _tabsIndex = widget.children.map((c) => c.id).toList();
    _tabController = TabController(
        length: _tabsIndex.length,
        animationDuration: Duration(
            milliseconds: widget.control.attrInt("animationDuration", 50)!),
        vsync: this);
    _tabController!.addListener(_tabChanged);
  }

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
      List<Map<String, String>> props = [
        {"i": widget.control.id, "selectedindex": index.toString()}
      ];
      _dispatch(
          UpdateControlPropsAction(UpdateControlPropsPayload(props: props)));
      final server = FletAppServices.of(context).server;
      server.updateControlProps(props: props);
      server.sendPageEvent(
          eventTarget: widget.control.id,
          eventName: "change",
          eventData: index.toString());
      _selectedIndex = index;
    }
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("TabsControl build: ${widget.control.id}");

    var tabsIndex = widget.children.map((c) => c.id).toList();
    if (tabsIndex.length != _tabsIndex.length ||
        !tabsIndex.every((item) => _tabsIndex.contains(item))) {
      _tabsIndex = tabsIndex;
      if (_tabController != null) {
        _tabController!.removeListener(_tabChanged);
        _tabController!.dispose();
      }
      _tabController = TabController(
          length: _tabsIndex.length,
          animationDuration: Duration(
              milliseconds: widget.control.attrInt("animationDuration", 50)!),
          vsync: this);
      _tabController!.addListener(_tabChanged);
    }

    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var selectedIndex = widget.control.attrInt("selectedIndex", 0)!;

    if (selectedIndex > -1 &&
        selectedIndex < tabsIndex.length &&
        _selectedIndex != selectedIndex) {
      _selectedIndex = selectedIndex;
      _tabController!.index = selectedIndex;
    }

    var tabs = StoreConnector<AppState, ControlsViewModel>(
        distinct: true,
        converter: (store) => ControlsViewModel.fromStore(
            store, widget.children.map((c) => c.id)),
        builder: (content, viewModel) {
          _dispatch = viewModel.dispatch;

          // check if all tabs have no content
          bool emptyTabs = !viewModel.controlViews
              .any((t) => t.children.any((c) => c.name == "content"));

          var overlayColorStr = widget.control.attrString("overlayColor");
          dynamic overlayColor;
          if (overlayColorStr != null) {
            overlayColor = json.decode(overlayColorStr);
          }

          var indicatorBorderRadius =
              parseBorderRadius(widget.control, "indicatorBorderRadius");
          var inidicatorBorderSide = parseBorderSide(
              Theme.of(context), widget.control, "inidicatorBorderSide");
          var indicatorPadding =
              parseEdgeInsets(widget.control, "indicatorPadding");

          var inidicatorColor = HexColor.fromString(Theme.of(context),
                  widget.control.attrString("indicatorColor", "")!) ??
              TabBarTheme.of(context).indicatorColor ??
              Theme.of(context).colorScheme.primary;

          var themeIndicator =
              TabBarTheme.of(context).indicator as UnderlineTabIndicator?;

          var indicatorTabSize = widget.control.attrBool("indicatorTabSize");

          var tabBar = TabBar(
              controller: _tabController,
              isScrollable: widget.control.attrBool("scrollable", true)!,
              dividerColor:
                  HexColor.fromString(Theme.of(context), widget.control.attrString("dividerColor", "")!) ??
                      TabBarTheme.of(context).dividerColor,
              indicatorSize: indicatorTabSize != null
                  ? (indicatorTabSize
                      ? TabBarIndicatorSize.tab
                      : TabBarIndicatorSize.label)
                  : TabBarTheme.of(context).indicatorSize,
              indicator: indicatorBorderRadius != null ||
                      inidicatorBorderSide != null ||
                      indicatorPadding != null
                  ? UnderlineTabIndicator(
                      borderRadius: indicatorBorderRadius ??
                          themeIndicator?.borderRadius ??
                          const BorderRadius.only(
                              topLeft: Radius.circular(2),
                              topRight: Radius.circular(2)),
                      borderSide: inidicatorBorderSide ??
                          themeIndicator?.borderSide ??
                          BorderSide(
                              width: themeIndicator?.borderSide.width ?? 2,
                              color: themeIndicator?.borderSide.color ??
                                  inidicatorColor),
                      insets: indicatorPadding ??
                          themeIndicator?.insets ??
                          EdgeInsets.zero)
                  : TabBarTheme.of(context).indicator,
              indicatorColor: inidicatorColor,
              labelColor: HexColor.fromString(Theme.of(context), widget.control.attrString("labelColor", "")!) ??
                  TabBarTheme.of(context).labelColor ??
                  Theme.of(context).colorScheme.primary,
              unselectedLabelColor:
                  HexColor.fromString(Theme.of(context), widget.control.attrString("unselectedLabelColor", "")!) ??
                      TabBarTheme.of(context).unselectedLabelColor ??
                      Theme.of(context).colorScheme.onSurface,
              overlayColor: getMaterialStateProperty(
                      overlayColor, (jv) => HexColor.fromString(Theme.of(context), jv as String), null) ??
                  TabBarTheme.of(context).overlayColor,
              tabs: viewModel.controlViews.map((tabView) {
                var text = tabView.control.attrString("text");
                var icon =
                    getMaterialIcon(tabView.control.attrString("icon", "")!);
                var tabContentCtrls = tabView.children
                    .where((c) => c.name == "tab_content" && c.isVisible);

                Widget tabChild;
                List<Widget> widgets = [];
                if (tabContentCtrls.isNotEmpty) {
                  tabChild = createControl(
                      widget.control, tabContentCtrls.first.id, disabled);
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
              }).toList());

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
                      children: viewModel.controlViews.map((tabView) {
                        var contentCtrls = tabView.children
                            .where((c) => c.name == "content" && c.isVisible);
                        if (contentCtrls.isEmpty) {
                          return const SizedBox.shrink();
                        }
                        return createControl(
                            widget.control, contentCtrls.first.id, disabled);
                      }).toList()))
            ],
          );
        });

    return constrainedControl(context, tabs, widget.parent, widget.control);
  }
}
