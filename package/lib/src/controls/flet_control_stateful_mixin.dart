import 'package:flutter/widgets.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../protocol/update_control_props_payload.dart';

mixin FletControlStatefulMixin<T extends StatefulWidget> on State<T> {
  void updateControlProps(String id, Map<String, String> props,
      {bool clientOnly = false}) {
    var appServices = FletAppServices.of(context);
    var dispatch = appServices.store.dispatch;
    Map<String, String> allProps = {"i": id};
    for (var entry in props.entries) {
      allProps[entry.key] = entry.value;
    }
    dispatch(
        UpdateControlPropsAction(UpdateControlPropsPayload(props: [allProps])));
    if (!clientOnly) {
      appServices.server.updateControlProps(props: [allProps]);
    }
  }

  void sendControlEvent(String controlId, String eventName, String eventData) {
    FletAppServices.of(context).server.sendPageEvent(
        eventTarget: controlId, eventName: eventName, eventData: eventData);
  }

  void subscribeMethods(String controlId,
      Future<String?> Function(String, Map<String, String>) methodHandler) {
    FletAppServices.of(context).server.controlInvokeMethods[controlId] =
        methodHandler;
  }

  void unsubscribeMethods(String controlId) {
    FletAppServices.of(context).server.controlInvokeMethods.remove(controlId);
  }
}
