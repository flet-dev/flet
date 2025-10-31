import 'package:flet/src/utils/buttons.dart';
import 'package:flet/src/utils/colors.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../models/page_design.dart';
import '../utils/platform.dart';
import '../widgets/error.dart';
import 'app_bar.dart';
import 'base_controls.dart';
import 'control_widget.dart';
import 'cupertino_app_bar.dart';

class PageletControl extends StatefulWidget {
  final Control control;

  PageletControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<PageletControl> createState() => _PageletControlState();
}

class _PageletControlState extends State<PageletControl> {
  final scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    widget.control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void dispose() {
    widget.control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("Pagelet.$name($args)");
    switch (name) {
      case "show_drawer":
        scaffoldKey.currentState?.openDrawer();
        break;
      case "close_drawer":
        scaffoldKey.currentState?.closeDrawer();
        break;
      case "show_end_drawer":
        scaffoldKey.currentState?.openEndDrawer();
        break;
      case "close_end_drawer":
        scaffoldKey.currentState?.closeEndDrawer();
        break;
      default:
        throw Exception("Unknown Pagelet method: $name");
    }
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Pagelet build: ${widget.control.id}");

    var appBar = widget.control.child("appbar");
    var content = widget.control.buildWidget("content");
    var navigationBar = widget.control.buildWidget("navigation_bar");
    var bottomAppBar = widget.control.buildWidget("bottom_appbar");
    var bottomSheet = widget.control.buildWidget("bottom_sheet");
    var drawer = widget.control.child("drawer");
    var endDrawer = widget.control.child("end_drawer");
    var hasDrawer = drawer != null || endDrawer != null;
    var fab = widget.control.buildWidget("floating_action_button");

    if (content == null) {
      return const ErrorControl("Pagelet.content must be provided and visible");
    }

    var widgetsDesign = widget.control.adaptive == true && isApplePlatform()
        ? PageDesign.cupertino
        : PageDesign.material;

    var bnb = navigationBar ?? bottomAppBar;

    void dismissDrawer(int id) {
      widget.control.backend.triggerControlEventById(id, "dismiss");
    }

    var bar = appBar != null
        ? appBar.type == "AppBar"
            ? widgetsDesign == PageDesign.cupertino
                ? CupertinoAppBarControl(control: appBar)
                : AppBarControl(control: appBar)
            : appBar.type == "CupertinoAppBar"
                ? CupertinoAppBarControl(control: appBar)
                    as ObstructingPreferredSizeWidget
                : null
        : null;

    Widget scaffold = Scaffold(
        key: bar == null || bar is AppBarControl ? scaffoldKey : null,
        backgroundColor: widget.control.getColor("bgcolor", context) ??
            CupertinoTheme.of(context).scaffoldBackgroundColor,
        appBar: bar is AppBarControl ? bar : null,
        drawer: drawer != null ? ControlWidget(control: drawer) : null,
        onDrawerChanged: (opened) {
          if (drawer != null && !opened) {
            dismissDrawer(drawer.id);
          }
        },
        endDrawer: endDrawer != null ? ControlWidget(control: endDrawer) : null,
        onEndDrawerChanged: (opened) {
          if (endDrawer != null && !opened) {
            dismissDrawer(endDrawer.id);
          }
        },
        body: content,
        bottomNavigationBar: bnb,
        bottomSheet: bottomSheet,
        floatingActionButton: fab,
        floatingActionButtonLocation: widget.control
            .getFloatingActionButtonLocation("floating_action_button_location",
                FloatingActionButtonLocation.endFloat));

    if (hasDrawer) {
      // Clip to page bounds so the drawer animation stays hidden outside the pagelet.
      scaffold = ClipRect(child: scaffold);
    }

    if (bar is CupertinoAppBarControl) {
      scaffold = CupertinoPageScaffold(
          key: scaffoldKey,
          backgroundColor: widget.control.getColor("bgcolor", context),
          navigationBar: bar as ObstructingPreferredSizeWidget,
          child: scaffold);
    }

    return LayoutControl(control: widget.control, child: scaffold);
  }
}
