import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:redux/redux.dart';

import 'actions.dart';
import 'flet_app_errors_handler.dart';
import 'flet_control_backend.dart';
import 'flet_server_protocol.dart';
import 'models/app_state.dart';
import 'protocol/add_page_controls_payload.dart';
import 'protocol/app_become_active_payload.dart';
import 'protocol/app_become_inactive_payload.dart';
import 'protocol/append_control_props_request.dart';
import 'protocol/clean_control_payload.dart';
import 'protocol/invoke_method_payload.dart';
import 'protocol/message.dart';
import 'protocol/page_controls_batch_payload.dart';
import 'protocol/page_event_from_web_request.dart';
import 'protocol/register_webclient_request.dart';
import 'protocol/register_webclient_response.dart';
import 'protocol/remove_control_payload.dart';
import 'protocol/replace_page_controls_payload.dart';
import 'protocol/session_crashed_payload.dart';
import 'protocol/update_control_props_payload.dart';
import 'protocol/update_control_props_request.dart';
import 'utils/uri.dart';

class FletServer implements FletControlBackend {
  final Store<AppState> _store;
  final int? reconnectIntervalMs;
  final int? reconnectTimeoutMs;
  final FletAppErrorsHandler? errorsHandler;

  FletServerProtocol? _clientProtocol;
  bool _disposed = false;
  String _address = "";
  String _pageName = "";
  String _pageHash = "";
  String _pageWidth = "";
  String _pageHeight = "";
  String _windowWidth = "";
  String _windowHeight = "";
  String _windowTop = "";
  String _windowLeft = "";
  String _isPWA = "";
  String _isWeb = "";
  String _isDebug = "";
  String _platform = "";
  String _platformBrightness = "";
  String _media = "";
  String _cookie = "";
  int reconnectStarted = 0;
  final Map<String, ControlInvokeMethodCallback> controlInvokeMethods;

  FletServer(this._store, this.controlInvokeMethods,
      {this.reconnectIntervalMs, this.reconnectTimeoutMs, this.errorsHandler});

  Future connect({required String address}) async {
    _address = address;

    debugPrint("Connecting to Flet server $address...");
    try {
      _clientProtocol = FletServerProtocol(
          address: _address,
          onDisconnect: _onDisconnect,
          onMessage: _onMessage);
      await _clientProtocol!.connect();
      registerWebClientInternal();
    } catch (e) {
      debugPrint("Error connecting to Flet server: $e");
      _onDisconnect();
    }
  }

  _onDisconnect() {
    if (_disposed) {
      return;
    }

    var nextReconnectDelayMs = _store.state.reconnectDelayMs;
    if (nextReconnectDelayMs == 0) {
      reconnectStarted = DateTime.now().millisecondsSinceEpoch;
    }

    // set/update timeout
    nextReconnectDelayMs =
        nextReconnectDelayMs == 0 || _clientProtocol!.isLocalConnection
            ? reconnectIntervalMs ?? _clientProtocol!.defaultReconnectIntervalMs
            : nextReconnectDelayMs * 2;

    if (reconnectTimeoutMs == null ||
        (DateTime.now().millisecondsSinceEpoch - reconnectStarted) <
            reconnectTimeoutMs!) {
      // re-connect
      _store.dispatch(PageReconnectingAction(
          isUdsPath(_address) ? "" : "Loading...", nextReconnectDelayMs));

      debugPrint("Reconnect in $nextReconnectDelayMs milliseconds");
      Future.delayed(Duration(milliseconds: nextReconnectDelayMs))
          .then((value) async {
        await connect(address: _address);
      });
    } else if (reconnectTimeoutMs != null) {
      errorsHandler
          ?.onError("Error connecting to a Flet service in a timely manner.");
    }
  }

  registerWebClient({
    required String pageName,
    required String pageRoute,
    required String pageWidth,
    required String pageHeight,
    required String windowWidth,
    required String windowHeight,
    required String windowTop,
    required String windowLeft,
    required String isPWA,
    required String isWeb,
    required String isDebug,
    required String platform,
    required String platformBrightness,
    required String media,
    required String cookie,
  }) {
    _pageName = pageName;
    _pageHash = pageRoute;
    _pageWidth = pageWidth;
    _pageHeight = pageHeight;
    _windowWidth = windowWidth;
    _windowHeight = windowHeight;
    _windowTop = windowTop;
    _windowLeft = windowLeft;
    _isPWA = isPWA;
    _isWeb = isWeb;
    _isDebug = isDebug;
    _platform = platform;
    _platformBrightness = platformBrightness;
    _media = media;
    _cookie = cookie;
  }

