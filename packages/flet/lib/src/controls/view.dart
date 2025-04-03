import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../controls/control_widget.dart';
import '../flet_backend.dart';
import '../models/control.dart';
import '../models/page_args_model.dart';
import '../models/page_design.dart';
import '../utils/alignment.dart';
import '../utils/box.dart';
import '../utils/buttons.dart';
import '../utils/edge_insets.dart';
import '../utils/platform.dart';
import '../utils/theme.dart';
import '../widgets/loading_page.dart';
import '../widgets/page_control_data.dart';
import '../widgets/page_media.dart';

class ViewControl extends StatefulWidget {
  final Control control;
  const ViewControl({super.key, required this.control});

  @override
  State<ViewControl> createState() => _ViewControlState();
}

class _ViewControlState extends State<ViewControl> {
  final scaffoldKey = GlobalKey<ScaffoldState>();
  Control? _overlay;
  Control? _dialogs;
  bool? _drawerOpened;
  bool? _endDrawerOpened;

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

  @override
  Widget build(BuildContext context) {
    debugPrint("View.build: ${widget.control.id}");

    var control = widget.control;
    var adaptive = control.adaptive ?? control.parent!.adaptive;

    final mainAlignment = parseMainAxisAlignment(
        control.get<String>("vertical_alignment"), MainAxisAlignment.start)!;
    final crossAlignment = parseCrossAxisAlignment(
        control.get<String>("horizontal_alignment"), CrossAxisAlignment.start)!;
    final fabLocation = parseFloatingActionButtonLocation(
        control,
        "floating_action_button_location",
        FloatingActionButtonLocation.endFloat);

    final textDirection = control.parent!.get<bool>("rtl", false)!
        ? TextDirection.rtl
        : TextDirection.ltr;

    Control? appbar = control.child("appbar");
    Control? drawer = control.child("drawer");
    Control? endDrawer = control.child("end_drawer");

    var column = Column(
        mainAxisAlignment: mainAlignment,
        crossAxisAlignment: crossAlignment,
        spacing: control.get<double>("spacing", 10)!,
        children: control
            .children("controls")
            .where((c) => c.visible)
            .map((child) =>
                ControlWidget(control: child, key: ValueKey(child.id)))
            .toList());

    var child = column;

    // Widget child = ScrollableControl(
    //     control: control, scrollDirection: Axis.vertical, child: column);

    // if (control.get<bool>("on_scroll", false)!) {
    //   child = ScrollNotificationControl(control: control, child: child);
    // }

    // var backend = FletBackend.of(context);
    // void dismissDrawer(int id) {
    //   backend.updateControlState(id, {"open": false});
    //   backend.triggerControlEvent(id, "dismiss");
    // }

    // WidgetsBinding.instance.addPostFrameCallback((_) {
    //   if (drawer != null) {
    //     if (scaffoldKey.currentState?.isDrawerOpen == false &&
    //         _drawerOpened == true) {
    //       _drawerOpened = false;
    //       dismissDrawer(drawer.id);
    //     }
    //     if (drawer.get<bool>("open", false)! && _drawerOpened != true) {
    //       if (scaffoldKey.currentState?.isEndDrawerOpen == true) {
    //         scaffoldKey.currentState?.closeEndDrawer();
    //       }
    //       Future.delayed(const Duration(milliseconds: 1)).then((value) {
    //         scaffoldKey.currentState?.openDrawer();
    //         _drawerOpened = true;
    //       });
    //     } else if (!drawer.get<bool>("open", false)! && _drawerOpened == true) {
    //       scaffoldKey.currentState?.closeDrawer();
    //       _drawerOpened = false;
    //     }
    //   }
    //   if (endDrawer != null) {
    //     if (scaffoldKey.currentState?.isEndDrawerOpen == false &&
    //         _endDrawerOpened == true) {
    //       _endDrawerOpened = false;
    //       dismissDrawer(endDrawer.id);
    //     }
    //     if (endDrawer.get<bool>("open", false)! && _endDrawerOpened != true) {
    //       if (scaffoldKey.currentState?.isDrawerOpen == true) {
    //         scaffoldKey.currentState?.closeDrawer();
    //       }
    //       Future.delayed(const Duration(milliseconds: 1)).then((value) {
    //         scaffoldKey.currentState?.openEndDrawer();
    //         _endDrawerOpened = true;
    //       });
    //     } else if (!endDrawer.get<bool>("open", false)! &&
    //         _endDrawerOpened == true) {
    //       scaffoldKey.currentState?.closeEndDrawer();
    //       _endDrawerOpened = false;
    //     }
    //   }
    // });

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

    if (overlayControls != null && dialogControls != null) {
      if (control.id == pageViews.last.id) {
        overlayWidgets
            .addAll(overlayControls.map((c) => ControlWidget(control: c)));
        overlayWidgets
            .addAll(dialogControls.map((c) => ControlWidget(control: c)));
        overlayWidgets.add(const PageMedia());
      }

      var windowControl = control.parent?.child("window");
      if (windowControl != null &&
          control.id == pageViews.first.id &&
          isDesktopPlatform()) {
        overlayWidgets.add(ControlWidget(control: windowControl));
      }
    }

    Widget body = Stack(children: [
      SizedBox.expand(
          child: Container(
              padding: parseEdgeInsets(
                  control, "padding", const EdgeInsets.all(10))!,
              child: child)),
      ...overlayWidgets
    ]);

    var materialTheme = pageData?.themeMode == ThemeMode.light ||
            ((pageData?.themeMode == null ||
                    pageData?.themeMode == ThemeMode.system) &&
                pageData?.brightness == Brightness.light)
        ? parseTheme(control.parent!, "theme", Brightness.light)
        : control.parent!.get<String>("dark_theme") != null
            ? parseTheme(control.parent!, "dark_theme", Brightness.dark)
            : parseTheme(control.parent!, "theme", Brightness.dark);

    Widget scaffold = Scaffold(
      key: scaffoldKey,
      //key: bar == null || bar is AppBarControl ? scaffoldKey : null,
      backgroundColor: control.getColor("bgcolor", context) ??
          ((pageData?.widgetsDesign == PageDesign.cupertino)
              ? CupertinoTheme.of(context).scaffoldBackgroundColor
              : Theme.of(context).scaffoldBackgroundColor),
      //appBar: bar is AppBarControl ? bar : null,
      // drawer: drawer != null
      //     ? NavigationDrawerControl(
      //         control: drawer.control,
      //         children: drawer.children,
      //         parentDisabled: control.isDisabled,
      //         parentAdaptive: adaptive,
      //         backend: widget.backend)
      //     : null,
      // onDrawerChanged: (opened) {
      //   if (!opened) {
      //     _drawerOpened = false;
      //     dismissDrawer(drawer!.id);
      //   }
      // },
      // endDrawer: endDrawer != null
      //     ? NavigationDrawerControl(
      //         control: endDrawer.control,
      //         children: endDrawer.children,
      //         parentDisabled: control.isDisabled,
      //         parentAdaptive: adaptive,
      //         backend: widget.backend)
      //     : null,
      // onEndDrawerChanged: (opened) {
      //   if (!opened) {
      //     _endDrawerOpened = false;
      //     dismissDrawer(endDrawer!.id);
      //   }
      // },
      body: body,
      // bottomNavigationBar: bnb != null
      //     ? createControl(control, bnb.id, control.isDisabled,
      //         parentAdaptive: adaptive)
      //     : null,
      // floatingActionButton: fab != null
      //     ? createControl(control, fab.id, control.isDisabled,
      //         parentAdaptive: adaptive)
      //     : null,
      floatingActionButtonLocation: fabLocation,
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
            ? parseCupertinoTheme(control.parent!, "theme", Brightness.light)
            : control.parent!.get<String>("dark_theme") != null
                ? parseCupertinoTheme(
                    control.parent!, "dark_theme", Brightness.dark)
                : parseCupertinoTheme(
                    control.parent!, "theme", Brightness.dark),
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

    var pageArgs = PageArgsModel(
        pageUri: FletBackend.of(context).pageUri,
        assetsDir: FletBackend.of(context).assetsDir);
    var backgroundDecoration =
        parseBoxDecoration(Theme.of(context), control, "decoration", pageArgs);
    var foregroundDecoration = parseBoxDecoration(
        Theme.of(context), control, "foreground_decoration", pageArgs);
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
