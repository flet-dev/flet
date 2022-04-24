import 'package:flet_view/controls/error.dart';
import 'package:flet_view/utils/icons.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../models/app_state.dart';
import '../models/control.dart';
import '../models/control_view_model.dart';
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
  int _tabsCount = 0;
  List<String> _tabsIndex = [];
  String? _value;
  TabController? _tabController;

  @override
  void initState() {
    super.initState();
    _tabsIndex = widget.children.map((c) => c.attrString("key", "")!).toList();
    _tabsCount = widget.children.length;
    _tabController = TabController(length: _tabsCount, vsync: this);
    _tabController!.addListener(() {
      if (_tabController!.indexIsChanging == true) {
        return;
      }
      var value = _tabsIndex[_tabController!.index];
      if (_value != value) {
        debugPrint("Selected tab: $value");
      }
      _value = value;
    });
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("TabsControl build: ${widget.control.id}");

    if (widget.children.length != _tabsCount) {
      _tabsCount = widget.children.length;
      _tabController = TabController(length: _tabsCount, vsync: this);
    }

    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    String? value = widget.control.attrString("value");
    if (_value != value) {
      _value = value;

      int idx = _tabsIndex.indexOf(_value ?? "");
      if (idx != -1) {
        _tabController!.index = idx;
      }
    }

    var tabs = Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        TabBar(
            controller: _tabController,
            isScrollable: true,
            indicatorColor: Theme.of(context).colorScheme.primary,
            labelColor: Theme.of(context).colorScheme.primary,
            unselectedLabelColor: Theme.of(context).colorScheme.onSurface,
            tabs: widget.children
                .map((c) => StoreConnector<AppState, ControlViewModel>(
                    distinct: true,
                    converter: (store) {
                      return ControlViewModel.fromStore(store, c.id);
                    },
                    builder: (context, tabView) {
                      var text = tabView.control.attrString("text");
                      var icon = getMaterialIcon(
                          tabView.control.attrString("icon", "")!);
                      var tabContentCtrls = tabView.children
                          .where((c) => c.name == "tab_content");

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
                    }))
                .toList()),
        Expanded(
            child: TabBarView(
                controller: _tabController,
                children: widget.children
                    .map((c) => StoreConnector<AppState, ControlViewModel>(
                        distinct: true,
                        converter: (store) {
                          return ControlViewModel.fromStore(store, c.id);
                        },
                        builder: (context, tabView) {
                          var contentCtrls = tabView.children
                              .where((c) => c.name == "content");
                          if (contentCtrls.isEmpty) {
                            return const ErrorControl(
                                "Tab should have a content.");
                          }
                          return createControl(
                              widget.control, contentCtrls.first.id, disabled);
                        }))
                    .toList()))
      ],
    );

    return constrainedControl(tabs, widget.parent, widget.control);
  }
}
