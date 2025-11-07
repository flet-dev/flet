import 'dart:async';

import 'package:device_info_plus/device_info_plus.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'flet_app_errors_handler.dart';
import 'flet_core_extension.dart';
import 'flet_extension.dart';
import 'models/asset_source.dart';
import 'models/control.dart';
import 'models/window_state.dart';
import 'protocol/control_event_body.dart';
import 'protocol/invoke_method_request_body.dart';
import 'protocol/invoke_method_response_body.dart';
import 'protocol/message.dart';
import 'protocol/page_media_data.dart';
import 'protocol/patch_control_request_body.dart';
import 'protocol/register_client_request_body.dart';
import 'protocol/register_client_response_body.dart';
import 'protocol/session_crashed_body.dart';
import 'protocol/update_control_body.dart';
import 'testing/tester.dart';
import 'transport/flet_backend_channel.dart';
import 'utils/desktop.dart';
import 'utils/images.dart';
import 'utils/numbers.dart';
import 'utils/platform.dart';
import 'utils/platform_utils_web.dart'
    if (dart.library.io) "utils/platform_utils_non_web.dart";
import 'utils/session_store_web.dart'
    if (dart.library.io) "utils/session_store_non_web.dart";
import 'utils/uri.dart';
import 'utils/weak_value_map.dart';

/// FletBackend - Handles business logic, provides data, and acts as ChangeNotifier
class FletBackend extends ChangeNotifier {
  bool multiView = false;
  bool _disposed = false;
  final WeakReference<FletBackend>? _parentFletBackend;
  final Uri pageUri;
  final String assetsDir;
  final bool? showAppStartupScreen;
  final String? appStartupScreenMessage;
  final int? controlId;
  final FletAppErrorsHandler? errorsHandler;
  late final List<FletExtension> extensions;
  final Map<String, dynamic>? args;
  final bool? forcePyodide;
  final Tester? tester;
  final Map<String, GlobalKey> globalKeys = {};

  final WeakValueMap<int, Control> controlsIndex = WeakValueMap<int, Control>();
  final int? _reconnectIntervalMs;
  final int? _reconnectTimeoutMs;
  int _reconnectStarted = 0;
  int _reconnectDelayMs = 0;
  FletBackendChannel? _backendChannel;
  final List<Message> _sendQueue = [];
  String route = "";
  bool isLoading = true;
  final Completer<void> pageSizeUpdated = Completer<void>();
  String error = "";
  Size pageSize = Size.zero;
  Map<String, double> sizeBreakpoints = const {
    "xs": 0,
    "sm": 576,
    "md": 768,
    "lg": 992,
    "xl": 1200,
    "xxl": 1400
  };
  Brightness platformBrightness = Brightness.light;
  PageMediaData media = PageMediaData(
    padding: PaddingData(EdgeInsets.zero),
    viewPadding: PaddingData(EdgeInsets.zero),
    viewInsets: PaddingData(EdgeInsets.zero),
    devicePixelRatio: 0,
    orientation: Orientation.portrait,
    alwaysUse24HourFormat: false,
  );
  TargetPlatform platform = defaultTargetPlatform;

  late Control _page;

  FletBackend(
      {required this.pageUri,
      required this.assetsDir,
      required this.multiView,
      int? reconnectIntervalMs,
      int? reconnectTimeoutMs,
      this.errorsHandler,
      this.showAppStartupScreen,
      this.appStartupScreenMessage,
      this.controlId,
      this.args,
      this.forcePyodide,
      this.tester,
      required extensions,
      FletBackend? parentFletBackend})
      : _parentFletBackend =
            parentFletBackend != null ? WeakReference(parentFletBackend) : null,
        _reconnectTimeoutMs = reconnectTimeoutMs,
        _reconnectIntervalMs = reconnectIntervalMs {
    // add Flet extension with core controls and services
    this.extensions = [...extensions, FletCoreExtension()];

    // initial "empty" page
    _page = Control.fromMap({
      "_c": "Page",
      "_i": 1,
      "pwa": isProgressiveWebApp(),
      "web": kIsWeb,
      "debug": kDebugMode,
      "wasm": const bool.fromEnvironment('dart.tool.dart2wasm'),
      "test": tester != null,
      "multi_view": multiView,
      "pyodide": isPyodideMode(),
      "window": {
        "_c": "Window",
        "_i": 2,
      }
    }, this);

    _page.addListener(_onPageUpdated);
    _onPageUpdated();

    if (errorsHandler != null) {
      if (controlId == null) {
        // root error handler
        errorsHandler!.addListener(() {
          triggerControlEvent(page, "error", errorsHandler!.error!);
        });
      } else if (controlId != null && _parentFletBackend != null) {
        // parent error handler
        errorsHandler?.addListener(() {
          _parentFletBackend?.target?.triggerControlEventById(
              controlId!, "error", errorsHandler!.error!);
        });
      }
    }
  }

