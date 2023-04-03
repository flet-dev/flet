import 'package:flutter/material.dart';

import 'flet_server.dart';
import 'models/control.dart';
import 'models/control_view_model.dart';
import 'models/window_media_data.dart';
import 'protocol/add_page_controls_payload.dart';
import 'protocol/app_become_active_payload.dart';
import 'protocol/app_become_inactive_payload.dart';
import 'protocol/append_control_props_request.dart';
import 'protocol/clean_control_payload.dart';
import 'protocol/invoke_method_payload.dart';
import 'protocol/page_controls_batch_payload.dart';
import 'protocol/register_webclient_response.dart';
import 'protocol/remove_control_payload.dart';
import 'protocol/replace_page_controls_payload.dart';
import 'protocol/session_crashed_payload.dart';
import 'protocol/update_control_props_payload.dart';

class PageLoadAction {
  final Uri pageUri;
  final String assetsDir;
  final FletServer server;
  final Map<String, Widget Function(Control?, ControlViewModel)>?
      controlsMapping;
  PageLoadAction(
      this.pageUri, this.assetsDir, this.server, this.controlsMapping);
}

class PageReconnectingAction {
  PageReconnectingAction();
}

class PageSizeChangeAction {
  final Size newPageSize;
  final WindowMediaData? wmd;
  final FletServer server;
  PageSizeChangeAction(this.newPageSize, this.wmd, this.server);
}

class SetPageRouteAction {
  final String route;
  final FletServer server;
  SetPageRouteAction(this.route, this.server);
}

class WindowEventAction {
  final String eventName;
  final WindowMediaData wmd;
  final FletServer server;
  WindowEventAction(this.eventName, this.wmd, this.server);
}

class PageBrightnessChangeAction {
  final Brightness brightness;
  PageBrightnessChangeAction(this.brightness);
}

class RegisterWebClientAction {
  final RegisterWebClientResponse payload;
  RegisterWebClientAction(this.payload);
}

class AppBecomeActiveAction {
  final FletServer server;
  final AppBecomeActivePayload payload;
  AppBecomeActiveAction(this.server, this.payload);
}

class AppBecomeInactiveAction {
  final AppBecomeInactivePayload payload;
  AppBecomeInactiveAction(this.payload);
}

class SessionCrashedAction {
  final SessionCrashedPayload payload;
  SessionCrashedAction(this.payload);
}

class InvokeMethodAction {
  final InvokeMethodPayload payload;
  final FletServer server;
  InvokeMethodAction(this.payload, this.server);
}

class AddPageControlsAction {
  final AddPageControlsPayload payload;
  AddPageControlsAction(this.payload);
}

class ReplacePageControlsAction {
  final ReplacePageControlsPayload payload;
  ReplacePageControlsAction(this.payload);
}

class PageControlsBatchAction {
  final PageControlsBatchPayload payload;
  PageControlsBatchAction(this.payload);
}

class UpdateControlPropsAction {
  final UpdateControlPropsPayload payload;
  UpdateControlPropsAction(this.payload);
}

class AppendControlPropsAction {
  final AppendControlPropsPayload payload;
  AppendControlPropsAction(this.payload);
}

class CleanControlAction {
  final CleanControlPayload payload;
  CleanControlAction(this.payload);
}

class RemoveControlAction {
  final RemoveControlPayload payload;
  RemoveControlAction(this.payload);
}
