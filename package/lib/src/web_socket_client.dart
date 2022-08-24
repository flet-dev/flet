import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:redux/redux.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

import 'actions.dart';
import 'models/app_state.dart';
import 'protocol/add_page_controls_payload.dart';
import 'protocol/app_become_active_payload.dart';
import 'protocol/app_become_inactive_payload.dart';
import 'protocol/append_control_props_request.dart';
import 'protocol/clean_control_payload.dart';
import 'protocol/message.dart';
import 'protocol/page_controls_batch_payload.dart';
import 'protocol/page_event_from_web_request.dart';
import 'protocol/register_webclient_request.dart';
import 'protocol/register_webclient_response.dart';
import 'protocol/remove_control_payload.dart';
import 'protocol/replace_page_controls_payload.dart';
import 'protocol/session_crashed_payload.dart';
import 'protocol/signout_payload.dart';
import 'protocol/update_control_props_payload.dart';
import 'protocol/update_control_props_request.dart';

class WebSocketClient {
  final Store<AppState> _store;
  WebSocketChannel? _channel;
  String _serverUrl = "";
  bool _connected = false;
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
  String _platform = "";
  String? _sessionId;

  WebSocketClient(this._store);

  connect({required String serverUrl}) async {
    _serverUrl = serverUrl;

    debugPrint("Connecting to WebSocket server $serverUrl...");
    try {
      _channel = WebSocketChannel.connect(Uri.parse(_serverUrl));
      _connected = true;
      _channel!.stream.listen(_onMessage, onDone: () async {
        debugPrint("WS stream closed");
        _store.dispatch(PageReconnectingAction());
        debugPrint("Reconnect in ${_store.state.reconnectingTimeout} seconds");
        Future.delayed(Duration(seconds: _store.state.reconnectingTimeout))
            .then((value) {
          connect(serverUrl: _serverUrl);
          registerWebClientInternal();
        });
      }, onError: (error) async {
        debugPrint("WS stream error $error");
        // Future.delayed(Duration(seconds: reconnectionTimeoutSeconds))
        //     .then((value) => connect(serverUrl: _serverUrl));
      });
    } catch (e) {
      debugPrint("WebSocket connection error: $e");
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
    required String platform,
    String? sessionId,
  }) {
    bool firstCall = _pageName == "";
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
    _platform = platform;
    _sessionId = sessionId;

    if (firstCall) {
      registerWebClientInternal();
    }
  }

  registerWebClientInternal() {
    debugPrint("registerWebClientInternal");
    var page = _store.state.controls["page"];
    send(Message(
        action: MessageAction.registerWebClient,
        payload: RegisterWebClientRequest(
            pageName: _pageName,
            pageRoute:
                _store.state.route != "" ? _store.state.route : _pageHash,
            pageWidth: page?.attrString("pageWidth") ?? _pageWidth,
            pageHeight: page?.attrString("pageHeight") ?? _pageHeight,
            windowLeft: page?.attrString("windowLeft") ?? _windowLeft,
            windowTop: page?.attrString("windowTop") ?? _windowTop,
            windowWidth: page?.attrString("windowWidth") ?? _windowWidth,
            windowHeight: page?.attrString("windowHeight") ?? _windowHeight,
            isPWA: _isPWA,
            isWeb: _isWeb,
            platform: _platform,
            sessionId: _sessionId)));
  }

  pageEventFromWeb(
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

  updateControlProps({required List<Map<String, String>> props}) {
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
            RegisterWebClientResponse.fromJson(msg.payload)));
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
      case MessageAction.signout:
        _store.dispatch(SignoutAction(SignoutPayload.fromJson(msg.payload)));
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
    if (_channel != null) {
      final m = json.encode(message.toJson());
      debugPrint("Send: $m");
      _channel!.sink.add(m);
    }
  }

  close() {
    if (_channel != null && _connected) {
      _channel!.sink.close();
    }
  }
}
