import 'package:flutter/widgets.dart';

import '../flet_app_services.dart';

mixin FletControlStatelessMixin on StatelessWidget {
  void sendControlEvent(BuildContext context, String controlId,
      String eventName, String eventData) {
    FletAppServices.of(context).server.sendPageEvent(
        eventTarget: controlId, eventName: eventName, eventData: eventData);
  }
}