  static FletBackend of(BuildContext context) {
    return Provider.of<FletBackend>(context, listen: false);
  }

  Control get page => _page;

  void _onPageUpdated() {
    var newPlatform = parseTargetPlatform(
        _page.getString("platform"), defaultTargetPlatform)!;
    debugPrint("Page updated: $newPlatform $platform");
    if (newPlatform != platform) {
      platform = newPlatform;
      notifyListeners();
    }
  }

  @override
  void dispose() {
    debugPrint("Disposing Flet backend.");
    _disposed = true;
    _page.removeListener(_onPageUpdated);
    _page.dispose();
    _backendChannel?.disconnect();
    super.dispose();
  }

  Future<void> connect() async {
    debugPrint("Connecting to Flet backend $pageUri...");
    try {
      _backendChannel = FletBackendChannel(
          address: pageUri.toString(),
          args: args ?? {},
          forcePyodide: forcePyodide == true,
          onDisconnect: _onDisconnect,
          onMessage: _onMessage);
      await _backendChannel!.connect();
      _registerClient();
    } catch (e) {
      debugPrint("Error connecting to Flet backend: $e");
      error = e.toString();
      _onDisconnect();
    }
  }

  _registerClient() {
    _send(
        Message(
            action: MessageAction.registerClient,
            payload: RegisterClientRequestBody(
                sessionId: SessionStore.getSessionId(),
                pageName: getWebPageName(pageUri),
                page: {
                  "route": page.get("route"),
                  "pwa": page.get("pwa"),
                  "web": page.get("web"),
                  "debug": page.get("debug"),
                  "wasm": page.get("wasm"),
                  "test": page.get("test"),
                  "multi_view": page.get("multi_view"),
                  "pyodide": page.get("pyodide"),
                  "platform_brightness": page.get("platform_brightness"),
                  "width": page.get("width"),
                  "height": page.get("height"),
                  "platform": page.get("platform"),
                  "window": page.child("window")!.toMap(),
                  "media": page.get("media"),
                }).toMap()),
        unbuffered: true);
  }

  _onClientRegistered(RegisterClientResponseBody resp) {
    if (resp.error?.isEmpty ?? true) {
      // all good!
      // store session ID in a cookie
      SessionStore.setSessionId(resp.sessionId);
      isLoading = false;
      _reconnectDelayMs = 0;
      error = "";

      page.update(resp.patch, shouldNotify: true);

      // drain send queue
      debugPrint("Send queue: ${_sendQueue.length}");
      for (var message in _sendQueue) {
        _send(message);
      }
      _sendQueue.clear();
    } else {
      // error response!
      isLoading = true;
      error = resp.error!;
      _reconnectDelayMs = 0;
    }
    _reconnectDelayMs = 0;
    notifyListeners();
  }

  void onRouteUpdated(String newRoute) {
    debugPrint("Route changed: $newRoute");

    if (route == "" && isLoading) {
      () async {
        await pageSizeUpdated.future;
        debugPrint("Registering web client with route: $newRoute");
        String platform = defaultTargetPlatform.name.toLowerCase();
        if (platform == "android") {
          try {
            DeviceInfoPlugin deviceInfo = DeviceInfoPlugin();
            AndroidDeviceInfo androidInfo = await deviceInfo.androidInfo;
            if (androidInfo.systemFeatures
                .contains('android.software.leanback')) {
              platform = "android_tv";
            }
          } on Exception catch (e) {
            debugPrint(e.toString());
          }
        }

        // update page details
        page.update({"route": newRoute, "platform": platform},
            shouldNotify: false);

        // connect to the server
        connect();
      }();
    } else {
      // existing route change
      debugPrint("New page route: $newRoute");
      _sendRouteChangeEvent(newRoute);
    }

    route = newRoute;
    notifyListeners();
  }

