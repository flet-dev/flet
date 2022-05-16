import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/controls_view_model.dart';
import '../protocol/update_control_props_payload.dart';
import '../utils/icons.dart';
import '../web_socket_client.dart';
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
      ws.updateControlProps(props: props);
      ws.pageEventFromWeb(
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

          var tabBar = TabBar(
              controller: _tabController,
              isScrollable: true,
              indicatorColor: Theme.of(context).colorScheme.primary,
              labelColor: Theme.of(context).colorScheme.primary,
              unselectedLabelColor: Theme.of(context).colorScheme.onSurface,
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
                      children: widgets,
                      mainAxisAlignment: MainAxisAlignment.center);
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

    return constrainedControl(tabs, widget.parent, widget.control);
  }
}
