import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_redux/flutter_redux.dart';
import 'package:redux/redux.dart';

import '../actions.dart';
import '../flet_app_context.dart';
import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/control_view_model.dart';
import '../models/page_media_view_model.dart';
import '../routing/route_parser.dart';
import '../routing/route_state.dart';
import '../routing/router_delegate.dart';
import '../utils/alignment.dart';
import '../utils/colors.dart';
import '../utils/desktop.dart';
import '../utils/edge_insets.dart';
import '../utils/images.dart';
import '../utils/theme.dart';
import '../utils/user_fonts.dart';
import '../widgets/animated_transition_page.dart';
import '../widgets/loading_page.dart';
import '../widgets/page_media.dart';
import '../widgets/window_media.dart';
import 'app_bar.dart';
import 'create_control.dart';
import 'cupertino_app_bar.dart';
import 'flet_control_state.dart';
import 'floating_action_button.dart';
import 'navigation_drawer.dart';
import 'scroll_notification_control.dart';
import 'scrollable_control.dart';

class RoutesViewModel extends Equatable {
  final Control page;
  final bool isLoading;
  final String error;
  final List<Control> offstageControls;
  final List<Control> views;

  const RoutesViewModel(
      {required this.page,
      required this.isLoading,
      required this.error,
      required this.offstageControls,
      required this.views});

  static RoutesViewModel fromStore(Store<AppState> store) {
    Control? offstageControl = store.state.controls["page"]!.childIds
        .map((childId) => store.state.controls[childId]!)
        .firstWhereOrNull((c) => c.type == "offstage");

    return RoutesViewModel(
        page: store.state.controls["page"]!,
        isLoading: store.state.isLoading,
        error: store.state.error,
        offstageControls: offstageControl != null
            ? store.state.controls[offstageControl.id]!.childIds
                .map((childId) => store.state.controls[childId]!)
                .where((c) => c.isVisible)
                .toList()
            : [],
        views: store.state.controls["page"]!.childIds
            .map((childId) => store.state.controls[childId]!)
            .where((c) => c.type != "offstage" && c.isVisible)
            .toList());
  }

  @override
  List<Object?> get props => [page, isLoading, error, offstageControls, views];
}

class KeyboardEvent {
  final String key;
  final bool isShiftPressed;
  final bool isControlPressed;
  final bool isAltPressed;
  final bool isMetaPressed;

  KeyboardEvent(
      {required this.key,
      required this.isShiftPressed,
      required this.isControlPressed,
      required this.isAltPressed,
      required this.isMetaPressed});

  Map<String, dynamic> toJson() => <String, dynamic>{
        'key': key,
        'shift': isShiftPressed,
        'ctrl': isControlPressed,
        'alt': isAltPressed,
        'meta': isMetaPressed
      };
}

class PageControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final dynamic dispatch;

  const PageControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.dispatch});

  @override
  State<PageControl> createState() => _PageControlState();
}

class _PageControlState extends FletControlState<PageControl> {
  String? _windowTitle;
  Color? _windowBgcolor;
  double? _windowWidth;
  double? _windowHeight;
  double? _windowMinWidth;
  double? _windowMinHeight;
  double? _windowMaxWidth;
  double? _windowMaxHeight;
  double? _windowTop;
  double? _windowLeft;
  double? _windowOpacity;
  bool? _windowMinimizable;
  bool? _windowMaximizable;
  bool? _windowFullScreen;
  bool? _windowMovable;
  bool? _windowResizable;
  bool? _windowAlwaysOnTop;
  bool? _windowPreventClose;
  bool? _windowMinimized;
  bool? _windowMaximized;
  bool? _windowVisible;
  bool? _windowFocused;
  String? _windowCenter;
  String? _windowClose;
  bool? _windowFrameless;
  bool? _windowTitleBarHidden;
  bool? _windowSkipTaskBar;
  double? _windowProgressBar;
  final _navigatorKey = GlobalKey<NavigatorState>();
  late final RouteState _routeState;
  late final SimpleRouterDelegate _routerDelegate;
  late final RouteParser _routeParser;
  String? _prevViewRoutes;
  bool _keyboardHandlerSubscribed = false;

