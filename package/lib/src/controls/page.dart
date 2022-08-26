import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/control_type.dart';
import '../models/control_view_model.dart';
import '../models/controls_view_model.dart';
import '../models/page_media_view_model.dart';
import '../models/routes_view_model.dart';
import '../protocol/keyboard_event_data.dart';
import '../routing/route_parser.dart';
import '../routing/route_state.dart';
import '../routing/router_delegate.dart';
import '../utils/alignment.dart';
import '../utils/colors.dart';
import '../utils/desktop.dart';
import '../utils/edge_insets.dart';
import '../utils/theme.dart';
import '../utils/uri.dart';
import '../utils/user_fonts.dart';
import '../widgets/fade_transition_page.dart';
import '../widgets/loading_page.dart';
import '../widgets/page_media.dart';
import '../widgets/window_media.dart';
import 'app_bar.dart';
import 'create_control.dart';
import 'scrollable_control.dart';

class PageControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final dynamic dispatch;

  const PageControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.dispatch})
      : super(key: key);

  @override
  State<PageControl> createState() => _PageControlState();
}

class _PageControlState extends State<PageControl> {
  String? _windowTitle;
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
  int _routeChanges = 2;
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
    widget.dispatch(
        SetPageRouteAction(_routeState.route, FletAppServices.of(context).ws));
    _routeChanges--;
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
        FletAppServices.of(context).ws.pageEventFromWeb(
            eventTarget: "page",
            eventName: "keyboard_event",
            eventData: json.encode(KeyboardEventData(
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

    // page route
    var route = widget.control.attrString("route");
    if (_routeState.route != route && route != null) {
      // route updated
      _routeState.route = route;
    }

    // theme
    var lightTheme = parseTheme(widget.control, "theme", Brightness.light);
    var darkTheme = parseTheme(widget.control, "darkTheme", Brightness.dark);
    var themeMode = ThemeMode.values.firstWhere(
        (t) =>
            t.name.toLowerCase() ==
            widget.control.attrString("themeMode", "")!.toLowerCase(),
        orElse: () => ThemeMode.system);

    debugPrint("Page theme: $themeMode");

    // keyboard handler
    var onKeyboardEvent = widget.control.attrBool("onKeyboardEvent", false)!;
    if (onKeyboardEvent && !_keyboardHandlerSubscribed) {
      RawKeyboard.instance.addListener(_handleKeyDown);
      _keyboardHandlerSubscribed = true;
    }

    // window params
    var windowTitle = widget.control.attrString("title", "")!;
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
    var minimizable = widget.control.attrBool("windowMinimizable");
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

      // window size
      if ((windowWidth != null || windowHeight != null) &&
          windowFullScreen != true &&
          (defaultTargetPlatform != TargetPlatform.macOS ||
              (defaultTargetPlatform == TargetPlatform.macOS &&
                  windowMaximized == false &&
                  windowMinimized == false))) {
        debugPrint("setWindowSize: $windowWidth, $windowHeight");
        await setWindowSize(windowWidth, windowHeight);
      }

      // window min size
      if (windowMinWidth != null || windowMinHeight != null) {
        debugPrint("setWindowMinSize: $windowMinWidth, $windowMinHeight");
        await setWindowMinSize(windowMinWidth, windowMinHeight);
      }

      // window max size
      if (windowMaxWidth != null || windowMaxHeight != null) {
        debugPrint("setWindowMaxSize: $windowMaxWidth, $windowMaxHeight");
        await setWindowMaxSize(windowMaxWidth, windowMaxHeight);
      }

      // window position
      if ((windowTop != null || windowLeft != null) &&
          windowFullScreen != true &&
          (windowCenter == null || windowCenter == "") &&
          (defaultTargetPlatform != TargetPlatform.macOS ||
              (defaultTargetPlatform == TargetPlatform.macOS &&
                  windowMaximized == false &&
                  windowMinimized == false))) {
        debugPrint("setWindowPosition: $windowTop, $windowLeft");
        await setWindowPosition(windowTop, windowLeft);
      }

      // window opacity
      if (windowOpacity != null) {
        await setWindowOpacity(windowOpacity);
      }

      // window minimizable
      if (minimizable != null) {
        await setWindowMinimizability(minimizable);
      }

      // window minimize
      if (windowMinimized == true) {
        await minimizeWindow();
      } else if (windowMinimized == false && windowMaximized == false) {
        await restoreWindow();
      }

      // window maximize
      if (windowMaximized == true) {
        await maximizeWindow();
      } else if (windowMaximized == false) {
        await unmaximizeWindow();
      }

      // window resizable
      if (windowResizable != null) {
        await setWindowResizability(windowResizable);
      }

      // window movable
      if (windowMovable != null) {
        await setWindowMovability(windowMovable);
      }

      // window fullScreen
      if (windowFullScreen != null) {
        await setWindowFullScreen(windowFullScreen);
      }

      // window alwaysOnTop
      if (windowAlwaysOnTop != null) {
        await setWindowAlwaysOnTop(windowAlwaysOnTop);
      }

      // window preventClose
      if (windowPreventClose != null) {
        await setWindowPreventClose(windowPreventClose);
      }

      if (windowTitleBarHidden != null &&
          windowTitleBarHidden != _windowTitleBarHidden) {
        await setWindowTitleBarVisibility(
            windowTitleBarHidden, windowTitleBarButtonsHidden);
        _windowTitleBarHidden = windowTitleBarHidden;
      }

      // window visible
      if (windowVisible == true) {
        await showWindow();
      } else if (windowVisible == false) {
        await hideWindow();
      }

      // window focus
      if (windowFocused == true) {
        await focusWindow();
      } else if (windowFocused == false) {
        await blurWindow();
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
      if (windowProgressBar != _windowProgressBar &&
          windowProgressBar != null) {
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

    return StoreConnector<AppState, Uri?>(
        distinct: true,
        converter: (store) => store.state.pageUri,
        builder: (context, pageUri) {
          debugPrint("Page fonts build: ${widget.control.id}");

          // load custom fonts
          parseFonts(widget.control, "fonts").forEach((fontFamily, fontUrl) {
            var fontUri = Uri.parse(fontUrl);
            if (!fontUri.hasAuthority) {
              fontUri = getAssetUri(pageUri!, fontUrl);
            }
            debugPrint("fontUri: $fontUri");
            UserFonts.loadFont(fontFamily, fontUri);
          });

          return StoreConnector<AppState, PageMediaViewModel>(
              distinct: true,
              converter: (store) => PageMediaViewModel.fromStore(store),
              builder: (context, media) {
                debugPrint("MeterialApp.router build: ${widget.control.id}");

                return MaterialApp.router(
                  showSemanticsDebugger:
                      widget.control.attrBool("showSemanticsDebugger", false)!,
                  routerDelegate: _routerDelegate,
                  routeInformationParser: _routeParser,
                  title: windowTitle,
                  theme: lightTheme,
                  darkTheme: darkTheme,
                  themeMode: themeMode,
                );
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

          List<Page<dynamic>> pages = [];
          if (routesView.isLoading || routesView.viewIds.isEmpty) {
            pages.add(FadeTransitionPage(
                child: LoadingPage(
              key: const ValueKey("Loading page"),
              title: "Flet is loading...",
              message: routesView.error,
            )));
          } else {
            // offstage
            overlayWidgets(String viewId) {
              List<Widget> overlayWidgets = [];

              if (viewId == routesView.viewIds.last) {
                overlayWidgets.addAll(routesView.offstageControls.map((c) =>
                    createControl(
                        routesView.page, c.id, routesView.page.isDisabled)));
                overlayWidgets.add(const PageMedia());
              }

              if (viewId == routesView.viewIds.first && isDesktop()) {
                overlayWidgets.add(const WindowMedia());
              }

              return overlayWidgets;
            }

            pages = routesView.viewIds.map((viewId) {
              var key = ValueKey(viewId);
              var child = _buildViewWidget(
                  routesView.page, viewId, overlayWidgets(viewId));
              return _routeChanges > 0
                  ? FadeTransitionPage(key: key, child: child)
                  : MaterialPage(key: key, child: child);
            }).toList();
          }

          return Navigator(
              key: navigatorKey,
              pages: pages,
              onPopPage: (route, dynamic result) {
                // if (!route.didPop(result)) {
                //   return false;
                // }
                // debugPrint("onPopPage");

                // if (route.settings is Page) {
                //   ws.pageEventFromWeb(
                //       eventTarget: "page",
                //       eventName: "route_pop",
                //       eventData:
                //           ((route.settings as Page).key as ValueKey).value);
                // }

                // return true;
                FletAppServices.of(context).ws.pageEventFromWeb(
                    eventTarget: "page",
                    eventName: "view_pop",
                    eventData:
                        ((route.settings as Page).key as ValueKey).value);
                return false;
              });
        });
  }

  Widget _buildViewWidget(
      Control parent, String viewId, List<Widget> overlayWidgets) {
    return StoreConnector<AppState, ControlViewModel>(
        distinct: true,
        converter: (store) {
          return ControlViewModel.fromStore(store, viewId);
        },
        ignoreChange: (state) {
          return state.controls[viewId] == null;
        },
        // onWillChange: (prev, next) {
        //   debugPrint("View StoreConnector.onWillChange(): $prev, $next");
        // },
        builder: (context, controlView) {
          debugPrint("View StoreConnector");

          var control = controlView.control;
          var children = controlView.children;

          final spacing = control.attrDouble("spacing", 10)!;
          final mainAlignment = parseMainAxisAlignment(
              control, "verticalAlignment", MainAxisAlignment.start);
          final crossAlignment = parseCrossAxisAlignment(
              control, "horizontalAlignment", CrossAxisAlignment.start);

          ScrollMode scrollMode = ScrollMode.values.firstWhere(
              (m) =>
                  m.name.toLowerCase() ==
                  control.attrString("scroll", "")!.toLowerCase(),
              orElse: () => ScrollMode.none);

          final autoScroll = control.attrBool("autoScroll", false)!;

          Control? appBar;
          Control? fab;
          List<Widget> controls = [];
          bool firstControl = true;

          for (var ctrl in children.where((c) => c.isVisible)) {
            if (ctrl.type == ControlType.appBar) {
              appBar = ctrl;
              continue;
            } else if (ctrl.type == ControlType.floatingActionButton) {
              fab = ctrl;
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

          List<String> childIds = [];
          if (appBar != null) {
            childIds.add(appBar.id);
          }

          final textDirection = parent.attrBool("rtl", false)!
              ? TextDirection.rtl
              : TextDirection.ltr;

          return StoreConnector<AppState, ControlsViewModel>(
              distinct: true,
              converter: (store) =>
                  ControlsViewModel.fromStore(store, childIds),
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
                debugPrint("Route view StoreConnector build");

                var appBarView =
                    appBar != null ? childrenViews.controlViews.last : null;

                var column = Column(
                    mainAxisAlignment: mainAlignment,
                    crossAxisAlignment: crossAlignment,
                    children: controls);

                return Directionality(
                    textDirection: textDirection,
                    child: Scaffold(
                      appBar: appBarView != null
                          ? AppBarControl(
                              parent: control,
                              control: appBarView.control,
                              children: appBarView.children,
                              parentDisabled: control.isDisabled,
                              height: appBarView.control
                                  .attrDouble("toolbarHeight", kToolbarHeight)!)
                          : null,
                      body: Stack(children: [
                        SizedBox.expand(
                            child: Container(
                                padding: parseEdgeInsets(control, "padding") ??
                                    const EdgeInsets.all(10),
                                decoration: BoxDecoration(
                                    color: HexColor.fromString(
                                        Theme.of(context),
                                        control.attrString("bgcolor", "")!)),
                                child: scrollMode != ScrollMode.none
                                    ? ScrollableControl(
                                        child: column,
                                        scrollDirection: Axis.vertical,
                                        scrollMode: scrollMode,
                                        autoScroll: autoScroll,
                                      )
                                    : column)),
                        ...overlayWidgets
                      ]),
                      floatingActionButton: fab != null
                          ? createControl(control, fab.id, control.isDisabled)
                          : null,
                    ));
              });
        });
  }
}
