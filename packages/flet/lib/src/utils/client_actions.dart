import 'package:flutter/widgets.dart';

import '../flet_backend.dart';
import '../models/control.dart';
import 'launch_url.dart';

/// Client actions can run for as long as the user keeps a native dialog open,
/// so the invoke-method timeout has to be generous rather than interactive.
const _kClientActionTimeout = Duration(hours: 1);

/// Runs the client actions declared on a control, by invoking the target
/// service's method directly on this client.
///
/// MUST be called synchronously from a gesture callback, and its result MUST
/// NOT be awaited. Browsers - WebKit strictly, others more leniently - permit
/// gesture-gated APIs such as opening a file picker, writing to the clipboard,
/// `navigator.share` and `window.open` only while user activation is live, and
/// activation does not survive an async gap. Awaiting anything before the
/// service method is entered silently breaks every one of them on iOS Safari
/// while leaving Android and desktop working. See flet-dev/flet#3710.
///
/// For the same reason each targeted service's `_invokeMethod` must reach its
/// gated call before its own first `await`.
void runClientActions(BuildContext context, dynamic actions) {
  if (actions == null) return;
  var backend = FletBackend.of(context);
  for (var action in actions is List ? actions : [actions]) {
    if (action is! Map) continue;
    var serviceId = action["service_id"];
    var method = action["method"];
    var service = backend.controlsIndex.get(serviceId);

    // Skip rather than await: invokeMethod() waits for a listener when the
    // service is not mounted yet, and that wait would consume the gesture and
    // leave the action failing silently.
    if (service == null || !service.hasInvokeMethodListeners) {
      debugPrint(
          "Client action target is not available: $method on service $serviceId");
      continue;
    }

    // Services distinguish the two entry points: reaching them from a gesture
    // is what makes gesture-gated APIs work, and a result cannot be returned
    // to a caller that does not exist, so services report it as an event.
    var args = {...?(action["args"] as Map?), "_from_gesture": true};

    service
        .invokeMethod(method, args, _kClientActionTimeout)
        .catchError((e) => debugPrint("Client action $method failed: $e"));
  }
}

/// Runs everything a control performs on the client when it is activated: its
/// `url`, then its `action`s, in that order.
///
/// Call this from the control's tap/press callback in place of handling `url`
/// separately. The same synchronous-call rule as [runClientActions] applies -
/// `url` is subject to it too, since opening a new tab is gesture-gated as
/// well.
void runControlActions(BuildContext context, Control control) {
  var url = control.getUrl("url");
  if (url != null) {
    openWebBrowser(url);
  }
  runClientActions(context, control.get("action"));
}

extension ClientActionParsers on Control {
  /// Whether this control performs anything on the client when it is
  /// activated - a `url` to open, or one or more `action`s.
  ///
  /// Controls that stay untappable unless something is wired to them use this
  /// to decide whether to install a tap handler at all.
  bool get hasControlActions => get("url") != null || get("action") != null;
}
