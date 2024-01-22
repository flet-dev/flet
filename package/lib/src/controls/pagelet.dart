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

class PageletControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final dynamic dispatch;

  const PageletControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.dispatch});

  @override
  State<PageletControl> createState() => _PageletControlState();
}

class _PageletControlState extends State<PageletControl> {
  // bool _selected = false;

  // late final FocusNode _focusNode;

  // @override
  // void initState() {
  //   super.initState();
  //   _focusNode = FocusNode();
  //   _focusNode.addListener(_onFocusChange);
  // }

  // @override
  // void dispose() {
  //   _focusNode.removeListener(_onFocusChange);
  //   _focusNode.dispose();
  //   super.dispose();
  // }

  // void _onSelect(bool selected) {
  //   var strSelected = selected.toString();
  //   debugPrint(strSelected);
  //   setState(() {
  //     _selected = selected;
  //   });
  //   List<Map<String, String>> props = [
  //     {"i": widget.control.id, "selected": strSelected}
  //   ];
  //   widget.dispatch(
  //       UpdateControlPropsAction(UpdateControlPropsPayload(props: props)));
  //   final server = FletAppServices.of(context).server;
  //   server.updateControlProps(props: props);
  //   server.sendPageEvent(
  //       eventTarget: widget.control.id,
  //       eventName: "select",
  //       eventData: strSelected);
  // }

  // void _onFocusChange() {
  //   FletAppServices.of(context).server.sendPageEvent(
  //       eventTarget: widget.control.id,
  //       eventName: _focusNode.hasFocus ? "focus" : "blur",
  //       eventData: "");
  //}

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

    if (contentCtrls.isEmpty) {
      return const ErrorControl("Pagelet must have content specified.");
    }

    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var bgcolor = HexColor.fromString(
        Theme.of(context), widget.control.attrString("bgcolor", "")!);

    List<String> childIds = [
      appBarCtrls.firstOrNull?.id,
      // drawer?.id,
      // endDrawer?.id
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
                  widget.control, navigationBarCtrls.first.id, disabled)
              : null;
          var bottomAppBar = bottomAppBarCtrls.isNotEmpty
              ? createControl(
                  widget.control, bottomAppBarCtrls.first.id, disabled)
              : null;
          var bnb = navBar ?? bottomAppBar;

          // var drawer = drawerCtrls.isNotEmpty
          //     ? createControl(widget.control, drawerCtrls.first.id, disabled)
          //     : null;

          // var endDrawer = endDrawerCtrls.isNotEmpty
          //     ? createControl(widget.control, endDrawerCtrls.first.id, disabled)
          //     : null;

          var appBarView = childrenViews.controlViews.firstWhereOrNull(
              (v) => v.control.id == (appBarCtrls.firstOrNull?.id ?? ""));

          var drawerView = childrenViews.controlViews.firstWhereOrNull(
              (v) => v.control.id == (drawerCtrls.firstOrNull?.id ?? ""));
          var endDrawerView = childrenViews.controlViews.firstWhereOrNull(
              (v) => v.control.id == (endDrawerCtrls.firstOrNull?.id ?? ""));

          var bar = appBarView != null
              ? appBarView.control.type == "appbar"
                  ? AppBarControl(
                      parent: widget.control,
                      control: appBarView.control,
                      children: appBarView.children,
                      parentDisabled: widget.control.isDisabled,
                      height: appBarView.control
                          .attrDouble("toolbarHeight", kToolbarHeight)!)
                  : appBarView.control.type == "cupertinoappbar"
                      ? CupertinoAppBarControl(
                          parent: widget.control,
                          control: appBarView.control,
                          children: appBarView.children,
                          parentDisabled: widget.control.isDisabled,
                          bgcolor: HexColor.fromString(Theme.of(context),
                              appBarView.control.attrString("bgcolor", "")!),
                        ) as ObstructingPreferredSizeWidget
                      : null
              : null;
          return constrainedControl(
              context,
              Scaffold(
                appBar: bar,
                backgroundColor: bgcolor,
                //backgroundColor: Colors.red,
                body: contentCtrls.isNotEmpty
                    ? createControl(
                        widget.control, contentCtrls.first.id, disabled)
                    : null,
                bottomNavigationBar: bnb,
                bottomSheet: bottomSheetCtrls.isNotEmpty
                    ? createControl(
                        widget.control, bottomSheetCtrls.first.id, disabled)
                    : null,
              ),
              widget.parent,
              widget.control);
        });
  }
}
