import 'dart:ui';

import 'package:collection/collection.dart';
import 'package:flet/src/extensions/control.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:provider/provider.dart';

import '../flet_backend.dart';
import '../models/control.dart';
import '../models/keyboard_event.dart';
import '../models/multi_view.dart';
import '../models/page_design.dart';
import '../routing/route_parser.dart';
import '../routing/route_state.dart';
import '../routing/router_delegate.dart';
import '../services/service_registry.dart';
import '../utils/locale.dart';
import '../utils/numbers.dart';
import '../utils/platform_utils_web.dart'
    if (dart.library.io) "../utils/platform_utils_non_web.dart";
import '../utils/theme.dart';
import '../utils/user_fonts.dart';
import '../widgets/animated_transition_page.dart';
import '../widgets/flet_app_context.dart';
import '../widgets/loading_page.dart';
import '../widgets/page_control_data.dart';
import '../widgets/page_media.dart';
import 'control_widget.dart';

class PageControl extends StatefulWidget {
  final Control control;

  const PageControl({super.key, required this.control});

  @override
  State<PageControl> createState() => _PageControlState();
}

class _PageControlState extends State<PageControl> with WidgetsBindingObserver {
  final _navigatorKey = GlobalKey<NavigatorState>();
  late final RouteState _routeState;
  late final SimpleRouterDelegate _routerDelegate;
  late final RouteParser _routeParser;
  late final AppLifecycleListener _appLifecycleListener;
  ServiceRegistry? _pageServices;
  ServiceRegistry? _userServices;
  bool? _prevOnKeyboardEvent;
  bool _keyboardHandlerSubscribed = false;

  bool? _adaptive;
  PageDesign _widgetsDesign = PageDesign.material;
  TargetPlatform _platform = defaultTargetPlatform;
  Brightness? _brightness;
  ThemeMode? _themeMode;
  ThemeData? _lightTheme;
  ThemeData? _darkTheme;
  Map<String, dynamic>? _localeConfiguration;
  String? _prevViewRoutes;

  final Map<int, MultiView> _multiViews = <int, MultiView>{};
  bool _registeredFromMultiViews = false;

  @override
  void initState() {
    debugPrint("Page.initState: ${widget.control.id}");
    super.initState();

    WidgetsBinding.instance.addObserver(this);
    _updateMultiViews();

    _routeParser = RouteParser();

    _routeState = RouteState(_routeParser);
    _routeState.addListener(_routeChanged);

    _routerDelegate = SimpleRouterDelegate(
      routeState: _routeState,
      navigatorKey: _navigatorKey,
      builder: (context) => _buildNavigator(context, _navigatorKey),
    );

    _appLifecycleListener = AppLifecycleListener(
        onShow: () => _handleAppLifecycleTransition('show'),
        onResume: () => _handleAppLifecycleTransition('resume'),
        onHide: () => _handleAppLifecycleTransition('hide'),
        onInactive: () => _handleAppLifecycleTransition('inactive'),
        onPause: () => _handleAppLifecycleTransition('pause'),
        onDetach: () => _handleAppLifecycleTransition('detach'),
        onRestart: () => _handleAppLifecycleTransition('restart'));

    _attachKeyboardListenerIfNeeded();
  }

  @override
  void didChangeDependencies() {
    debugPrint("Page.didChangeDependencies: ${widget.control.id}");
    super.didChangeDependencies();

    _loadFontsIfNeeded(FletBackend.of(context));
  }

  @override
  void didUpdateWidget(covariant PageControl oldWidget) {
    debugPrint("Page.didUpdateWidget: ${widget.control.id}");
    super.didUpdateWidget(oldWidget);
    _updateMultiViews();

    // page services
    var pageServicesControl = widget.control.child("_page_services");
    if (_pageServices == null && pageServicesControl != null) {
      _pageServices = ServiceRegistry(
          control: pageServicesControl,
          propertyName: "services",
          backend: FletBackend.of(context));
    }

    // user services
    var userServicesControl = widget.control.child("_user_services");
    if (_userServices == null && userServicesControl != null) {
      _userServices = ServiceRegistry(
          control: userServicesControl,
          propertyName: "services",
          backend: FletBackend.of(context));
    }

    _attachKeyboardListenerIfNeeded();
    _loadFontsIfNeeded(FletBackend.of(context));
  }

