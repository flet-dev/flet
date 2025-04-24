import 'package:flet/src/utils/buttons.dart';
import 'package:flet/src/utils/colors.dart';
import 'package:flet/src/utils/numbers.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../models/page_design.dart';
import '../utils/platform.dart';
import '../widgets/error.dart';
import 'app_bar.dart';
import 'base_controls.dart';
import 'cupertino_app_bar.dart';
import 'navigation_drawer.dart';

class PageletControl extends StatefulWidget {
  final Control control;

  const PageletControl({super.key, required this.control});

  @override
  State<PageletControl> createState() => _PageletControlState();
}

class _PageletControlState extends State<PageletControl> {
  final scaffoldKey = GlobalKey<ScaffoldState>();

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
    var fab = widget.control.buildWidget("floating_action_button");

    if (content == null) {
      return const ErrorControl("Pagelet.content must be provided and visible");
    }

    var widgetsDesign = widget.control.adaptive == true && isApplePlatform()
        ? PageDesign.cupertino
        : PageDesign.material;

    var bnb = navigationBar ?? bottomAppBar;

    final bool? drawerOpened = widget.control.getBool("drawer_opened");
    final bool? endDrawerOpened = widget.control.getBool("end_drawer_opened");
    final fabLocation = widget.control.getFloatingActionButtonLocation(
        "floating_action_button_location",
        FloatingActionButtonLocation.endFloat);

    void dismissDrawer(dynamic id) {
      // fixme: id
      widget.control.updateProperties({"open": false});
      widget.control.triggerEvent("dismiss");
    }

    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (drawer != null) {
        if (scaffoldKey.currentState?.isDrawerOpen == false &&
            drawerOpened == true) {
          widget.control
              .updateProperties({"drawer_opened": false}, python: false);
          dismissDrawer(drawer.id);
        }
        if (drawer.getBool("open", false)! && drawerOpened != true) {
          if (scaffoldKey.currentState?.isEndDrawerOpen == true) {
            scaffoldKey.currentState?.closeEndDrawer();
          }
          Future.delayed(const Duration(milliseconds: 1)).then((value) {
            scaffoldKey.currentState?.openDrawer();
            widget.control
                .updateProperties({"drawer_opened": true}, python: false);
          });
        } else if (!drawer.getBool("open", false)! && drawerOpened == true) {
          scaffoldKey.currentState?.closeDrawer();
          widget.control
              .updateProperties({"drawer_opened": false}, python: false);
        }
      }
      if (endDrawer != null) {
        if (scaffoldKey.currentState?.isEndDrawerOpen == false &&
            endDrawerOpened == true) {
          widget.control
              .updateProperties({"end_drawer_opened": false}, python: false);
          dismissDrawer(endDrawer.id);
        }
        if (endDrawer.getBool("open", false)! && endDrawerOpened != true) {
          if (scaffoldKey.currentState?.isDrawerOpen == true) {
            scaffoldKey.currentState?.closeDrawer();
          }
          Future.delayed(const Duration(milliseconds: 1)).then((value) {
            scaffoldKey.currentState?.openEndDrawer();
            widget.control
                .updateProperties({"end_drawer_opened": true}, python: false);
          });
        } else if (!endDrawer.getBool("open", false)! &&
            endDrawerOpened == true) {
          scaffoldKey.currentState?.closeEndDrawer();
          widget.control
              .updateProperties({"end_drawer_opened": false}, python: false);
        }
      }
    });

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
        drawer:
            drawer != null ? NavigationDrawerControl(control: drawer) : null,
        onDrawerChanged: (opened) {
          if (drawer != null && !opened) {
            widget.control
                .updateProperties({"drawer_opened": false}, python: false);
            dismissDrawer(drawer.id);
          }
        },
        endDrawer: endDrawer != null
            ? NavigationDrawerControl(control: endDrawer)
            : null,
        onEndDrawerChanged: (opened) {
          if (endDrawer != null && !opened) {
            widget.control
                .updateProperties({"end_drawer_opened": false}, python: false);
            dismissDrawer(endDrawer.id);
          }
        },
        body: content,
        bottomNavigationBar: bnb,
        bottomSheet: bottomSheet,
        floatingActionButton: fab,
        floatingActionButtonLocation: fabLocation);

    if (bar is CupertinoAppBarControl) {
      scaffold = CupertinoPageScaffold(
          key: scaffoldKey,
          backgroundColor: widget.control.getColor("bgcolor", context),
          navigationBar: bar as ObstructingPreferredSizeWidget,
          child: scaffold);
    }

    return ConstrainedControl(control: widget.control, child: scaffold);
  }
}
