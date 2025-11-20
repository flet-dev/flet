import 'dart:async';

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
  final _materialScaffoldKey = GlobalKey<ScaffoldState>();
  final _cupertinoPageScaffoldKey = GlobalKey();
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
      case "show_drawer":
        _materialScaffoldKey.currentState?.openDrawer();
        break;
      case "close_drawer":
        _materialScaffoldKey.currentState?.closeDrawer();
        break;
      case "show_end_drawer":
        _materialScaffoldKey.currentState?.openEndDrawer();
        break;
      case "close_end_drawer":
        _materialScaffoldKey.currentState?.closeEndDrawer();
        break;
      case "confirm_pop":
        if (_popCompleter != null && !_popCompleter!.isCompleted) {
          _popCompleter?.complete(args["should_pop"]);
        }
        break;
    }
  }

  void _overlayOrDialogsChanged() {
    setState(() {});
  }

  Future<void> _dismissDrawer(int drawerId) async {
    widget.control.backend.triggerControlEventById(drawerId, "dismiss");
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
      control: control,
      scrollDirection: Axis.vertical,
      wrapIntoScrollableView: true,
      child: column,
    );

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

    var drawer = widget.control.child("drawer");
    var endDrawer = widget.control.child("end_drawer");

    var isRootView = control.id == pageViews.first.id;

    if (overlayControls != null && dialogControls != null) {
      if (control.id == pageViews.last.id) {
        overlayWidgets
            .addAll(overlayControls.map((c) => ControlWidget(control: c)));
        overlayWidgets
            .addAll(dialogControls.map((c) => ControlWidget(control: c)));
        overlayWidgets.add(PageMedia(view: widget.control.parent));
      }

    }

    Widget body = Stack(children: [
      SizedBox.expand(
          child: Container(
              padding: control.getPadding("padding", const EdgeInsets.all(10))!,
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

    Widget scaffold = Scaffold(
      key: _materialScaffoldKey,
      backgroundColor: control.getColor("bgcolor", context) ??
          ((pageData?.widgetsDesign == PageDesign.cupertino)
              ? CupertinoTheme.of(context).scaffoldBackgroundColor
              : Theme.of(context).scaffoldBackgroundColor),
      appBar: appBarWidget is AppBarControl ? appBarWidget : null,
      drawer: drawer != null ? ControlWidget(control: drawer) : null,
      onDrawerChanged: (opened) {
        if (!opened) {
          _dismissDrawer(drawer!.id);
        }
      },
      endDrawer: endDrawer != null ? ControlWidget(control: endDrawer) : null,
      onEndDrawerChanged: (opened) {
        if (!opened) {
          _dismissDrawer(endDrawer!.id);
        }
      },
      body: body,
      bottomNavigationBar: control.buildWidget("navigation_bar") ??
          control.buildWidget("bottom_appbar"),
      floatingActionButton: control.buildWidget("floating_action_button"),
      floatingActionButtonLocation: control.getFloatingActionButtonLocation(
          "floating_action_button_location",
          FloatingActionButtonLocation.endFloat),
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
          key: _cupertinoPageScaffoldKey,
          backgroundColor: control.getColor("bgcolor", context),
          navigationBar: appBarWidget,
          child: scaffold);
    }

    var backend = FletBackend.of(context);
    var showAppStartupScreen = backend.showAppStartupScreen ?? false;
    var appStartupScreenMessage =
        backend.appStartupScreenMessage ?? "";

    var appStatus =
        context.select<FletBackend, ({bool isLoading, String error})>(
            (backend) => (isLoading: backend.isLoading, error: backend.error));
    var formattedErrorMessage =
        backend.formatAppErrorMessage(appStatus.error);

    Widget? loadingPage;
    if ((appStatus.isLoading || appStatus.error != "") &&
        showAppStartupScreen) {
      loadingPage = LoadingPage(
        isLoading: appStatus.isLoading,
        message:
            appStatus.isLoading ? appStartupScreenMessage : formattedErrorMessage,
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
