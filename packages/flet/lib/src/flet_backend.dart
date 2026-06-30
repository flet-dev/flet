import 'dart:async';
import 'dart:convert';

import 'package:device_info_plus/device_info_plus.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:msgpack_dart/msgpack_dart.dart' as msgpack;
import 'package:provider/provider.dart';

import 'flet_app_errors_handler.dart';
import 'flet_core_extension.dart';
import 'flet_extension.dart';
import 'models/asset_source.dart';
import 'models/boot_status.dart';
import 'models/control.dart';
import 'models/window_state.dart';
import 'protocol/control_event_body.dart';
import 'protocol/invoke_method_request_body.dart';
import 'protocol/invoke_method_response_body.dart';
import 'protocol/message.dart';
import 'protocol/page_media_data.dart';
import 'protocol/patch_control_request_body.dart';
import 'protocol/python_output_body.dart';
import 'protocol/register_client_request_body.dart';
import 'protocol/register_client_response_body.dart';
import 'protocol/session_crashed_body.dart';
import 'protocol/update_control_body.dart';
import 'testing/tester.dart';
import 'transport/data_channel.dart';
import 'transport/flet_backend_channel.dart';
import 'transport/flet_msgpack_decoder.dart';
import 'transport/flet_msgpack_encoder.dart';
import 'transport/protocol_muxed_data_channel.dart';
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
  static const String defaultAppErrorMessageTemplate =
      "The application encountered an error: {message}\n\n{details}";
  bool multiView = false;
  bool _disposed = false;
  final WeakReference<FletBackend>? _parentFletBackend;
  final Uri pageUri;
  final String assetsDir;
  final String bootScreenName;
  final Map<String, dynamic> bootScreenOptions;
  final String? appErrorMessage;
  final int? controlId;
  /// Notifies the boot screen of the current [BootStatus] (stage, any startup
  /// error, and whether boot is done). Kept in sync with [isLoading]/[error].
  ///
  /// May be injected by the embedder (e.g. a persistent boot overlay in the
  /// app bootstrap that needs the same notifier across both boot phases). When
  /// injected, this backend updates but does not own/dispose it.
  late final ValueNotifier<BootStatus> bootStatus;
  final bool _ownsBootStatus;
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
  final FletBackendChannelBuilder? _channelBuilder;
  late final DataChannelFactory _dataChannelFactory;
  final DataChannelFactory? _injectedDataChannelFactory;
  // Inbound mux registry for ProtocolMuxedDataChannel — type-byte 0x01
  // frames are routed by channel_id to the matching channel's deliver hook.
  // PythonBridge-backed DataChannels do NOT live in this registry (their
  // bytes arrive on their own native port, never on the Flet transport).
  final Map<int, ProtocolMuxedDataChannel> _dataChannels = {};
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
      this.bootScreenName = "flet",
      this.bootScreenOptions = const {},
      this.appErrorMessage,
      this.controlId,
      this.args,
      this.forcePyodide,
      this.tester,
      required extensions,
      ValueNotifier<BootStatus>? bootStatus,
      FletBackendChannelBuilder? channelBuilder,
      DataChannelFactory? dataChannelFactory,
      FletBackend? parentFletBackend})
      : _parentFletBackend =
            parentFletBackend != null ? WeakReference(parentFletBackend) : null,
        _reconnectTimeoutMs = reconnectTimeoutMs,
        _reconnectIntervalMs = reconnectIntervalMs,
        _channelBuilder = channelBuilder,
        _ownsBootStatus = bootStatus == null,
        _injectedDataChannelFactory = dataChannelFactory {
    this.bootStatus = bootStatus ??
        ValueNotifier<BootStatus>(const BootStatus(BootStage.startingUp));
    _dataChannelFactory =
        _injectedDataChannelFactory ?? ProtocolMuxedDataChannelFactory(this);
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
      "test": tester != null || const bool.fromEnvironment("FLET_TEST"),
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
    if (_ownsBootStatus) {
      bootStatus.dispose();
    }
    super.dispose();
  }

  Future<void> connect() async {
    debugPrint("Connecting to Flet backend $pageUri...");
    try {
      final builder = _channelBuilder;
      if (builder != null) {
        // Embedder-supplied transport (e.g. serious_python's in-process FFI
        // bridge). The builder is responsible for the entire transport
        // lifecycle; we just wire its callbacks to ours.
        _backendChannel = builder(
            onDisconnect: _onDisconnect, onPacket: _onPacket);
      } else {
        _backendChannel = FletBackendChannel(
            address: pageUri.toString(),
            args: args ?? {},
            forcePyodide: forcePyodide == true,
            onDisconnect: _onDisconnect,
            onPacket: _onPacket);
      }
      await _backendChannel!.connect();
      _registerClient();
    } catch (e) {
      debugPrint("Error connecting to Flet backend: $e");
      error = e.toString();
      _onDisconnect();
    }
  }

  /// Opens a dedicated [DataChannel] for high-throughput byte traffic from a
  /// widget. In embedded mode this is backed by a fresh `PythonBridge`; in
  /// dev / web modes it is a logical channel multiplexed over the active
  /// [FletBackendChannel] (see [ProtocolMuxedDataChannelFactory]).
  ///
  /// Must be called from the main Isolate (it doesn't escape there, but
  /// the returned channel is main-Isolate-bound either way).
  DataChannel openDataChannel() => _dataChannelFactory.open();

  // ---------------------------------------------------------------------
  // Mux registry — used by ProtocolMuxedDataChannel only.
  // ---------------------------------------------------------------------

  /// Registers a muxed data channel so inbound 0x01 frames for [id] are
  /// routed to it. Called from [ProtocolMuxedDataChannel.<ctor>].
  void registerDataChannel(int id, ProtocolMuxedDataChannel channel) {
    assert(!_dataChannels.containsKey(id), "duplicate data channel id $id");
    _dataChannels[id] = channel;
  }

  /// Removes [id] from the routing table. Called from
  /// [ProtocolMuxedDataChannel.close]. Idempotent — frames for an
  /// unregistered id are silently dropped.
  void unregisterDataChannel(int id) {
    _dataChannels.remove(id);
  }

  /// Sends a fully-formed packet on the active transport. Used by
  /// [ProtocolMuxedDataChannel] to ship `[0x01][channel_id:u32 LE][bytes]`
  /// alongside regular protocol traffic.
  void sendRawPacket(Uint8List packet) {
    _backendChannel?.send(packet);
  }

  _registerClient() {
    debugPrint("Registering web client: $page");
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
                  "window": page.child("window", visibleOnly: false)!.toMap(),
                  "media": page.get("media"),
                }).toMap()),
        unbuffered: true);
  }

  _onClientRegistered(RegisterClientResponseBody resp) {
    if (resp.error?.isEmpty ?? true) {
      // all good!
      // if a root FletApp, store session ID globally
      if (controlId == null) {
        SessionStore.setSessionId(resp.sessionId);
      }
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
      isLoading = false;
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
        if (platform == "android" && !kIsWeb) {
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

    // Initial page sizing should only hydrate Python state. Later size changes
    // must reach Python even if no explicit "on_resize" handler is set.
    if (pageSizeUpdated.isCompleted) {
      triggerControlEventById(ctrl.id, "resize", newProps);
    }

    if (isDesktopPlatform()) {
      var windowState = await getWindowState();
      debugPrint("Window state updated: $windowState");
      var window = page.child("window", visibleOnly: false)!;
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
    // Initial page media should only hydrate Python state. Later media changes
    // must reach Python even if no explicit "on_media_change" handler is set.
    if (pageSizeUpdated.isCompleted) {
      triggerControlEventById(ctrl.id, "media_change", newMedia.toMap());
    }
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

  /// Inbound transport dispatcher. Every packet starts with a 1-byte type
  /// discriminator:
  ///   0x00 → MsgPack-encoded Flet control frame (the existing protocol).
  ///   0x01 → raw DataChannel frame `[channel_id:u32 LE][payload]`.
  void _onPacket(Uint8List packet) {
    if (packet.isEmpty) {
      debugPrint("Dropping empty packet");
      return;
    }
    final type = packet[0];
    if (type == 0x00) {
      // Decode the MsgPack body and dispatch as a Flet protocol message.
      final body = msgpack.deserialize(
          Uint8List.sublistView(packet, 1),
          extDecoder: FletMsgpackDecoder());
      _onMessage(Message.fromList(body));
    } else if (type == 0x01) {
      if (packet.length < 5) {
        debugPrint("Dropping malformed data channel frame (len=${packet.length})");
        return;
      }
      final channelId =
          ByteData.sublistView(packet, 1, 5).getUint32(0, Endian.little);
      final channel = _dataChannels[channelId];
      if (channel == null) {
        // Stale frame after channel.close() — silently drop.
        return;
      }
      channel.deliver(Uint8List.sublistView(packet, 5));
    } else {
      debugPrint("Dropping packet with unknown type byte 0x${type.toRadixString(16)}");
    }
  }

  void _onMessage(Message message) {
    debugPrint("Received message: ${message.toList()}");
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
      case MessageAction.pythonOutput:
        _onPythonOutput(PythonOutputBody.fromJson(message.payload));
        break;
      default:
    }
  }

  void _onPythonOutput(PythonOutputBody body) {
    // Nested FletApp: bubble the line to the outer backend so the
    // host page can render it (same shape as errorsHandler bubbling
    // at lines 135-148). Root FletApp: nothing to bubble to, so fall
    // back to the browser console — preserves Pyodide's default
    // visibility now that we've taken over its stdout/stderr hooks.
    if (controlId != null && _parentFletBackend != null) {
      _parentFletBackend?.target?.triggerControlEventById(
        controlId!,
        "python_output",
        {"text": body.text, "is_stderr": body.isStderr},
      );
    } else {
      // Use `print` rather than `debugPrint` — main.dart silences
      // debugPrint in release builds, which would swallow this fallback.
      final line = body.text.endsWith('\n')
          ? body.text.substring(0, body.text.length - 1)
          : body.text;
      if (body.isStderr) {
        // ignore: avoid_print
        print("[stderr] $line");
      } else {
        // ignore: avoid_print
        print(line);
      }
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

  @override
  void notifyListeners() {
    // Keep the boot screen status in sync with the loading/error state.
    // While loading (incl. reconnecting) show the loading state; show the
    // error only once loading has settled with an error present.
    final err =
        (!isLoading && error.isNotEmpty) ? formatAppErrorMessage(error) : null;
    final newStatus = BootStatus(BootStage.startingUp,
        error: err, done: !isLoading && error.isEmpty);
    if (bootStatus.value != newStatus) {
      bootStatus.value = newStatus;
    }
    super.notifyListeners();
  }

  String formatAppErrorMessage(String rawError) {
    if (rawError.isEmpty) {
      return "";
    }
    var template = appErrorMessage ?? defaultAppErrorMessageTemplate;
    final lines = const LineSplitter().convert(rawError);
    final message = lines.isNotEmpty ? lines.first : "";
    final details = lines.length > 1 ? lines.sublist(1).join("\n") : "";
    template = template.replaceAll("{message}", message);
    if (details.isEmpty) {
      template = template.replaceAll(RegExp(r'(\r?\n)*\{details\}'), "");
    } else {
      template = template.replaceAll("{details}", details);
    }
    return template.trimRight();
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
      final encoded = msgpack.serialize(message.toList(),
          extEncoder: FletMsgpackEncoder());
      final packet = Uint8List(1 + encoded.length);
      packet[0] = 0x00;
      packet.setRange(1, packet.length, encoded);
      _backendChannel?.send(packet);
    } else {
      _sendQueue.add(message);
    }
  }
}