  @override
  void didChangeMetrics() {
    _updateMultiViews();
  }

  @override
  void dispose() {
    debugPrint("Page.dispose: ${widget.control.id}");
    WidgetsBinding.instance.removeObserver(this);
    _routeState.removeListener(_routeChanged);
    _appLifecycleListener.dispose();
    if (_keyboardHandlerSubscribed) {
      HardwareKeyboard.instance.removeHandler(_handleKeyDown);
    }
    super.dispose();
  }

  void _updateMultiViews() {
    if (!isMultiView()) {
      return;
    }
    bool changed = false;
    for (final FlutterView view
        in WidgetsBinding.instance.platformDispatcher.views) {
      if (!_multiViews.containsKey(view.viewId)) {
        var initialData = getViewInitialData(view.viewId);
        debugPrint("View initial data ${view.viewId}: $initialData");
        _multiViews[view.viewId] = MultiView(
            viewId: view.viewId, flutterView: view, initialData: initialData);
        widget.control.backend.triggerControlEventById(
            widget.control.id,
            "multi_view_add",
            {"view_id": view.viewId, "initial_data": initialData});
        changed = true;
      }
    }
    for (var viewId in _multiViews.keys.toList()) {
      if (!WidgetsBinding.instance.platformDispatcher.views
          .any((view) => view.viewId == viewId)) {
        _multiViews.remove(viewId);
        widget.control.backend.triggerControlEventById(
            widget.control.id, "multi_view_remove", viewId);
        changed = true;
      }
    }
    if (changed && !_registeredFromMultiViews) {
      _registeredFromMultiViews = true;
      widget.control.backend.onRouteUpdated("/");
    } else {
      // re-draw
      setState(() {});
    }
  }

  void _routeChanged() {
    FletBackend.of(context).onRouteUpdated(_routeState.route);
  }

  void _handleAppLifecycleTransition(String state) {
    widget.control.triggerEvent("app_lifecycle_state_change", state);
  }