  /// Triggers a control event for the specified [control].
  ///
  /// This method checks if the control has an event handler for the given
  /// [eventName] and triggers the event if the application is not in a loading state.
  ///
  /// - [control]: The control for which the event is triggered.
  /// - [eventName]: The name of the event to trigger.
  /// - [eventData]: Optional data to pass along with the event.
  void triggerControlEvent(Control control, String eventName,
      [dynamic eventData]) {
    if (control.get("on_$eventName") == true) {
      debugPrint("${control.type}(${control.id}).on_$eventName($eventData)");
      triggerControlEventById(control.id, eventName, eventData);
    }
  }

  void triggerControlEventById(int controlId, String eventName,
      [dynamic eventData]) {
    _send(Message(
        action: MessageAction.controlEvent,
        payload: ControlEventBody(
                target: controlId, name: eventName, data: eventData)
            .toMap()));
  }

  void _sendRouteChangeEvent(String route) {
    updateControl(page.id, {"route": route}, notify: true);
    triggerControlEventById(page.id, "route_change", {"route": route});
  }

  void onWindowEvent(String eventName, WindowState windowState) {
    debugPrint("Window event - $eventName: $windowState");
    var window = page.get("window");
    if (window != null && window is Control) {
      updateControl(window.id, windowState.toMap());
      triggerControlEvent(window, "event", {"type": eventName});
      notifyListeners();
    }
  }

  void updatePageSize(Size newSize, {Control? view}) async {
    debugPrint("Page size updated: $newSize");
    pageSize = newSize;
    var newProps = {"width": newSize.width, "height": newSize.height};
    var ctrl = view ?? page;
    updateControl(ctrl.id, newProps);
    triggerControlEvent(ctrl, "resize", newProps);

    if (isDesktopPlatform()) {
      var windowState = await getWindowState();
      debugPrint("Window state updated: $windowState");
      var window = page.child("window")!;
      updateControl(window.id, windowState.toMap());
      triggerControlEvent(window, "event", {"type": "resized"});
    }

    if (!pageSizeUpdated.isCompleted) {
      pageSizeUpdated.complete();
    }
    notifyListeners();
  }

  void updateBrightness(Brightness newBrightness) {
    debugPrint("Platform brightness updated: $newBrightness");
    platformBrightness = newBrightness;
    updateControl(page.id, {"platform_brightness": newBrightness.name});
    triggerControlEventById(
        page.id, "platform_brightness_change", newBrightness.name);
    notifyListeners();
  }

  void updateMedia(PageMediaData newMedia, {Control? view}) {
    debugPrint("Page media updated: $newMedia");
    media = newMedia;
    var ctrl = view ?? page;
    updateControl(ctrl.id, {"media": newMedia.toMap()});
    triggerControlEvent(ctrl, "media_change", newMedia.toMap());
    notifyListeners();
  }

  /// Updates the properties of a control with the given [id].
  ///
  /// This method takes a control's unique identifier [id] and a map of
  /// properties [props] to update the control's state. The [props] map
  /// contains key-value pairs where the key is the property name and the
  /// value is the new value for that property.
  ///
  /// - [id]: The unique identifier of the control to be updated.
  /// - [props]: A map of property names and their corresponding new values.
  /// - [dart]: A boolean indicating whether to apply the patch in Dart. Defaults to `true`.
  /// - [python]: A boolean indicating whether to send the update to the Python backend. Defaults to `true`.
  /// - [notify]: A boolean indicating whether to notify listeners after applying the patch. Defaults to `false`.
  ///
  /// This method is typically used to modify the state of a control dynamically.
  void updateControl(int id, Map<String, dynamic> props,
      {bool dart = true, bool python = true, bool notify = false}) {
    var control = controlsIndex.get(id);
    if (control != null) {
      if (dart) {
        control.update(props, shouldNotify: notify);
      }
      if (python) {
        _send(Message(
            action: MessageAction.updateControl,
            payload: UpdateControlBody(id: id, props: props).toMap()));
      }
    }
  }

