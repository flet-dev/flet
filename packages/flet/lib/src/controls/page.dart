import 'dart:ui';

import 'package:collection/collection.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:provider/provider.dart';

import '../extensions/control.dart';
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
import '../utils/session_store_web.dart'
    if (dart.library.io) "../utils/session_store_non_web.dart";
import '../utils/theme.dart';
import '../utils/user_fonts.dart';
import '../widgets/animated_transition_page.dart';
import '../widgets/loading_page.dart';
import '../widgets/page_context.dart';
import '../widgets/page_media.dart';
import 'control_widget.dart';

class PageControl extends StatefulWidget {
  final Control control;

  PageControl({Key? key, required this.control})
      : super(key: ValueKey("control_${control.id}"));

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
    if (pageServicesControl != null) {
      if (_pageServices == null ||
          (_pageServices != null &&
              _pageServices?.control.internals?["uid"] !=
                  pageServicesControl.internals?["uid"])) {
        _pageServices = ServiceRegistry(
            control: pageServicesControl,
            propertyName: "services",
            backend: FletBackend.of(context));
      }
    }

    // user services
    var userServicesControl = widget.control.child("_user_services");
    if (userServicesControl != null) {
      if (_userServices == null ||
          _userServices?.control.internals?["uid"] !=
              userServicesControl.internals?["uid"]) {
        _userServices = ServiceRegistry(
            control: userServicesControl,
            propertyName: "services",
            backend: FletBackend.of(context));
      }
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
    if (!widget.control.backend.multiView) {
      return;
    }
    bool changed = false;

    bool triggerAddViewEvent = SessionStore.get("triggerAddViewEvent") == null;
    for (final FlutterView view
        in WidgetsBinding.instance.platformDispatcher.views) {
      if (!_multiViews.containsKey(view.viewId)) {
        var initialData = getViewInitialData(view.viewId);
        debugPrint("View initial data ${view.viewId}: $initialData");
        _multiViews[view.viewId] = MultiView(
            viewId: view.viewId, flutterView: view, initialData: initialData);
        if (triggerAddViewEvent) {
          widget.control.backend.triggerControlEventById(
              widget.control.id,
              "multi_view_add",
              {"view_id": view.viewId, "initial_data": initialData});
        }
        changed = true;
      }
    }
    for (var viewId in _multiViews.keys.toList()) {
      if (!WidgetsBinding.instance.platformDispatcher.views
          .any((view) => view.viewId == viewId)) {
        _multiViews.remove(viewId);
        if (triggerAddViewEvent) {
          widget.control.backend.triggerControlEventById(
              widget.control.id, "multi_view_remove", viewId);
        }
        changed = true;
      }
    }
    SessionStore.set("triggerAddViewEvent", "true");
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
    widget.control.triggerEvent("app_lifecycle_state_change", {"state": state});
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
          await UserFonts.loadFontFromFile(fontFamily, assetSrc.path);
        } else {
          await UserFonts.loadFontFromUrl(fontFamily, assetSrc.path);
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

    if (!widget.control.backend.multiView) {
      // single page mode
      return _buildApp(widget.control, null);
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
            .firstWhereOrNull((v) => v.get("view_id") == view.key);

        var viewControl = multiViewControl?.children("views").firstOrNull;

        Widget viewChild = SizedBox(
          width: 100,
          height: 100,
          child: viewControl != null
              ? ControlWidget(control: viewControl)
              : Stack(children: [
                  const PageMedia(),
                  LoadingPage(
                    isLoading: appStatus.isLoading,
                    message: appStatus.isLoading
                        ? appStartupScreenMessage
                        : appStatus.error,
                  )
                ]),
        );

        viewChild = _buildApp(multiViewControl ?? widget.control, viewChild);
        views.add(View(view: view.value.flutterView, child: viewChild));
      }
      return ViewCollection(views: views);
    }
  }

  Widget _buildApp(Control control, Widget? home) {
    var platform = TargetPlatform.values.firstWhere(
        (a) =>
            a.name.toLowerCase() ==
            control.getString("platform", "")!.toLowerCase(),
        orElse: () => defaultTargetPlatform);

    var widgetsDesign = control.adaptive == true &&
            (platform == TargetPlatform.iOS || platform == TargetPlatform.macOS)
        ? PageDesign.cupertino
        : PageDesign.material;

    // theme
    var themeMode = control.getThemeMode("theme_mode") ??
        PageContext.of(context)?.themeMode;

    var localeConfiguration =
        control.getLocaleConfiguration("locale_configuration");

    var localizationsDelegates = const [
      GlobalMaterialLocalizations.delegate,
      GlobalWidgetsLocalizations.delegate,
      GlobalCupertinoLocalizations.delegate,
    ];

    var brightness = context.select<FletBackend, Brightness>(
        (backend) => backend.platformBrightness);

    var windowTitle = control.getString("title", "")!;

    var newLightTheme = control.getTheme("theme", context, Brightness.light);
    var newDarkTheme = control.getString("dark_theme") == null
        ? control.getTheme("theme", context, Brightness.dark)
        : parseTheme(control.get("dark_theme"), context, Brightness.dark);

    var lightTheme = control.get("_lightTheme");
    if (lightTheme == null || !themesEqual(lightTheme!, newLightTheme)) {
      control.updateProperties({"_lightTheme": newLightTheme}, python: false);
      lightTheme = newLightTheme;
    }

    var darkTheme = control.get("_darkTheme");
    if (darkTheme == null || !themesEqual(darkTheme!, newDarkTheme)) {
      control.updateProperties({"_darkTheme": newDarkTheme}, python: false);
      darkTheme = newDarkTheme;
    }

    var cupertinoTheme = themeMode == ThemeMode.light ||
            ((themeMode == null || themeMode == ThemeMode.system) &&
                brightness == Brightness.light)
        ? parseCupertinoTheme(control.get("theme"), context, Brightness.light)
        : control.getString("dark_theme") != null
            ? control.getCupertinoTheme("dark_theme", context, Brightness.dark)
            : control.getCupertinoTheme("theme", context, Brightness.dark);

    var showSemanticsDebugger =
        control.getBool("show_semantics_debugger", false)!;

    var app = widgetsDesign == PageDesign.cupertino
        ? home != null
            ? CupertinoApp(
                debugShowCheckedModeBanner: false,
                showSemanticsDebugger: showSemanticsDebugger,
                title: windowTitle,
                theme: cupertinoTheme,
                supportedLocales: localeConfiguration.supportedLocales,
                locale: localeConfiguration.locale,
                localizationsDelegates: localizationsDelegates,
                home: home,
              )
            : CupertinoApp.router(
                debugShowCheckedModeBanner: false,
                showSemanticsDebugger: showSemanticsDebugger,
                routerDelegate: _routerDelegate,
                routeInformationParser: _routeParser,
                title: windowTitle,
                theme: cupertinoTheme,
                localizationsDelegates: localizationsDelegates,
                supportedLocales: localeConfiguration.supportedLocales,
                locale: localeConfiguration.locale,
              )
        : home != null
            ? MaterialApp(
                debugShowCheckedModeBanner: false,
                showSemanticsDebugger: showSemanticsDebugger,
                title: windowTitle,
                theme: lightTheme,
                darkTheme: darkTheme,
                themeMode: themeMode,
                supportedLocales: localeConfiguration.supportedLocales,
                locale: localeConfiguration.locale,
                localizationsDelegates: localizationsDelegates,
                home: home,
              )
            : MaterialApp.router(
                debugShowCheckedModeBanner: false,
                showSemanticsDebugger: showSemanticsDebugger,
                routerDelegate: _routerDelegate,
                routeInformationParser: _routeParser,
                title: windowTitle,
                theme: lightTheme,
                darkTheme: darkTheme,
                themeMode: themeMode,
                localizationsDelegates: localizationsDelegates,
                supportedLocales: localeConfiguration.supportedLocales,
                locale: localeConfiguration.locale,
              );
    return PageContext(
      themeMode: themeMode,
      brightness: brightness,
      widgetsDesign: widgetsDesign,
      child: app,
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

    return Navigator(
        key: navigatorKey,
        pages: pages,
        onDidRemovePage: (page) {
          if (page.key != null) {
            widget.control.triggerEvent(
                "view_pop", {"route": (page.key as ValueKey).value});
          }
        });
  }
}