  bool _handleKeyDown(KeyEvent e) {
    if (e is KeyDownEvent) {
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
        widget.control.triggerEvent(
            "keyboard_event",
            KeyboardEvent(
                    key: k.keyLabel,
                    isAltPressed: HardwareKeyboard.instance.isAltPressed,
                    isControlPressed:
                        HardwareKeyboard.instance.isControlPressed,
                    isShiftPressed: HardwareKeyboard.instance.isShiftPressed,
                    isMetaPressed: HardwareKeyboard.instance.isMetaPressed)
                .toMap());
      }
    }
    return false;
  }

  void _attachKeyboardListenerIfNeeded() {
    var onKeyboardEvent = widget.control.getBool("on_keyboard_event", false);
    if (onKeyboardEvent != _prevOnKeyboardEvent) {
      if (onKeyboardEvent == true && !_keyboardHandlerSubscribed) {
        HardwareKeyboard.instance.addHandler(_handleKeyDown);
        _keyboardHandlerSubscribed = true;
      } else if (onKeyboardEvent == false && _keyboardHandlerSubscribed) {
        HardwareKeyboard.instance.removeHandler(_handleKeyDown);
        _keyboardHandlerSubscribed = false;
      }
      _prevOnKeyboardEvent = onKeyboardEvent;
    }
  }

  Future<void> _loadFontsIfNeeded(FletBackend backend) async {
    final fonts = widget.control.getFonts("fonts", {})!;
    for (final entry in fonts.entries) {
      final fontFamily = entry.key;
      final fontUrl = entry.value;
      var assetSrc = backend.getAssetSource(fontUrl);
      try {
        if (assetSrc.isFile) {
          await UserFonts.loadFontFromFile(fontFamily, fontUrl);
        } else {
          await UserFonts.loadFontFromUrl(fontFamily, fontUrl);
        }
      } catch (e) {
        debugPrint("Error loading font $fontFamily: $e");
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Page.build: ${widget.control.id}");

    // clear hrefs index
    FletBackend.of(context).globalKeys.clear();

    // page route
    var route = widget.control.getString("route");
    if (route != null && _routeState.route != route) {
      // update route
      WidgetsBinding.instance.addPostFrameCallback((_) {
        _routeState.route = route;
      });
    }

    _platform = TargetPlatform.values.firstWhere(
        (a) =>
            a.name.toLowerCase() ==
            widget.control.getString("platform", "")!.toLowerCase(),
        orElse: () => defaultTargetPlatform);

    _adaptive = widget.control.adaptive;

    _widgetsDesign = _adaptive == true &&
            (_platform == TargetPlatform.iOS ||
                _platform == TargetPlatform.macOS)
        ? PageDesign.cupertino
        : PageDesign.material;

    // theme
    _themeMode = widget.control.getThemeMode("theme_mode") ??
        FletAppContext.of(context)?.themeMode;

    _localeConfiguration =
        widget.control.getLocaleConfiguration("locale_configuration");

    _brightness = context.select<FletBackend, Brightness>(
        (backend) => backend.platformBrightness);

    var windowTitle = widget.control.getString("title", "")!;

    var lightTheme =
        widget.control.getTheme("theme", context, Brightness.light);
    var darkTheme = widget.control.getString("dark_theme") == null
        ? widget.control.getTheme("theme", context, Brightness.dark)
        : parseTheme(
            widget.control.get("dark_theme"), context, Brightness.dark);

    if (_lightTheme == null || !themesEqual(_lightTheme!, lightTheme)) {
      _lightTheme = lightTheme;
    }
    if (_darkTheme == null || !themesEqual(_darkTheme!, darkTheme)) {
      _darkTheme = darkTheme;
    }

    Widget appContextChild;

    if (!isMultiView()) {
      appContextChild = _widgetsDesign == PageDesign.cupertino
          ? CupertinoApp.router(
              debugShowCheckedModeBanner: false,
              showSemanticsDebugger:
                  widget.control.getBool("show_semantics_debugger", false)!,
              routerDelegate: _routerDelegate,
              routeInformationParser: _routeParser,
              title: windowTitle,
              theme: _themeMode == ThemeMode.light ||
                      ((_themeMode == null || _themeMode == ThemeMode.system) &&
                          _brightness == Brightness.light)
                  ? parseCupertinoTheme(
                      widget.control.get("theme"), context, Brightness.light)
                  : widget.control.getString("dark_theme") != null
                      ? widget.control.getCupertinoTheme(
                          "dark_theme", context, Brightness.dark)
                      : widget.control
                          .getCupertinoTheme("theme", context, Brightness.dark),
              localizationsDelegates: const [
                GlobalMaterialLocalizations.delegate,
                GlobalWidgetsLocalizations.delegate,
                GlobalCupertinoLocalizations.delegate,
              ],
              supportedLocales: _localeConfiguration != null
                  ? _localeConfiguration!["supported_locales"]
                  : [const Locale('en', 'US')],
              locale: _localeConfiguration != null
                  ? (_localeConfiguration?["locale"])
                  : null,
            )
          : MaterialApp.router(
              debugShowCheckedModeBanner: false,
              showSemanticsDebugger:
                  widget.control.getBool("show_semantics_debugger", false)!,
              routerDelegate: _routerDelegate,
              routeInformationParser: _routeParser,
              title: windowTitle,
              localizationsDelegates: const [
                GlobalMaterialLocalizations.delegate,
                GlobalWidgetsLocalizations.delegate,
                GlobalCupertinoLocalizations.delegate,
              ],
              supportedLocales: _localeConfiguration != null
                  ? _localeConfiguration!["supported_locales"]
                  : [const Locale('en', 'US')],
              locale: _localeConfiguration != null
                  ? (_localeConfiguration?["locale"])
                  : null,
              theme: _lightTheme,
              darkTheme: _darkTheme,
              themeMode: _themeMode,
            );
    } else {
      // multi-view mode
      var appStatus = context
          .select<FletBackend, ({bool isLoading, String error})>((backend) =>
              (isLoading: backend.isLoading, error: backend.error));
      var appStartupScreenMessage =
          FletBackend.of(context).appStartupScreenMessage ?? "";

      List<Widget> views = [];
      for (var view in _multiViews.entries) {
        var multiViewControl = widget.control
            .children("multi_views")
            .firstWhereOrNull((v) => v.get("view_id") == view.key)
            ?.buildWidget("content");
        var viewChild = multiViewControl ??
            Container(
              constraints:
                  const BoxConstraints.tightFor(width: 500, height: 500),
              child: Stack(children: [
                const PageMedia(),
                LoadingPage(
                  isLoading: appStatus.isLoading,
                  message: appStatus.isLoading
                      ? appStartupScreenMessage
                      : appStatus.error,
                )
              ]),
            );
        viewChild = _widgetsDesign == PageDesign.cupertino
            ? CupertinoApp(
                debugShowCheckedModeBanner: false,
                showSemanticsDebugger:
                    widget.control.getBool("show_semantics_debugger", false)!,
                home: viewChild,
                title: windowTitle,
                theme: _themeMode == ThemeMode.light ||
                        ((_themeMode == null ||
                                _themeMode == ThemeMode.system) &&
                            _brightness == Brightness.light)
                    ? parseCupertinoTheme(
                        widget.control.get("theme"), context, Brightness.light)
                    : widget.control.getString("dark_theme") != null
                        ? widget.control.getCupertinoTheme(
                            "dark_theme", context, Brightness.dark)
                        : widget.control.getCupertinoTheme(
                            "theme", context, Brightness.dark),
                localizationsDelegates: const [
                  GlobalMaterialLocalizations.delegate,
                  GlobalWidgetsLocalizations.delegate,
                  GlobalCupertinoLocalizations.delegate,
                ],
                supportedLocales: _localeConfiguration != null
                    ? _localeConfiguration!["supported_locales"]
                    : [const Locale('en', 'US')],
                locale: _localeConfiguration != null
                    ? (_localeConfiguration?["locale"])
                    : null,
              )
            : MaterialApp(
                debugShowCheckedModeBanner: false,
                showSemanticsDebugger:
                    widget.control.getBool("show_semantics_debugger", false)!,
                home: viewChild,
                title: windowTitle,
                localizationsDelegates: const [
                  GlobalMaterialLocalizations.delegate,
                  GlobalWidgetsLocalizations.delegate,
                  GlobalCupertinoLocalizations.delegate,
                ],
                supportedLocales: _localeConfiguration != null
                    ? _localeConfiguration!["supported_locales"]
                    : [const Locale('en', 'US')],
                locale: _localeConfiguration != null
                    ? (_localeConfiguration?["locale"])
                    : null,
                theme: _lightTheme,
                darkTheme: _darkTheme,
                themeMode: _themeMode,
              );
        views.add(View(view: view.value.flutterView, child: viewChild));
      }
      appContextChild = ViewCollection(views: views);
    }

    return FletAppContext(
      themeMode: _themeMode,
      child: appContextChild,
    );
  }

  Widget _buildNavigator(
      BuildContext context, GlobalKey<NavigatorState> navigatorKey) {
    debugPrint("Page navigator build: ${widget.control.id}");

    var showAppStartupScreen =
        FletBackend.of(context).showAppStartupScreen ?? false;
    var appStartupScreenMessage =
        FletBackend.of(context).appStartupScreenMessage ?? "";

    var appStatus =
        context.select<FletBackend, ({bool isLoading, String error})>(
            (backend) => (isLoading: backend.isLoading, error: backend.error));

    var views = widget.control.children("views");
    List<Page<dynamic>> pages = [];
    if (views.isEmpty) {
      pages.add(AnimatedTransitionPage(
          key: ValueKey("empty_route_${widget.control.id}"),
          fadeTransition: true,
          duration: Duration.zero,
          child: showAppStartupScreen
              ? Stack(children: [
                  const PageMedia(),
                  LoadingPage(
                    isLoading: appStatus.isLoading,
                    message: appStatus.isLoading
                        ? appStartupScreenMessage
                        : appStatus.error,
                  )
                ])
              : const Scaffold(
                  body: PageMedia(),
                )));
    } else {
      String viewRoutes =
          views.map((v) => v.getString("route", v.id.toString())).join();

      pages = views.map((view) {
        var key = ValueKey(view.getString("route", view.id.toString()));
        var child = ControlWidget(control: view);

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
                fullscreenDialog: view.getBool("fullscreen_dialog", false)!);
      }).toList();

      _prevViewRoutes = viewRoutes;
    }

    return PageControlData(
        themeMode: _themeMode,
        brightness: _brightness,
        widgetsDesign: _widgetsDesign,
        child: Navigator(
            key: navigatorKey,
            pages: pages,
            onDidRemovePage: (page) {
              widget.control
                  .triggerEvent("view_pop", (page.key as ValueKey).value);
            }));
  }
}
