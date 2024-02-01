import 'package:collection/collection.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../models/app_state.dart';
import '../models/control.dart';
import '../models/controls_view_model.dart';
import '../utils/colors.dart';
import 'app_bar.dart';
import 'create_control.dart';
import 'cupertino_app_bar.dart';
import 'error.dart';
import 'flet_control_stateful_mixin.dart';
import 'floating_action_button.dart';
import 'navigation_drawer.dart';

class PageletControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;

  const PageletControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive});

  @override
  State<PageletControl> createState() => _PageletControlState();
}

class _PageletControlState extends State<PageletControl>
    with FletControlStatefulMixin {
  final scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  Widget build(BuildContext context) {
    debugPrint("Pagelet build: ${widget.control.id}");

    var appBarCtrls =
        widget.children.where((c) => c.name == "appbar" && c.isVisible);
    var contentCtrls =
        widget.children.where((c) => c.name == "content" && c.isVisible);
    var navigationBarCtrls =
        widget.children.where((c) => c.name == "navigationbar" && c.isVisible);
    var bottomAppBarCtrls =
        widget.children.where((c) => c.name == "bottomappbar" && c.isVisible);
    var bottomSheetCtrls =
        widget.children.where((c) => c.name == "bottomsheet" && c.isVisible);
    var drawerCtrls =
        widget.children.where((c) => c.name == "drawer" && c.isVisible);
    var endDrawerCtrls =
        widget.children.where((c) => c.name == "enddrawer" && c.isVisible);
    var fabCtrls = widget.children
        .where((c) => c.name == "floatingactionbutton" && c.isVisible);

    if (contentCtrls.isEmpty) {
      return const ErrorControl("Pagelet must have content specified.");
    }

    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    bool? adaptive =
        widget.control.attrBool("adaptive") ?? widget.parentAdaptive;

    var bgcolor = HexColor.fromString(
        Theme.of(context), widget.control.attrString("bgcolor", "")!);

    List<String> childIds = [
      appBarCtrls.firstOrNull?.id,
      drawerCtrls.firstOrNull?.id,
      endDrawerCtrls.firstOrNull?.id
    ].whereNotNull().toList();

    return StoreConnector<AppState, ControlsViewModel>(
        distinct: true,
        converter: (store) => ControlsViewModel.fromStore(store, childIds),
        ignoreChange: (state) {
          //debugPrint("ignoreChange: $id");
          for (var id in childIds) {
            if (state.controls[id] == null) {
              return true;
            }
          }
          return false;
        },
        builder: (context, childrenViews) {
          var navBar = navigationBarCtrls.isNotEmpty
              ? createControl(
                  widget.control, navigationBarCtrls.first.id, disabled,
                  parentAdaptive: adaptive)
              : null;
          var bottomAppBar = bottomAppBarCtrls.isNotEmpty
              ? createControl(
                  widget.control, bottomAppBarCtrls.first.id, disabled,
                  parentAdaptive: adaptive)
              : null;
          var bnb = navBar ?? bottomAppBar;

          var appBarView = childrenViews.controlViews.firstWhereOrNull(
              (v) => v.control.id == (appBarCtrls.firstOrNull?.id ?? ""));

          var drawerView = childrenViews.controlViews.firstWhereOrNull(
              (v) => v.control.id == (drawerCtrls.firstOrNull?.id ?? ""));
          var endDrawerView = childrenViews.controlViews.firstWhereOrNull(
              (v) => v.control.id == (endDrawerCtrls.firstOrNull?.id ?? ""));

          final bool? drawerOpened = widget.control.state["drawerOpened"];
          final bool? endDrawerOpened = widget.control.state["endDrawerOpened"];

          final fabLocation = parseFloatingActionButtonLocation(
              widget.control,
              "floatingActionButtonLocation",
              FloatingActionButtonLocation.endFloat);

          void dismissDrawer(String id) {
            updateControlProps(id, {"open": "false"});
            sendControlEvent(id, "dismiss", "");
          }

          WidgetsBinding.instance.addPostFrameCallback((_) {
            if (drawerView != null) {
              if (scaffoldKey.currentState?.isDrawerOpen == false &&
                  drawerOpened == true) {
                widget.control.state["drawerOpened"] = false;
                dismissDrawer(drawerView.control.id);
              }
              if (drawerView.control.attrBool("open", false)! &&
                  drawerOpened != true) {
                if (scaffoldKey.currentState?.isEndDrawerOpen == true) {
                  scaffoldKey.currentState?.closeEndDrawer();
                }
                Future.delayed(const Duration(milliseconds: 1)).then((value) {
                  scaffoldKey.currentState?.openDrawer();
                  widget.control.state["drawerOpened"] = true;
                });
              } else if (!drawerView.control.attrBool("open", false)! &&
                  drawerOpened == true) {
                scaffoldKey.currentState?.closeDrawer();
                widget.control.state["drawerOpened"] = false;
              }
            }
            if (endDrawerView != null) {
              if (scaffoldKey.currentState?.isEndDrawerOpen == false &&
                  endDrawerOpened == true) {
                widget.control.state["endDrawerOpened"] = false;
                dismissDrawer(endDrawerView.control.id);
              }
              if (endDrawerView.control.attrBool("open", false)! &&
                  endDrawerOpened != true) {
                if (scaffoldKey.currentState?.isDrawerOpen == true) {
                  scaffoldKey.currentState?.closeDrawer();
                }
                Future.delayed(const Duration(milliseconds: 1)).then((value) {
                  scaffoldKey.currentState?.openEndDrawer();
                  widget.control.state["endDrawerOpened"] = true;
                });
              } else if (!endDrawerView.control.attrBool("open", false)! &&
                  endDrawerOpened == true) {
                scaffoldKey.currentState?.closeEndDrawer();
                widget.control.state["endDrawerOpened"] = false;
              }
            }
          });

          var bar = appBarView != null
              ? appBarView.control.type == "appbar"
                  ? AppBarControl(
                      parent: widget.control,
                      control: appBarView.control,
                      children: appBarView.children,
                      parentDisabled: widget.control.isDisabled,
                      parentAdaptive: adaptive,
                      height: appBarView.control
                          .attrDouble("toolbarHeight", kToolbarHeight)!)
                  : appBarView.control.type == "cupertinoappbar"
                      ? CupertinoAppBarControl(
                          parent: widget.control,
                          control: appBarView.control,
                          children: appBarView.children,
                          parentDisabled: widget.control.isDisabled,
                          parentAdaptive: adaptive,
                          bgcolor: HexColor.fromString(Theme.of(context),
                              appBarView.control.attrString("bgcolor", "")!),
                        ) as ObstructingPreferredSizeWidget
                      : null
              : null;
          return constrainedControl(
              context,
              Scaffold(
                  key: scaffoldKey,
                  appBar: bar,
                  backgroundColor: bgcolor,
                  //backgroundColor: Colors.red,
                  drawer: drawerView != null
                      ? NavigationDrawerControl(
                          control: drawerView.control,
                          children: drawerView.children,
                          parentDisabled: widget.control.isDisabled,
                          parentAdaptive: adaptive,
                        )
                      : null,
                  onDrawerChanged: (opened) {
                    if (drawerView != null && !opened) {
                      widget.control.state["drawerOpened"] = false;
                      dismissDrawer(drawerView.control.id);
                    }
                  },
                  endDrawer: endDrawerView != null
                      ? NavigationDrawerControl(
                          control: endDrawerView.control,
                          children: endDrawerView.children,
                          parentDisabled: widget.control.isDisabled,
                          parentAdaptive: adaptive,
                        )
                      : null,
                  onEndDrawerChanged: (opened) {
                    if (endDrawerView != null && !opened) {
                      widget.control.state["endDrawerOpened"] = false;
                      dismissDrawer(endDrawerView.control.id);
                    }
                  },
                  body: contentCtrls.isNotEmpty
                      ? createControl(
                          widget.control, contentCtrls.first.id, disabled,
                          parentAdaptive: adaptive)
                      : null,
                  bottomNavigationBar: bnb,
                  bottomSheet: bottomSheetCtrls.isNotEmpty
                      ? createControl(
                          widget.control, bottomSheetCtrls.first.id, disabled,
                          parentAdaptive: adaptive)
                      : null,
                  floatingActionButton: fabCtrls.isNotEmpty
                      ? createControl(
                          widget.control, fabCtrls.first.id, disabled,
                          parentAdaptive: adaptive)
                      : null,
                  floatingActionButtonLocation: fabLocation),
              widget.parent,
              widget.control);
        });
  }
}
