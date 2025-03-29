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
import 'transport/flet_backend_channel.dart';
import 'utils/desktop.dart';
import 'utils/images.dart';
import 'utils/platform.dart';
import 'utils/platform_utils_non_web.dart'
    if (dart.library.js) "utils/platform_utils_web.dart";
import 'utils/session_store_non_web.dart'
    if (dart.library.js) "utils/session_store_web.dart";
import 'utils/uri.dart';
import 'utils/weak_value_map.dart';

/// FletBackend - Handles business logic, provides data, and acts as ChangeNotifier
class FletBackend extends ChangeNotifier {
  bool _disposed = false;
  final WeakReference<FletBackend>? _parentFletBackend;
  final Uri pageUri;
  final String assetsDir;
  final bool? showAppStartupScreen;
  final String? appStartupScreenMessage;
  final int? controlId;
  final FletAppErrorsHandler? errorsHandler;
  final List<FletExtension> extensions;
  final Map<String, GlobalKey> globalKeys = {};

  final WeakValueMap<int, Control> _controlsIndex =
      WeakValueMap<int, Control>();
  final int? _reconnectIntervalMs;
  final int? _reconnectTimeoutMs;
  int _reconnectStarted = 0;
  int _reconnectDelayMs = 0;
  FletBackendChannel? _backendChannel;
  String route = "";
  String _deepLinkingRoute = "";
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
      viewInsets: PaddingData(EdgeInsets.zero));

  late Control _page;

  FletBackend(
      {required this.pageUri,
      required this.assetsDir,
      int? reconnectIntervalMs,
      int? reconnectTimeoutMs,
      this.errorsHandler,
      this.showAppStartupScreen,
      this.appStartupScreenMessage,
      this.controlId,
      required this.extensions,
      FletBackend? parentFletBackend})
      : _parentFletBackend =
            parentFletBackend != null ? WeakReference(parentFletBackend) : null,
        _reconnectTimeoutMs = reconnectTimeoutMs,
        _reconnectIntervalMs = reconnectIntervalMs {
    // add Flet extension with core controls and services
    extensions.add(FletCoreExtension());

    // initial "empty" page
    _page = Control.fromMap({
      "_c": "Page",
      "_i": 1,
      "pwa": isProgressiveWebApp(),
      "web": kIsWeb,
      "debug": kDebugMode,
      "window": {
        "_c": "Window",
        "_i": 2,
      }
    }, controlsIndex: _controlsIndex);

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

  Future<void> connect() async {
    debugPrint("Connecting to Flet backend $pageUri...");
    try {
      _backendChannel = FletBackendChannel(
          address: pageUri.toString(),
          onDisconnect: _onDisconnect,
          onMessage: _onMessage);
      await _backendChannel!.connect();
      _registerClient();
    } catch (e) {
      debugPrint("Error connecting to Flet backend: $e");
      _onDisconnect();
    }
  }

  _registerClient() {
    _send(Message(
        action: MessageAction.registerClient,
        payload: RegisterClientRequestBody(
                sessionId: SessionStore.sessionId,
                pageName: getWebPageName(pageUri),
                page: page)
            .toJson()));
  }

  _onClientRegistered(RegisterClientResponseBody resp) {
    if (resp.error?.isEmpty ?? true) {
      // all good!
      // store session ID in a cookie
      SessionStore.sessionId = resp.sessionId;
      isLoading = false;
      _reconnectDelayMs = 0;
      error = "";

      page.applyPatch(resp.patch, controlsIndex: _controlsIndex);

      if (_deepLinkingRoute.isNotEmpty) {
        debugPrint("Sending buffered deep link route: $_deepLinkingRoute");
        _sendRouteChangeEvent(_deepLinkingRoute);
      }
      _deepLinkingRoute = "";
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
        page.applyPatch({"route": newRoute, "platform": platform},
            notify: false);

        // connect to the server
        connect();
      }();
    } else if (isLoading) {
      // buffer route
      debugPrint("Saving deep linking route");
      _deepLinkingRoute = newRoute;
    } else {
      // existing route change
      debugPrint("New page route: $newRoute");
      _sendRouteChangeEvent(newRoute);
    }

    route = newRoute;
    notifyListeners();
  }

  void triggerControlEvent(Control control, String eventName,
      [dynamic eventData]) {
    if (!isLoading && control.get<bool>("on_$eventName", false)!) {
      triggerControlEventById(control.id, eventName, eventData);
    }
  }

  void triggerControlEventById(int controlId, String eventName,
      [dynamic eventData]) {
    _send(Message(
        action: MessageAction.controlEvent,
        payload: ControlEventBody(
                target: controlId, name: eventName, data: eventData)
            .toJson()));
  }

  void _sendRouteChangeEvent(String route) {
    updateControl(page.id, {"route": route});
    triggerControlEvent(page, "route_change", route);
  }

  void onWindowEvent(String eventName, WindowState windowState) {
    debugPrint("Window event - $eventName: $windowState");
    var window = page.child("window")!;
    updateControl(window.id, windowState.toJson());
    triggerControlEvent(window, "event", {"type": eventName});
    notifyListeners();
  }

  void updatePageSize(Size newSize) async {
    debugPrint("Page size updated: $newSize");
    pageSize = newSize;
    var eventData = {"width": newSize.width, "height": newSize.height};
    updateControl(page.id, eventData);
    triggerControlEvent(page, "resized", eventData);

    if (isDesktopPlatform()) {
      var windowState = await getWindowState();
      debugPrint("Window state updated: $windowState");
      var window = page.child("window")!;
      updateControl(window.id, windowState.toJson());
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
    triggerControlEvent(page, "platform_brightness_change");
    notifyListeners();
  }

  void updateMedia(PageMediaData newMedia) {
    debugPrint("Page media updated: $newMedia");
    media = newMedia;
    updateControl(page.id, {"media": newMedia.toJson()});
    triggerControlEvent(page, "media_change");
    notifyListeners();
  }

  void updateControl(int id, Map<String, dynamic> props,
      {bool dart = true, bool python = true, bool notify = false}) {
    var control = _controlsIndex.get(id);
    if (control != null) {
      if (dart) {
        control.applyPatch(props,
            controlsIndex: _controlsIndex, notify: notify);
      }
      if (python && !isLoading) {
        _send(Message(
            action: MessageAction.updateControl,
            payload: UpdateControlBody(id: id, props: props).toJson()));
      }
    }
  }

  AssetSource getAssetSource(String src) {
    return getAssetSrc(src, pageUri, assetsDir);
  }

  _onMessage(Message message) {
    debugPrint("Received message: ${message.toJson()}");
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
    var control = _controlsIndex.get(req.id);
    if (control != null) {
      control.applyPatch(req.patch, controlsIndex: _controlsIndex);
      //debugPrint("patched control: $control");
      //debugPrint("_controlsIndex.length: ${_controlsIndex.length}");
    }
  }

  _onInvokeMethod(InvokeMethodRequestBody req) async {
    var control = _controlsIndex.get(req.id);
    dynamic result;
    String? error;
    if (control != null) {
      try {
        result = await control.invokeMethod(req.name, req.args, req.timeout);
      } catch (e) {
        error = e.toString();
      }
    } else {
      error = "Calling ${req.name} method of inexistent control: ${req.id}";
    }

    _send(Message(
        action: MessageAction.invokeControlMethod,
        payload: InvokeMethodResponseBody(
                id: req.id, name: req.name, result: result, error: error)
            .toJson()));
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
      errorsHandler
          ?.onError("Error connecting to a Flet service in a timely manner.");
    }
  }

  _send(Message message) {
    _backendChannel?.send(message);
  }

  void disconnect() {
    debugPrint("Disconnecting from Flet backend.");
    _disposed = true;
    _backendChannel?.disconnect();
  }
}
