import 'package:collection/collection.dart';
import 'package:flet/src/extensions/control.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../controls/control_widget.dart';
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
import '../widgets/page_control_data.dart';
import '../widgets/page_media.dart';
import '../widgets/scaffold_key_provider.dart';
import 'scroll_notification_control.dart';
import 'scrollable_control.dart';

class ViewControl extends StatefulWidget {
  final Control control;
  const ViewControl({super.key, required this.control});

  @override
  State<ViewControl> createState() => _ViewControlState();
}

class _ViewControlState extends State<ViewControl> {
  final _scaffoldKey = GlobalKey<ScaffoldState>();
  Control? _overlay;
  Control? _dialogs;

  @override
  void initState() {
    debugPrint("View.initState: ${widget.control.id}");
    super.initState();
    _overlay = widget.control.parent?.child("_overlay");
    _overlay?.addListener(_overlayOrDialogsChanged);
    _dialogs = widget.control.parent?.child("_dialogs");
    _dialogs?.addListener(_overlayOrDialogsChanged);
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
    super.dispose();
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

    Control? appbar = control.child("appbar");

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

    // var bnb = control.child("navigation_bar") ?? control.child("bottom_appbar");

    // var bar = appbar != null
    //     ? widget.widgetsDesign == PageDesign.cupertino
    //         ? CupertinoAppBarControl(
    //             parent: control,
    //             control: appBarView.control,
    //             children: appBarView.children,
    //             parentDisabled: control.isDisabled,
    //             parentAdaptive: adaptive)
    //         : AppBarControl(
    //             parent: control,
    //             control: appBarView.control,
    //             children: appBarView.children,
    //             parentDisabled: control.isDisabled,
    //             parentAdaptive: adaptive,
    //             height: appBarView.control
    //                 .attrDouble("toolbar_height", kToolbarHeight)!)
    //     : cupertinoAppBarView != null
    //         ? CupertinoAppBarControl(
    //             parent: control,
    //             control: cupertinoAppBarView.control,
    //             children: cupertinoAppBarView.children,
    //             parentDisabled: control.isDisabled,
    //             parentAdaptive: adaptive,
    //           ) as ObstructingPreferredSizeWidget
    //         : null;

    var pageData = PageControlData.of(context);

    List<Widget> overlayWidgets = [];
    var pageViews = control.parent!.children("views");
    var overlayControls = _overlay?.children("controls");
    var dialogControls = _dialogs?.children("controls");

    Control? drawer = dialogControls?.firstWhereOrNull(
        (c) => c.type == "NavigationDrawer" && c.get("position") != "end");
    Control? endDrawer = dialogControls?.firstWhereOrNull(
        (c) => c.type == "NavigationDrawer" && c.get("position") == "end");

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
      if (windowControl != null &&
          control.id == pageViews.first.id &&
          isDesktopPlatform()) {
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
        key: _scaffoldKey,
        //key: bar == null || bar is AppBarControl ? scaffoldKey : null,
        backgroundColor: control.getColor("bgcolor", context) ??
            ((pageData?.widgetsDesign == PageDesign.cupertino)
                ? CupertinoTheme.of(context).scaffoldBackgroundColor
                : Theme.of(context).scaffoldBackgroundColor),
        //appBar: bar is AppBarControl ? bar : null,
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

    // var systemOverlayStyle =
    //     materialTheme.extension<SystemUiOverlayStyleTheme>();

    // if (systemOverlayStyle != null &&
    //     systemOverlayStyle.systemUiOverlayStyle != null &&
    //     bar == null) {
    //   scaffold = AnnotatedRegion<SystemUiOverlayStyle>(
    //     value: systemOverlayStyle.systemUiOverlayStyle!,
    //     child: scaffold,
    //   );
    // }

    // if (bar is CupertinoAppBarControl) {
    //   scaffold = CupertinoPageScaffold(
    //       key: scaffoldKey,
    //       backgroundColor: control.attrColor("bgcolor", context),
    //       navigationBar: bar as ObstructingPreferredSizeWidget,
    //       child: scaffold);
    // }

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

    var result = Directionality(
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
      return Container(
        decoration: backgroundDecoration,
        foregroundDecoration: foregroundDecoration,
        child: result,
      );
    }
    return result;
  }
}
