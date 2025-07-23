import 'dart:async';

import 'package:collection/collection.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';

import '../controls/control_widget.dart';
import '../extensions/control.dart';
import '../flet_backend.dart';
import '../models/control.dart';
import '../models/page_design.dart';
import '../utils/alignment.dart';
import '../utils/box.dart';
import '../utils/buttons.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/numbers.dart';
import '../utils/platform.dart';
import '../utils/theme.dart';
import '../widgets/loading_page.dart';
import '../widgets/page_context.dart';
import '../widgets/page_media.dart';
import '../widgets/scaffold_key_provider.dart';
import 'app_bar.dart';
import 'cupertino_app_bar.dart';
import 'scroll_notification_control.dart';
import 'scrollable_control.dart';

class ViewControl extends StatefulWidget {
  final Control control;

  ViewControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<ViewControl> createState() => _ViewControlState();
}

class _ViewControlState extends State<ViewControl> {
  final _scaffoldKey = GlobalKey<ScaffoldState>();
  Control? _overlay;
  Control? _dialogs;
  Completer<bool>? _popCompleter;

  @override
  void initState() {
    debugPrint("View.initState: ${widget.control.id}");
    super.initState();
    _overlay = widget.control.parent?.child("_overlay");
    _overlay?.addListener(_overlayOrDialogsChanged);
    _dialogs = widget.control.parent?.child("_dialogs");
    _dialogs?.addListener(_overlayOrDialogsChanged);
    widget.control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void didUpdateWidget(covariant ViewControl oldWidget) {
    debugPrint("View.didUpdateWidget: ${widget.control.id}");
    super.didUpdateWidget(oldWidget);
  }

  @override
  void dispose() {
    debugPrint("View.dispose: ${widget.control.id}");
    _overlay?.removeListener(_overlayOrDialogsChanged);
    widget.control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("View.$name($args)");
    switch (name) {
      case "confirm_pop":
        if (_popCompleter != null && !_popCompleter!.isCompleted) {
          _popCompleter?.complete(args["should_pop"]);
        }
      default:
        throw Exception("Unknown View method: $name");
    }
  }

  void _overlayOrDialogsChanged() {
    setState(() {});
  }

  Future<void> _dismissDrawer(Control drawer, FletBackend backend) async {
    await Future.delayed(const Duration(milliseconds: 250));
    backend.updateControl(drawer.id, {"open": false});
    backend.triggerControlEvent(drawer, "dismiss");
  }

  void _openDrawers(Control? drawer, Control? endDrawer) {
    if (drawer != null &&
        drawer.getBool("open", false) == true &&
        _scaffoldKey.currentState?.isDrawerOpen == false) {
      _scaffoldKey.currentState?.openDrawer();
    } else if (endDrawer != null &&
        endDrawer.getBool("open", false) == true &&
        _scaffoldKey.currentState?.isEndDrawerOpen == false) {
      _scaffoldKey.currentState?.openEndDrawer();
    }
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("View.build: ${widget.control.id}");

    var control = widget.control;

    final mainAlignment = parseMainAxisAlignment(
        control.getString("vertical_alignment"), MainAxisAlignment.start)!;
    final crossAlignment = parseCrossAxisAlignment(
        control.getString("horizontal_alignment"), CrossAxisAlignment.start)!;

    final textDirection = control.parent!.getBool("rtl", false)!
        ? TextDirection.rtl
        : TextDirection.ltr;

    var column = Column(
        mainAxisAlignment: mainAlignment,
        crossAxisAlignment: crossAlignment,
        spacing: control.getDouble("spacing", 10)!,
        children: control
            .children("controls")
            .where((c) => c.visible)
            .map((child) =>
                ControlWidget(control: child, key: ValueKey(child.id)))
            .toList());

    Widget child = ScrollableControl(
        control: control, scrollDirection: Axis.vertical, child: column);

    if (control.getBool("on_scroll", false)!) {
      child = ScrollNotificationControl(control: control, child: child);
    }

    var pageData = PageContext.of(context);

    Control? appBar = control.child("appbar");
    Widget? appBarWidget;
    if (appBar != null) {
      appBar.notifyParent = true;
      appBarWidget = pageData?.widgetsDesign == PageDesign.cupertino ||
              appBar.type == "CupertinoAppBar"
          ? CupertinoAppBarControl(control: appBar)
              as ObstructingPreferredSizeWidget
          : AppBarControl(control: appBar);
    }

    List<Widget> overlayWidgets = [];
    var pageViews = control.parent!.children("views");
    var overlayControls = _overlay?.children("controls");
    var dialogControls = _dialogs?.children("controls");

    Control? drawer = dialogControls?.firstWhereOrNull(
        (c) => c.type == "NavigationDrawer" && c.get("position") != "end");
    Control? endDrawer = dialogControls?.firstWhereOrNull(
        (c) => c.type == "NavigationDrawer" && c.get("position") == "end");

    var isRootView = control.id == pageViews.first.id;

    if (overlayControls != null && dialogControls != null) {
      if (control.id == pageViews.last.id) {
        overlayWidgets
            .addAll(overlayControls.map((c) => ControlWidget(control: c)));
        overlayWidgets.addAll(dialogControls
            .where((dialog) => dialog.type != "NavigationDrawer")
            .map((c) => ControlWidget(control: c)));
        overlayWidgets.add(const PageMedia());
      }

      var windowControl = control.parent?.get("window");
      if (windowControl != null && isRootView && isDesktopPlatform()) {
        overlayWidgets.add(ControlWidget(control: windowControl));
      }
    }

    WidgetsBinding.instance.addPostFrameCallback((_) {
      _openDrawers(drawer, endDrawer);
    });

    Widget body = Stack(children: [
      SizedBox.expand(
          child: Container(
              padding: parsePadding(
                  control.get("padding"), const EdgeInsets.all(10))!,
              child: child)),
      ...overlayWidgets
    ]);

    var materialTheme = pageData?.themeMode == ThemeMode.light ||
            ((pageData?.themeMode == null ||
                    pageData?.themeMode == ThemeMode.system) &&
                pageData?.brightness == Brightness.light)
        ? parseTheme(control.parent!.get("theme"), context, Brightness.light)
        : control.parent!.getString("dark_theme") != null
            ? parseTheme(
                control.parent!.get("dark_theme"), context, Brightness.dark)
            : parseTheme(
                control.parent!.get("theme"), context, Brightness.dark);

    Widget scaffold = ScaffoldKeyProvider(
      scaffoldKey: _scaffoldKey,
      child: Scaffold(
        key: appBarWidget == null || appBarWidget is AppBarControl
            ? _scaffoldKey
            : null,
        backgroundColor: control.getColor("bgcolor", context) ??
            ((pageData?.widgetsDesign == PageDesign.cupertino)
                ? CupertinoTheme.of(context).scaffoldBackgroundColor
                : Theme.of(context).scaffoldBackgroundColor),
        appBar: appBarWidget is AppBarControl ? appBarWidget : null,
        drawer: drawer != null ? ControlWidget(control: drawer) : null,
        onDrawerChanged: (opened) {
          if (!opened) {
            _dismissDrawer(drawer!, FletBackend.of(context));
          }
        },
        endDrawer: endDrawer != null ? ControlWidget(control: endDrawer) : null,
        onEndDrawerChanged: (opened) {
          if (!opened) {
            _dismissDrawer(endDrawer!, FletBackend.of(context));
          }
        },
        body: body,
        bottomNavigationBar: control.buildWidget("navigation_bar") ??
            control.buildWidget("bottom_appbar"),
        floatingActionButton: control.buildWidget("floating_action_button"),
        floatingActionButtonLocation: control.getFloatingActionButtonLocation(
            "floating_action_button_location",
            FloatingActionButtonLocation.endFloat),
      ),
    );

    var systemOverlayStyle =
        materialTheme.extension<SystemUiOverlayStyleTheme>();

    if (systemOverlayStyle != null &&
        systemOverlayStyle.systemUiOverlayStyle != null &&
        appBarWidget == null) {
      scaffold = AnnotatedRegion<SystemUiOverlayStyle>(
        value: systemOverlayStyle.systemUiOverlayStyle!,
        child: scaffold,
      );
    }

    if (appBarWidget is CupertinoAppBarControl) {
      scaffold = CupertinoPageScaffold(
          key: _scaffoldKey,
          backgroundColor: control.getColor("bgcolor", context),
          navigationBar: appBarWidget,
          child: scaffold);
    }

    if (pageData?.widgetsDesign == PageDesign.material) {
      scaffold = CupertinoTheme(
        data: pageData?.themeMode == ThemeMode.light ||
                ((pageData?.themeMode == null ||
                        pageData?.themeMode == ThemeMode.system) &&
                    pageData?.brightness == Brightness.light)
            ? parseCupertinoTheme(
                control.parent!.get("theme"), context, Brightness.light)
            : control.parent!.getString("dark_theme") != null
                ? parseCupertinoTheme(
                    control.parent!.get("dark_theme"), context, Brightness.dark)
                : parseCupertinoTheme(
                    control.parent!.get("theme"), context, Brightness.dark),
        child: scaffold,
      );
    } else if (pageData?.widgetsDesign == PageDesign.cupertino) {
      scaffold = Theme(
        data: materialTheme,
        child: scaffold,
      );
    }

    var showAppStartupScreen =
        FletBackend.of(context).showAppStartupScreen ?? false;
    var appStartupScreenMessage =
        FletBackend.of(context).appStartupScreenMessage ?? "";

    var appStatus =
        context.select<FletBackend, ({bool isLoading, String error})>(
            (backend) => (isLoading: backend.isLoading, error: backend.error));

    Widget? loadingPage;
    if ((appStatus.isLoading || appStatus.error != "") &&
        showAppStartupScreen) {
      loadingPage = LoadingPage(
        isLoading: appStatus.isLoading,
        message:
            appStatus.isLoading ? appStartupScreenMessage : appStatus.error,
      );
    }

    Widget result = Directionality(
        textDirection: textDirection,
        child: loadingPage != null
            ? Stack(
                children: [scaffold, loadingPage],
              )
            : scaffold);

    var backgroundDecoration = control.getBoxDecoration("decoration", context);
    var foregroundDecoration =
        control.getBoxDecoration("foreground_decoration", context);
    if (backgroundDecoration != null || foregroundDecoration != null) {
      result = Container(
        decoration: backgroundDecoration,
        foregroundDecoration: foregroundDecoration,
        child: result,
      );
    }

    result = PopScope(
        canPop: control.getBool("can_pop", true)!,
        onPopInvokedWithResult: (didPop, result) {
          if (didPop || !control.getBool("on_confirm_pop", false)!) {
            return;
          }
          debugPrint("Page.onPopInvokedWithResult()");
          if (_popCompleter != null && !_popCompleter!.isCompleted) {
            _popCompleter!.completeError("Aborted");
          }
          _popCompleter = Completer<bool>();
          control.triggerEvent("confirm_pop");
          _popCompleter!.future
              .timeout(
            const Duration(minutes: 5),
            onTimeout: () => false,
          )
              .then((shouldPop) {
            if (context.mounted && shouldPop) {
              if (isRootView) {
                SystemNavigator.pop();
              } else {
                Navigator.pop(context);
              }
            }
          }).onError((e, st) {/* do nothing */});
        },
        child: result);
    return result;
  }
}
