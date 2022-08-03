import 'package:flet_view/models/routes_view_model.dart';
import 'package:flet_view/widgets/page_media.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/control_type.dart';
import '../models/control_view_model.dart';
import '../models/controls_view_model.dart';
import '../models/page_media_view_model.dart';
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
import '../web_socket_client.dart';
import '../widgets/fade_transition_page.dart';
import '../widgets/loading_page.dart';
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
  String? _windowCenter;
  final _navigatorKey = GlobalKey<NavigatorState>();
  late final RouteState _routeState;
  late final SimpleRouterDelegate _routerDelegate;
  late final RouteParser _routeParser;
  int _routeChanges = 2;

  @override
  void initState() {
    _routeParser = RouteParser();

    _routeState = RouteState(_routeParser);
    _routeState.addListener(_routeChanged);

    _routerDelegate = SimpleRouterDelegate(
      routeState: _routeState,
      navigatorKey: _navigatorKey,
      builder: (context) => _buildNavigator(context, _navigatorKey),
    );

    super.initState();
  }

  void _routeChanged() {
    widget.dispatch(SetPageRouteAction(_routeState.route));
    _routeChanges--;
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
    var lightTheme = parseTheme(widget.control, "theme") ??
        ThemeData(
            colorSchemeSeed: Colors.blue,
            brightness: Brightness.light,
            useMaterial3: true,
            // fontFamily: kIsWeb && window.navigator.userAgent.contains('OS 15_')
            //     ? '-apple-system'
            //     : null,
            visualDensity: VisualDensity.standard);

    var darkTheme = parseTheme(widget.control, "darkTheme") ??
        ThemeData(
            colorSchemeSeed: Colors.blue,
            brightness: Brightness.dark,
            useMaterial3: true,
            visualDensity: VisualDensity.standard);

    var themeMode = ThemeMode.values.firstWhere(
        (t) =>
            t.name.toLowerCase() ==
            widget.control.attrString("themeMode", "")!.toLowerCase(),
        orElse: () => ThemeMode.system);

    debugPrint("Page theme: $themeMode");

    // window title
    String title = widget.control.attrString("title", "")!;
    setWindowTitle(title);

    // window params
    var windowCenter = widget.control.attrString("windowCenter");
    var fullScreen = widget.control.attrBool("windowFullScreen");

    // window size
    var windowWidth = widget.control.attrDouble("windowWidth");
    var windowHeight = widget.control.attrDouble("windowHeight");
    if ((windowWidth != null || windowHeight != null) && fullScreen != true) {
      debugPrint("setWindowSize: $windowWidth, $windowHeight");
      setWindowSize(windowWidth, windowHeight);
    }

    // window min size
    var windowMinWidth = widget.control.attrDouble("windowMinWidth");
    var windowMinHeight = widget.control.attrDouble("windowMinHeight");
    if (windowMinWidth != null || windowMinHeight != null) {
      debugPrint("setWindowMinSize: $windowMinWidth, $windowMinHeight");
      setWindowMinSize(windowMinWidth, windowMinHeight);
    }

    // window max size
    var windowMaxWidth = widget.control.attrDouble("windowMaxWidth");
    var windowMaxHeight = widget.control.attrDouble("windowMaxHeight");
    if (windowMaxWidth != null || windowMaxHeight != null) {
      debugPrint("setWindowMaxSize: $windowMaxWidth, $windowMaxHeight");
      setWindowMaxSize(windowMaxWidth, windowMaxHeight);
    }

    // window position
    var windowTop = widget.control.attrDouble("windowTop");
    var windowLeft = widget.control.attrDouble("windowLeft");
    if ((windowTop != null || windowLeft != null) &&
        fullScreen != true &&
        (windowCenter == null || windowCenter == "")) {
      debugPrint("setWindowPosition: $windowTop, $windowLeft");
      setWindowPosition(windowTop, windowLeft);
    }

    // window opacity
    var opacity = widget.control.attrDouble("windowOpacity");
    if (opacity != null) {
      setWindowOpacity(opacity);
    }

    // window minimizable
    var minimizable = widget.control.attrBool("windowMinimizable");
    if (minimizable != null) {
      setWindowMinimizability(minimizable);
    }

    // window minimize
    var minimized = widget.control.attrBool("windowMinimized");
    if (minimized == true) {
      minimizeWindow();
    } else if (minimized == false) {
      restoreWindow();
    }

    // window maximize
    var maximized = widget.control.attrBool("windowMaximized");
    if (maximized == true) {
      maximizeWindow();
    } else if (maximized == false) {
      unmaximizeWindow();
    }

    // window resizable
    var resizable = widget.control.attrBool("windowResizable");
    if (resizable != null) {
      setWindowResizability(resizable);
    }

    // window movable
    var movable = widget.control.attrBool("windowMovable");
    if (movable != null) {
      setWindowMovability(movable);
    }

    // window fullScreen
    if (fullScreen != null) {
      setWindowFullScreen(fullScreen);
    }

    // window alwaysOnTop
    var alwaysOnTop = widget.control.attrBool("windowAlwaysOnTop");
    if (alwaysOnTop != null) {
      setWindowAlwaysOnTop(alwaysOnTop);
    }

    // window preventClose
    var preventClose = widget.control.attrBool("windowPreventClose");
    if (preventClose != null) {
      setWindowPreventClose(preventClose);
    }

    // window focus
    var focused = widget.control.attrBool("windowFocused");
    if (focused == true) {
      focusWindow();
    } else if (focused == false) {
      blurWindow();
    }

    // window center
    if (windowCenter != _windowCenter) {
      centerWindow();
      _windowCenter = windowCenter;
    }

    // window destroy
    var destroy = widget.control.attrBool("windowDestroy");
    if (destroy == true) {
      destroyWindow();
    }

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
                  routerDelegate: _routerDelegate,
                  routeInformationParser: _routeParser,
                  title: title,
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
            pages.add(const FadeTransitionPage(
                child: LoadingPage(
                    key: ValueKey("Loading page"),
                    title: "Flet is loading...")));
          } else {
            // offstage
            _overlayWidgets(String viewId) {
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
                  routesView.page, viewId, _overlayWidgets(viewId));
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
                ws.pageEventFromWeb(
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

  @override
  void dispose() {
    _routeState.removeListener(_routeChanged);
    super.dispose();
  }
}