  registerWebClientInternal() {
    debugPrint("registerWebClientInternal");
    var page = _store.state.controls["page"];
    send(Message(
        action: MessageAction.registerWebClient,
        payload: RegisterWebClientRequest(
            pageName: _pageName,
            pageRoute: _pageHash != "" ? _pageHash : _store.state.route,
            pageWidth: page?.attrString("pageWidth") ?? _pageWidth,
            pageHeight: page?.attrString("pageHeight") ?? _pageHeight,
            windowLeft: page?.attrString("windowLeft") ?? _windowLeft,
            windowTop: page?.attrString("windowTop") ?? _windowTop,
            windowWidth: page?.attrString("windowWidth") ?? _windowWidth,
            windowHeight: page?.attrString("windowHeight") ?? _windowHeight,
            isPWA: _isPWA,
            isWeb: _isWeb,
            isDebug: _isDebug,
            platform: _platform,
            platformBrightness: _platformBrightness,
            media: _media,
            sessionId: _store.state.sessionId,
            cookie: _cookie)));
    _pageHash = "";
  }

  @override
  void updateControlState(String id, Map<String, String> props,
      {bool client = true, bool server = true}) {
    Map<String, String> allProps = {"i": id};
    for (var entry in props.entries) {
      allProps[entry.key.toLowerCase()] = entry.value;
    }
    if (client) {
      _store.dispatch(UpdateControlPropsAction(
          UpdateControlPropsPayload(props: [allProps])));
    }
    if (server) {
      _updateControlProps(props: [allProps]);
    }
  }

  @override
  void triggerControlEvent(String controlId, String eventName,
      [String eventData = ""]) {
    _sendPageEvent(
        eventTarget: controlId, eventName: eventName, eventData: eventData);
  }

  @override
  void subscribeMethods(String controlId,
      Future<String?> Function(String, Map<String, String>) methodHandler) {
    controlInvokeMethods[controlId] = methodHandler;
  }

  @override
  void unsubscribeMethods(String controlId) {
    controlInvokeMethods.remove(controlId);
  }

  _sendPageEvent(
      {required String eventTarget,
      required String eventName,
      required String eventData}) {
    send(Message(
        action: MessageAction.pageEventFromWeb,
        payload: PageEventFromWebRequest(
            eventTarget: eventTarget,
            eventName: eventName,
            eventData: eventData)));
  }

  _updateControlProps({required List<Map<String, String>> props}) {
    send(Message(
        action: MessageAction.updateControlProps,
        payload: UpdateControlPropsRequest(props: props)));
  }

  _onMessage(message) {
    debugPrint("WS message: $message");
    final msg = Message.fromJson(json.decode(message));
    switch (msg.action) {
      case MessageAction.registerWebClient:
        _store.dispatch(RegisterWebClientAction(
            RegisterWebClientResponse.fromJson(msg.payload), this));
        break;
      case MessageAction.appBecomeActive:
        _store.dispatch(AppBecomeActiveAction(
            this, AppBecomeActivePayload.fromJson(msg.payload)));
        break;
      case MessageAction.appBecomeInactive:
        _store.dispatch(AppBecomeInactiveAction(
            AppBecomeInactivePayload.fromJson(msg.payload)));
        break;
      case MessageAction.sessionCrashed:
        _store.dispatch(
            SessionCrashedAction(SessionCrashedPayload.fromJson(msg.payload)));
        break;
      case MessageAction.invokeMethod:
        _store.dispatch(InvokeMethodAction(
            InvokeMethodPayload.fromJson(msg.payload), this));
        break;
      case MessageAction.addPageControls:
        _store.dispatch(AddPageControlsAction(
            AddPageControlsPayload.fromJson(msg.payload)));
        break;
      case MessageAction.appendControlProps:
        _store.dispatch(AppendControlPropsAction(
            AppendControlPropsPayload.fromJson(msg.payload)));
        break;
      case MessageAction.updateControlProps:
        _store.dispatch(UpdateControlPropsAction(
            UpdateControlPropsPayload.fromJson(msg.payload)));
        break;
      case MessageAction.replacePageControls:
        _store.dispatch(ReplacePageControlsAction(
            ReplacePageControlsPayload.fromJson(msg.payload)));
        break;
      case MessageAction.cleanControl:
        _store.dispatch(
            CleanControlAction(CleanControlPayload.fromJson(msg.payload)));
        break;
      case MessageAction.removeControl:
        _store.dispatch(
            RemoveControlAction(RemoveControlPayload.fromJson(msg.payload)));
        break;
      case MessageAction.pageControlsBatch:
        _store.dispatch(PageControlsBatchAction(
            PageControlsBatchPayload.fromJson(msg.payload)));
        break;
      default:
    }
  }

  send(Message message) {
    final m = json.encode(message.toJson());
    _clientProtocol?.send(m);
  }

  void disconnect() {
    debugPrint("Disconnecting from Flet server.");
    _disposed = true;
    _clientProtocol?.disconnect();
  }
}