  @override
  void initState() {
    super.initState();
    _routeParser = RouteParser();

    _routeState = RouteState(_routeParser);
    _routeState.addListener(_routeChanged);

    _routerDelegate = SimpleRouterDelegate(
      routeState: _routeState,
      navigatorKey: _navigatorKey,
      builder: (context) => _buildNavigator(context, _navigatorKey),
    );
  }

  @override
  void dispose() {
    _routeState.removeListener(_routeChanged);
    _routeState.dispose();
    if (_keyboardHandlerSubscribed) {
      RawKeyboard.instance.removeListener(_handleKeyDown);
    }
    super.dispose();
  }

  void _routeChanged() {
    widget.dispatch(SetPageRouteAction(
        _routeState.route, FletAppServices.of(context).server));
  }

  void _handleKeyDown(RawKeyEvent e) {
    if (e is RawKeyDownEvent) {
      final k = e.logicalKey;
      if (![
        LogicalKeyboardKey.control,
        LogicalKeyboardKey.controlLeft,
        LogicalKeyboardKey.controlRight,
        LogicalKeyboardKey.alt,
        LogicalKeyboardKey.altLeft,
        LogicalKeyboardKey.altRight,
        LogicalKeyboardKey.meta,
        LogicalKeyboardKey.metaLeft,
        LogicalKeyboardKey.metaRight,
        LogicalKeyboardKey.shift,
        LogicalKeyboardKey.shiftLeft,
        LogicalKeyboardKey.shiftRight
      ].contains(k)) {
        sendControlEvent(
            "page",
            "keyboard_event",
            json.encode(KeyboardEvent(
                    key: k.keyLabel,
                    isAltPressed: e.isAltPressed,
                    isControlPressed: e.isControlPressed,
                    isShiftPressed: e.isShiftPressed,
                    isMetaPressed: e.isMetaPressed)
                .toJson()));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Page build: ${widget.control.id}");

    //debugDumpRenderTree();

    // clear hrefs index
    FletAppServices.of(context).globalKeys.clear();

    // page route
    var route = widget.control.attrString("route");
    if (_routeState.route != route && route != null) {
      // route updated
      _routeState.route = route;
    }

    // theme
    var theme = parseTheme(widget.control, "theme", Brightness.light);
    var darkTheme = widget.control.attrString("darkTheme") == null
        ? parseTheme(widget.control, "theme", Brightness.dark)
        : parseTheme(widget.control, "darkTheme", Brightness.dark);
    var themeMode = ThemeMode.values.firstWhereOrNull((t) =>
            t.name.toLowerCase() ==
            widget.control.attrString("themeMode", "")!.toLowerCase()) ??
        FletAppContext.of(context)?.themeMode;

    debugPrint("Page theme: $themeMode");

    // keyboard handler
    var onKeyboardEvent = widget.control.attrBool("onKeyboardEvent", false)!;
    if (onKeyboardEvent && !_keyboardHandlerSubscribed) {
      RawKeyboard.instance.addListener(_handleKeyDown);
      _keyboardHandlerSubscribed = true;
    }

    // window params
    var windowTitle = widget.control.attrString("title", "")!;
    var windowBgcolor = HexColor.fromString(
        Theme.of(context), widget.control.attrString("windowBgcolor", "")!);
    var windowWidth = widget.control.attrDouble("windowWidth");
    var windowHeight = widget.control.attrDouble("windowHeight");
    var windowMinWidth = widget.control.attrDouble("windowMinWidth");
    var windowMinHeight = widget.control.attrDouble("windowMinHeight");
    var windowMaxWidth = widget.control.attrDouble("windowMaxWidth");
    var windowMaxHeight = widget.control.attrDouble("windowMaxHeight");
    var windowTop = widget.control.attrDouble("windowTop");
    var windowLeft = widget.control.attrDouble("windowLeft");
    var windowCenter = widget.control.attrString("windowCenter");
    var windowClose = widget.control.attrString("windowClose");
    var windowFullScreen = widget.control.attrBool("windowFullScreen");
    var windowMinimized = widget.control.attrBool("windowMinimized");
    var windowMaximized = widget.control.attrBool("windowMaximized");
    var windowOpacity = widget.control.attrDouble("windowOpacity");
    var windowMinimizable = widget.control.attrBool("windowMinimizable");
    var windowMaximizable = widget.control.attrBool("windowMaximizable");
    var windowAlwaysOnTop = widget.control.attrBool("windowAlwaysOnTop");
    var windowResizable = widget.control.attrBool("windowResizable");
    var windowMovable = widget.control.attrBool("windowMovable");
    var windowPreventClose = widget.control.attrBool("windowPreventClose");
    var windowTitleBarHidden = widget.control.attrBool("windowTitleBarHidden");
    var windowTitleBarButtonsHidden =
        widget.control.attrBool("windowTitleBarButtonsHidden", false)!;
    var windowVisible = widget.control.attrBool("windowVisible");
    var windowFocused = widget.control.attrBool("windowFocused");
    var windowDestroy = widget.control.attrBool("windowDestroy");
    var windowSkipTaskBar = widget.control.attrBool("windowSkipTaskBar");
    var windowFrameless = widget.control.attrBool("windowFrameless");
    var windowProgressBar = widget.control.attrDouble("windowProgressBar");

    updateWindow() async {
      // window title
      if (_windowTitle != windowTitle) {
        setWindowTitle(windowTitle);
        _windowTitle = windowTitle;
      }

      // window bgcolor
      if (_windowBgcolor != windowBgcolor && windowBgcolor != null) {
        setWindowBackgroundColor(windowBgcolor);
        _windowBgcolor = windowBgcolor;
      }

      // window size
      if ((windowWidth != null || windowHeight != null) &&
          (windowWidth != _windowWidth || windowHeight != _windowHeight) &&
          windowFullScreen != true &&
          (defaultTargetPlatform != TargetPlatform.macOS ||
              (defaultTargetPlatform == TargetPlatform.macOS &&
                  windowMaximized != true &&
                  windowMinimized != true))) {
        debugPrint("setWindowSize: $windowWidth, $windowHeight");
        await setWindowSize(windowWidth, windowHeight);
        _windowWidth = windowWidth;
        _windowHeight = windowHeight;
      }

      // window min size
      if ((windowMinWidth != null || windowMinHeight != null) &&
          (windowMinWidth != _windowMinWidth ||
              windowMinHeight != _windowMinHeight)) {
        debugPrint("setWindowMinSize: $windowMinWidth, $windowMinHeight");
        await setWindowMinSize(windowMinWidth, windowMinHeight);
        _windowMinWidth = windowMinWidth;
        _windowMinHeight = windowMinHeight;
      }

      // window max size
      if ((windowMaxWidth != null || windowMaxHeight != null) &&
          (windowMaxWidth != _windowMaxWidth ||
              windowMaxHeight != _windowMaxHeight)) {
        debugPrint("setWindowMaxSize: $windowMaxWidth, $windowMaxHeight");
        await setWindowMaxSize(windowMaxWidth, windowMaxHeight);
        _windowMaxWidth = windowMaxWidth;
        _windowMaxHeight = windowMaxHeight;
      }

      // window position
      if ((windowTop != null || windowLeft != null) &&
          (windowTop != _windowTop || windowLeft != _windowLeft) &&
          windowFullScreen != true &&
          (windowCenter == null || windowCenter == "") &&
          (defaultTargetPlatform != TargetPlatform.macOS ||
              (defaultTargetPlatform == TargetPlatform.macOS &&
                  windowMaximized != true &&
                  windowMinimized != true))) {
        debugPrint("setWindowPosition: $windowTop, $windowLeft");
        await setWindowPosition(windowTop, windowLeft);
        _windowTop = windowTop;
        _windowLeft = windowLeft;
      }

      // window opacity
      if (windowOpacity != null && windowOpacity != _windowOpacity) {
        await setWindowOpacity(windowOpacity);
        _windowOpacity = windowOpacity;
      }

      // window minimizable
      if (windowMinimizable != null &&
          windowMinimizable != _windowMinimizable) {
        await setWindowMinimizability(windowMinimizable);
        _windowMinimizable = windowMinimizable;
      }

      // window minimize
      if (windowMinimized != _windowMinimized) {
        if (windowMinimized == true) {
          await minimizeWindow();
        } else if (windowMinimized == false && windowMaximized == false) {
          await restoreWindow();
        }
        _windowMinimized = windowMinimized;
      }

      // window maximizable
      if (windowMaximizable != null &&
          windowMaximizable != _windowMaximizable) {
        await setWindowMaximizability(windowMaximizable);
        _windowMaximizable = windowMaximizable;
      }

      // window maximize
      if (windowMaximized != _windowMaximized) {
        if (windowMaximized == true) {
          await maximizeWindow();
        } else if (windowMaximized == false) {
          await unmaximizeWindow();
        }
        _windowMaximized = windowMaximized;
      }

      // window resizable
      if (windowResizable != null && windowResizable != _windowResizable) {
        await setWindowResizability(windowResizable);
        _windowResizable = windowResizable;
      }

      // window movable
      if (windowMovable != null && windowMovable != _windowMovable) {
        await setWindowMovability(windowMovable);
        _windowMovable = windowMovable;
      }

      // window fullScreen
      if (windowFullScreen != null && windowFullScreen != _windowFullScreen) {
        await setWindowFullScreen(windowFullScreen);
        _windowFullScreen = windowFullScreen;
      }

      // window alwaysOnTop
      if (windowAlwaysOnTop != null &&
          windowAlwaysOnTop != _windowAlwaysOnTop) {
        await setWindowAlwaysOnTop(windowAlwaysOnTop);
        _windowAlwaysOnTop = windowAlwaysOnTop;
      }

      // window preventClose
      if (windowPreventClose != null &&
          windowPreventClose != _windowPreventClose) {
        await setWindowPreventClose(windowPreventClose);
        _windowPreventClose = windowPreventClose;
      }

      if (windowTitleBarHidden != null &&
          windowTitleBarHidden != _windowTitleBarHidden) {
        await setWindowTitleBarVisibility(
            windowTitleBarHidden, windowTitleBarButtonsHidden);
        _windowTitleBarHidden = windowTitleBarHidden;
      }

      // window visible
      if (windowVisible != _windowVisible) {
        if (windowVisible == true) {
          await showWindow();
        } else if (windowVisible == false) {
          await hideWindow();
        }
        _windowVisible = windowVisible;
      }

      // window focus
      if (windowFocused != _windowFocused) {
        if (windowFocused == true) {
          await focusWindow();
        } else if (windowFocused == false) {
          await blurWindow();
        }
        _windowFocused = windowFocused;
      }

      // window center
      if (windowCenter != _windowCenter && windowFullScreen != true) {
        await centerWindow();
        _windowCenter = windowCenter;
      }

      // window frameless
      if (windowFrameless != _windowFrameless && windowFrameless == true) {
        await setWindowFrameless();
        _windowFrameless = windowFrameless;
      }

      // window progress
      if (windowProgressBar != null &&
          windowProgressBar != _windowProgressBar) {
        await setWindowProgressBar(windowProgressBar);
        _windowProgressBar = windowProgressBar;
      }

      if (windowSkipTaskBar != null &&
          windowSkipTaskBar != _windowSkipTaskBar) {
        await setWindowSkipTaskBar(windowSkipTaskBar);
        _windowSkipTaskBar = windowSkipTaskBar;
      }

      // window close
      if (windowClose != _windowClose) {
        await closeWindow();
        _windowClose = windowClose;
      }

      // window destroy
      if (windowDestroy == true) {
        await destroyWindow();
      }
    }

    updateWindow();

    return withPageArgs((context, pageArgs) {
      debugPrint("Page fonts build: ${widget.control.id}");

      // load custom fonts
      parseFonts(widget.control, "fonts").forEach((fontFamily, fontUrl) {
        var assetSrc =
            getAssetSrc(fontUrl, pageArgs.pageUri!, pageArgs.assetsDir);

        if (assetSrc.isFile) {
          UserFonts.loadFontFromFile(fontFamily, assetSrc.path);
        } else {
          UserFonts.loadFontFromUrl(fontFamily, assetSrc.path);
        }
      });

      return StoreConnector<AppState, PageMediaViewModel>(
          distinct: true,
          converter: (store) => PageMediaViewModel.fromStore(store),
          builder: (context, media) {
            debugPrint("MaterialApp.router build: ${widget.control.id}");

            return FletAppContext(
                themeMode: themeMode,
                child: MaterialApp.router(
                  debugShowCheckedModeBanner: false,
                  showSemanticsDebugger:
                      widget.control.attrBool("showSemanticsDebugger", false)!,
                  routerDelegate: _routerDelegate,
                  routeInformationParser: _routeParser,
                  title: windowTitle,
                  theme: theme,
                  darkTheme: darkTheme,
                  themeMode: themeMode,
                ));
          });
    });
  }

  Widget _buildNavigator(
      BuildContext context, GlobalKey<NavigatorState> navigatorKey) {
    debugPrint("Page navigator build: ${widget.control.id}");

    return StoreConnector<AppState, RoutesViewModel>(
        distinct: true,
        converter: (store) => RoutesViewModel.fromStore(store),
        // onWillChange: (prev, next) {
        //   debugPrint("Page navigator.onWillChange(): $prev, $next");
        // },
        builder: (context, routesView) {
          debugPrint("_buildNavigator build");

          var hideLoadingPage =
              FletAppServices.of(context).hideLoadingPage ?? false;

          List<Page<dynamic>> pages = [];
          if (routesView.views.isEmpty) {
            pages.add(AnimatedTransitionPage(
                fadeTransition: true,
                duration: Duration.zero,
                child: hideLoadingPage
                    ? const Scaffold(
                        body: PageMedia(),
                      )
                    : Stack(children: [
                        const PageMedia(),
                        LoadingPage(
                          isLoading: routesView.isLoading,
                          message: routesView.error,
                        )
                      ])));
          } else {
            Widget? loadingPage;
            // offstage
            overlayWidgets(String viewId) {
              List<Widget> overlayWidgets = [];

              if (viewId == routesView.views.last.id) {
                overlayWidgets.addAll(routesView.offstageControls
                    .where((c) => !c.isNonVisual)
                    .map((c) => createControl(
                        routesView.page, c.id, routesView.page.isDisabled)));
                overlayWidgets.add(const PageMedia());
              }

              if (viewId == routesView.views.first.id && isDesktop()) {
                overlayWidgets.add(WindowMedia(dispatch: widget.dispatch));
              }

              return overlayWidgets;
            }

            if ((routesView.isLoading || routesView.error != "") &&
                !hideLoadingPage) {
              loadingPage = LoadingPage(
                isLoading: routesView.isLoading,
                message: routesView.error,
              );
            }

            String viewRoutes = routesView.views
                .map((v) => v.attrString("route") ?? v.id)
                .join();

            pages = routesView.views.map((view) {
              var key = ValueKey(view.attrString("route") ?? view.id);
              var child = ViewControl(
                  parent: routesView.page,
                  viewId: view.id,
                  overlayWidgets: overlayWidgets(view.id),
                  loadingPage: loadingPage);

              //debugPrint("ROUTES: $_prevViewRoutes $viewRoutes");

              return _prevViewRoutes == null
                  ? AnimatedTransitionPage(
                      key: key,
                      child: child,
                      fadeTransition: true,
                      duration: Duration.zero,
                    )
                  : AnimatedTransitionPage(
                      key: key,
                      child: child,
                      fullscreenDialog:
                          view.attrBool("fullscreenDialog", false)!);
            }).toList();

            _prevViewRoutes = viewRoutes;
          }

          Widget nextChild = Navigator(
              key: navigatorKey,
              pages: pages,
              onPopPage: (route, dynamic result) {
                sendControlEvent("page", "view_pop",
                    ((route.settings as Page).key as ValueKey).value);
                return false;
              });

          // wrap navigator into non-visual offstage controls
          for (var c
              in routesView.offstageControls.where((c) => c.isNonVisual)) {
            nextChild = createControl(
                routesView.page, c.id, routesView.page.isDisabled,
                nextChild: nextChild);
          }

          return nextChild;
        });
  }
}

class ViewControl extends StatefulWidget {
  final Control parent;
  final String viewId;
  final List<Widget> overlayWidgets;
  final Widget? loadingPage;

  const ViewControl(
      {super.key,
      required this.parent,
      required this.viewId,
      required this.overlayWidgets,
      required this.loadingPage});

  @override
  State<ViewControl> createState() => _ViewControlState();
}

class _ViewControlState extends FletControlState<ViewControl> {
  final scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  Widget build(BuildContext context) {
    return StoreConnector<AppState, ControlViewModel?>(
        distinct: true,
        converter: (store) {
          return ControlViewModel.fromStore(store, widget.viewId);
        },
        ignoreChange: (state) {
          return state.controls[widget.viewId] == null;
        },
        // onWillChange: (prev, next) {
        //   debugPrint("View StoreConnector.onWillChange(): $prev, $next");
        // },
        builder: (context, controlView) {
          debugPrint("View build");

          if (controlView == null) {
            return const SizedBox.shrink();
          }

          var control = controlView.control;
          var children = controlView.children;

          final spacing = control.attrDouble("spacing", 10)!;
          final mainAlignment = parseMainAxisAlignment(
              control, "verticalAlignment", MainAxisAlignment.start);
          final crossAlignment = parseCrossAxisAlignment(
              control, "horizontalAlignment", CrossAxisAlignment.start);
          final fabLocation = parseFloatingActionButtonLocation(
              control,
              "floatingActionButtonLocation",
              FloatingActionButtonLocation.endFloat);

          Control? appBar;
          Control? cupertinoAppBar;
          Control? bottomAppBar;
          Control? fab;
          Control? navBar;
          Control? drawer;
          Control? endDrawer;
          List<Widget> controls = [];
          bool firstControl = true;

          for (var ctrl in children.where((c) => c.isVisible)) {
            if (ctrl.type == "appbar") {
              appBar = ctrl;
              continue;
            } else if (ctrl.type == "cupertinoappbar") {
              cupertinoAppBar = ctrl;
              continue;
            } else if (ctrl.type == "bottomappbar") {
              bottomAppBar = ctrl;
              continue;
            } else if (ctrl.type == "floatingactionbutton") {
              fab = ctrl;
              continue;
            } else if (ctrl.type == "navigationbar" ||
                ctrl.type == "cupertinonavigationbar") {
              navBar = ctrl;
              continue;
            } else if (ctrl.type == "navigationdrawer" &&
                ctrl.name == "start") {
              drawer = ctrl;
              continue;
            } else if (ctrl.type == "navigationdrawer" && ctrl.name == "end") {
              endDrawer = ctrl;
              continue;
            }
            // spacer between displayed controls
            else if (spacing > 0 &&
                !firstControl &&
                mainAlignment != MainAxisAlignment.spaceAround &&
                mainAlignment != MainAxisAlignment.spaceBetween &&
                mainAlignment != MainAxisAlignment.spaceEvenly) {
              controls.add(SizedBox(height: spacing));
            }
            firstControl = false;

            // displayed control
            controls.add(createControl(control, ctrl.id, control.isDisabled));
          }

          List<String> childIds = [
            appBar?.id,
            cupertinoAppBar?.id,
            drawer?.id,
            endDrawer?.id
          ].whereNotNull().toList();

          final textDirection = widget.parent.attrBool("rtl", false)!
              ? TextDirection.rtl
              : TextDirection.ltr;

          return withControls(childIds, (context, childrenViews) {
            debugPrint("Route view build: ${widget.viewId}");

            var appBarView = childrenViews.controlViews
                .firstWhereOrNull((v) => v.control.id == (appBar?.id ?? ""));
            var cupertinoAppBarView = childrenViews.controlViews
                .firstWhereOrNull(
                    (v) => v.control.id == (cupertinoAppBar?.id ?? ""));
            var drawerView = childrenViews.controlViews
                .firstWhereOrNull((v) => v.control.id == (drawer?.id ?? ""));
            var endDrawerView = childrenViews.controlViews
                .firstWhereOrNull((v) => v.control.id == (endDrawer?.id ?? ""));

            var column = Column(
                mainAxisAlignment: mainAlignment,
                crossAxisAlignment: crossAlignment,
                children: controls);

            Widget child = ScrollableControl(
              control: control,
              scrollDirection: Axis.vertical,
              child: column,
            );

            if (control.attrBool("onScroll", false)!) {
              child = ScrollNotificationControl(control: control, child: child);
            }

            final bool? drawerOpened = widget.parent.state["drawerOpened"];
            final bool? endDrawerOpened =
                widget.parent.state["endDrawerOpened"];

            void dismissDrawer(String id) {
              updateControlProps(id, {"open": "false"});
              sendControlEvent(id, "dismiss", "");
            }

            WidgetsBinding.instance.addPostFrameCallback((_) {
              if (drawerView != null) {
                if (scaffoldKey.currentState?.isDrawerOpen == false &&
                    drawerOpened == true) {
                  widget.parent.state["drawerOpened"] = false;
                  dismissDrawer(drawerView.control.id);
                }
                if (drawerView.control.attrBool("open", false)! &&
                    drawerOpened != true) {
                  if (scaffoldKey.currentState?.isEndDrawerOpen == true) {
                    scaffoldKey.currentState?.closeEndDrawer();
                  }
                  Future.delayed(const Duration(milliseconds: 1)).then((value) {
                    scaffoldKey.currentState?.openDrawer();
                    widget.parent.state["drawerOpened"] = true;
                  });
                } else if (!drawerView.control.attrBool("open", false)! &&
                    drawerOpened == true) {
                  scaffoldKey.currentState?.closeDrawer();
                  widget.parent.state["drawerOpened"] = false;
                }
              }
              if (endDrawerView != null) {
                if (scaffoldKey.currentState?.isEndDrawerOpen == false &&
                    endDrawerOpened == true) {
                  widget.parent.state["endDrawerOpened"] = false;
                  dismissDrawer(endDrawerView.control.id);
                }
                if (endDrawerView.control.attrBool("open", false)! &&
                    endDrawerOpened != true) {
                  if (scaffoldKey.currentState?.isDrawerOpen == true) {
                    scaffoldKey.currentState?.closeDrawer();
                  }
                  Future.delayed(const Duration(milliseconds: 1)).then((value) {
                    scaffoldKey.currentState?.openEndDrawer();
                    widget.parent.state["endDrawerOpened"] = true;
                  });
                } else if (!endDrawerView.control.attrBool("open", false)! &&
                    endDrawerOpened == true) {
                  scaffoldKey.currentState?.closeEndDrawer();
                  widget.parent.state["endDrawerOpened"] = false;
                }
              }
            });

            var bnb = navBar ?? bottomAppBar;

            var bar = appBarView != null
                ? AppBarControl(
                    parent: control,
                    control: appBarView.control,
                    children: appBarView.children,
                    parentDisabled: control.isDisabled,
                    height: appBarView.control
                        .attrDouble("toolbarHeight", kToolbarHeight)!)
                : cupertinoAppBarView != null
                    ? CupertinoAppBarControl(
                        parent: control,
                        control: cupertinoAppBarView.control,
                        children: cupertinoAppBarView.children,
                        parentDisabled: control.isDisabled,
                        bgcolor: HexColor.fromString(
                            Theme.of(context),
                            cupertinoAppBarView.control
                                .attrString("bgcolor", "")!),
                      ) as ObstructingPreferredSizeWidget
                    : null;

            var scaffold = Scaffold(
              key: scaffoldKey,
              backgroundColor: HexColor.fromString(
                  Theme.of(context), control.attrString("bgcolor", "")!),
              appBar: bar,
              drawer: drawerView != null
                  ? NavigationDrawerControl(
                      control: drawerView.control,
                      children: drawerView.children,
                      parentDisabled: control.isDisabled,
                    )
                  : null,
              onDrawerChanged: (opened) {
                if (drawerView != null && !opened) {
                  widget.parent.state["drawerOpened"] = false;
                  dismissDrawer(drawerView.control.id);
                }
              },
              endDrawer: endDrawerView != null
                  ? NavigationDrawerControl(
                      control: endDrawerView.control,
                      children: endDrawerView.children,
                      parentDisabled: control.isDisabled,
                    )
                  : null,
              onEndDrawerChanged: (opened) {
                if (endDrawerView != null && !opened) {
                  widget.parent.state["endDrawerOpened"] = false;
                  dismissDrawer(endDrawerView.control.id);
                }
              },
              body: Stack(children: [
                SizedBox.expand(
                    child: Container(
                        padding: parseEdgeInsets(control, "padding") ??
                            const EdgeInsets.all(10),
                        child: child)),
                ...widget.overlayWidgets
              ]),
              bottomNavigationBar: bnb != null
                  ? createControl(control, bnb.id, control.isDisabled)
                  : null,
              floatingActionButton: fab != null
                  ? createControl(control, fab.id, control.isDisabled)
                  : null,
              floatingActionButtonLocation: fabLocation,
            );

            return Directionality(
                textDirection: textDirection,
                child: widget.loadingPage != null
                    ? Stack(
                        children: [scaffold, widget.loadingPage!],
                      )
                    : scaffold);
          });
        });
  }
}