  /// Retrieves the asset source for a given [src].
  ///
  /// This method determines the source of an asset based on the provided [src],
  /// the current page URI, and the assets directory. It returns an [AssetSource]
  /// object that represents the resolved asset source.
  ///
  /// - [src]: The relative or absolute path to the asset.
  /// - Returns: An [AssetSource] object representing the resolved asset source.
  AssetSource getAssetSource(String src) {
    return getAssetSrc(src, pageUri, assetsDir);
  }

  _onMessage(Message message) {
    debugPrint("Received message: ${message.toList()}");
    //debugPrint("message.payload: ${message.payload}");
    switch (message.action) {
      case MessageAction.registerClient:
        _onClientRegistered(
            RegisterClientResponseBody.fromJson(message.payload));
        break;
      case MessageAction.sessionCrashed:
        _onSessionCrashed(SessionCrashedBody.fromJson(message.payload));
        break;
      case MessageAction.patchControl:
        _onPatchControl(PatchControlRequestBody.fromJson(message.payload));
        break;
      case MessageAction.invokeControlMethod:
        _onInvokeMethod(InvokeMethodRequestBody.fromJson(message.payload));
        break;
      default:
    }
  }

  _onPatchControl(PatchControlRequestBody req) {
    var control = controlsIndex.get(req.id);
    if (control != null) {
      control.applyPatch(req.patch, this);
      //debugPrint("patched control: $control");
      //debugPrint("_controlsIndex.length: ${_controlsIndex.length}");
    }
  }

  _onInvokeMethod(InvokeMethodRequestBody req) async {
    var control = controlsIndex.get(req.controlId);
    dynamic result;
    String? error;
    if (control != null) {
      try {
        result = await control.invokeMethod(req.name, req.args, req.timeout);
      } catch (e) {
        error = e.toString();
      }
    } else {
      error =
          "Calling ${req.name} method of inexistent control: ${req.controlId}";
    }

    _send(Message(
        action: MessageAction.invokeControlMethod,
        payload: InvokeMethodResponseBody(
                controlId: req.controlId,
                callId: req.callId,
                result: result,
                error: error)
            .toMap()));
  }

  _onSessionCrashed(SessionCrashedBody body) {
    error = body.message;
    notifyListeners();
  }

  _reconnect(String message, int reconnectDelayMs) {
    isLoading = true;
    error = message;
    _reconnectDelayMs = reconnectDelayMs;
    notifyListeners();
  }

  _onDisconnect() {
    if (_disposed) {
      return;
    }

    var nextReconnectDelayMs = _reconnectDelayMs;
    if (nextReconnectDelayMs == 0) {
      _reconnectStarted = DateTime.now().millisecondsSinceEpoch;
    }

    // set/update timeout
    nextReconnectDelayMs = nextReconnectDelayMs == 0 ||
            _backendChannel!.isLocalConnection
        ? _reconnectIntervalMs ?? _backendChannel!.defaultReconnectIntervalMs
        : nextReconnectDelayMs * 2;

    if (_reconnectTimeoutMs == null ||
        (DateTime.now().millisecondsSinceEpoch - _reconnectStarted) <
            _reconnectTimeoutMs!) {
      // re-connect
      _reconnect(isUdsPath(pageUri) ? "" : "Loading...", nextReconnectDelayMs);

      debugPrint("Reconnect in $nextReconnectDelayMs milliseconds");
      Future.delayed(Duration(milliseconds: nextReconnectDelayMs))
          .then((value) async {
        await connect();
      });
    } else {
      errorsHandler?.onError(error != ""
          ? error
          : "Error connecting to a Flet service in a timely manner.");
    }
  }

  _send(Message message, {bool unbuffered = false}) {
    if (unbuffered || !isLoading) {
      debugPrint("_send: ${message.action} ${message.payload}");
      _backendChannel?.send(message);
    } else {
      _sendQueue.add(message);
    }
  }
}
