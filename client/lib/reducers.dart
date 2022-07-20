// One simple action: Increment
import 'package:flet_view/protocol/add_page_controls_payload.dart';
import 'package:flet_view/protocol/clean_control_payload.dart';
import 'package:flet_view/protocol/message.dart';
import 'package:flet_view/protocol/remove_control_payload.dart';
import 'package:flet_view/protocol/update_control_props_payload.dart';
import 'package:flet_view/web_socket_client.dart';
import 'package:flutter/cupertino.dart';

import '../utils/platform_utils.dart'
    if (dart.library.io) "../utils/platform_utils_io.dart"
    if (dart.library.js) "../utils/platform_utils_js.dart";
import 'actions.dart';
import 'models/app_state.dart';
import 'models/control.dart';
import 'session_store/session_store.dart'
    if (dart.library.io) "session_store/session_store_io.dart"
    if (dart.library.js) "session_store/session_store_js.dart";
import 'utils/desktop.dart';
import 'utils/uri.dart';

enum Actions { increment, setText, setError }

AppState appReducer(AppState state, dynamic action) {
  if (action is PageLoadAction) {
    ws.connect(serverUrl: getWebSocketEndpoint(action.pageUri));
    return state.copyWith(
        pageUri: action.pageUri, sessionId: action.sessionId, isLoading: true);
  } else if (action is PageSizeChangeAction) {
    //
    // page size changed
    //
    // calculate break point
    final width = action.newPageSize.width;
    String newBreakpoint = "";
    state.sizeBreakpoints.forEach((bpName, bpWidth) {
      if (width >= bpWidth) {
        newBreakpoint = bpName;
      }
    });

    debugPrint(
        "New page size: ${action.newPageSize}, new breakpoint: $newBreakpoint");

    var page = state.controls["page"];
    var controls = Map.of(state.controls);
    if (page != null && !state.isLoading) {
      var pageAttrs = Map.of(page.attrs);
      pageAttrs["width"] = action.newPageSize.width.toString();
      pageAttrs["height"] = action.newPageSize.height.toString();
      controls[page.id] = page.copyWith(attrs: pageAttrs);

      List<Map<String, String>> props = [
        {"i": "page", "width": action.newPageSize.width.toString()},
        {"i": "page", "height": action.newPageSize.height.toString()},
      ];
      ws.updateControlProps(props: props);
      ws.pageEventFromWeb(
          eventTarget: "page",
          eventName: "resize",
          eventData:
              "${action.newPageSize.width},${action.newPageSize.height}");
    }

    return state.copyWith(
        controls: controls,
        size: action.newPageSize,
        sizeBreakpoint: newBreakpoint);
  } else if (action is SetPageRouteAction) {
    //
    // page route changed
    //
    var page = state.controls["page"];
    var controls = Map.of(state.controls);
    if (page != null) {
      var pageAttrs = Map.of(page.attrs);
      pageAttrs["route"] = action.route;
      controls[page.id] = page.copyWith(attrs: pageAttrs);

      if (state.route == "" && state.isLoading) {
        // registering a client
        debugPrint("Registering web client with route: ${action.route}");
        String pageName = getWebPageName(state.pageUri!);

        getWindowMediaData().then((wmd) {
          ws.registerWebClient(
              pageName: pageName,
              pageRoute: action.route,
              sessionId: state.sessionId,
              pageWidth: state.size.width.toString(),
              pageHeight: state.size.height.toString(),
              windowWidth: wmd.width != null ? wmd.width.toString() : "",
              windowHeight: wmd.height != null ? wmd.height.toString() : "",
              windowTop: wmd.top != null ? wmd.top.toString() : "",
              windowLeft: wmd.left != null ? wmd.left.toString() : "",
              isPWA: isProgressiveWebApp().toString());
        });
      } else {
        // existing route change
        debugPrint("New page route: ${action.route}");
        List<Map<String, String>> props = [
          {"i": "page", "route": action.route},
        ];
        ws.updateControlProps(props: props);
        ws.pageEventFromWeb(
            eventTarget: "page",
            eventName: "route_change",
            eventData: action.route);
      }
    }

    return state.copyWith(controls: controls, route: action.route);
  } else if (action is WindowEventAction) {
    //
    // window event
    //

    debugPrint("Window event: ${action.eventName}");

    var page = state.controls["page"];
    var controls = Map.of(state.controls);
    if (page != null && !state.isLoading) {
      var pageAttrs = Map.of(page.attrs);
      pageAttrs["windowwidth"] = action.wmd.width.toString();
      pageAttrs["windowheight"] = action.wmd.height.toString();
      pageAttrs["windowtop"] = action.wmd.top.toString();
      pageAttrs["windowleft"] = action.wmd.left.toString();
      pageAttrs["windowminimized"] = action.wmd.isMinimized.toString();
      pageAttrs["windowmaximized"] = action.wmd.isMaximized.toString();
      pageAttrs["windowfocused"] = action.wmd.isFocused.toString();
      controls[page.id] = page.copyWith(attrs: pageAttrs);

      List<Map<String, String>> props = [
        {"i": "page", "windowwidth": action.wmd.width.toString()},
        {"i": "page", "windowheight": action.wmd.height.toString()},
        {"i": "page", "windowtop": action.wmd.top.toString()},
        {"i": "page", "windowleft": action.wmd.left.toString()},
        {"i": "page", "windowminimized": action.wmd.isMinimized.toString()},
        {"i": "page", "windowmaximized": action.wmd.isMaximized.toString()},
        {"i": "page", "windowfocused": action.wmd.isFocused.toString()},
      ];
      ws.updateControlProps(props: props);
      ws.pageEventFromWeb(
          eventTarget: "page",
          eventName: "window_event",
          eventData: action.eventName);
    }

    return state.copyWith(controls: controls);
  } else if (action is PageBrightnessChangeAction) {
    return state.copyWith(displayBrightness: action.brightness);
  } else if (action is RegisterWebClientAction) {
    //
    // register web client
    //
    if (action.payload.error != null && action.payload.error!.isNotEmpty) {
      // error
      return state.copyWith(
          isLoading: false,
          reconnectingTimeout: 0,
          error: action.payload.error);
    } else {
      final sessionId = action.payload.session!.id;

      // store sessionId in a cookie
      SessionStore.set("sessionId", sessionId);

      // connected to the session
      return state.copyWith(
          isLoading: false,
          reconnectingTimeout: 0,
          sessionId: sessionId,
          controls: action.payload.session!.controls);
    }
  } else if (action is PageReconnectingAction) {
    //
    // reconnecting WebSocket
    //
    return state.copyWith(
        isLoading: true,
        reconnectingTimeout:
            state.reconnectingTimeout == 0 ? 1 : state.reconnectingTimeout * 2);
  } else if (action is AppBecomeInactiveAction) {
    //
    // app become inactive
    //
    return state.copyWith(error: action.payload.message);
  } else if (action is SessionCrashedAction) {
    //
    // session crashed
    //
    return state.copyWith(error: action.payload.message);
  } else if (action is SignoutAction) {
    // TODO
    // var redirectUrl = encodeURIComponent(window.location.pathname);
    // window.location.replace("/api/auth/signout?redirect_url=" + redirectUrl);
  } else if (action is AddPageControlsAction) {
    //
    // add controls
    //
    var controls = Map.of(state.controls);
    addControls(controls, action.payload.controls);
    removeControls(controls, action.payload.trimIDs);
    return state.copyWith(controls: controls);
  } else if (action is ReplacePageControlsAction) {
    //
    // replace controls
    //
    var controls = Map.of(state.controls);
    if (action.payload.remove) {
      removeControls(controls, action.payload.ids);
    } else {
      cleanControls(controls, action.payload.ids);
    }
    addControls(controls, action.payload.controls);
    return state.copyWith(controls: controls);
  } else if (action is PageControlsBatchAction) {
    //
    // batch of commands
    //
    var controls = Map.of(state.controls);
    for (var message in action.payload.messages) {
      if (message.action == MessageAction.addPageControls) {
        var payload = AddPageControlsPayload.fromJson(message.payload);
        addControls(controls, payload.controls);
        removeControls(controls, payload.trimIDs);
      } else if (message.action == MessageAction.updateControlProps) {
        var payload = UpdateControlPropsPayload.fromJson(message.payload);
        changeProps(controls, payload.props);
      } else if (message.action == MessageAction.cleanControl) {
        var payload = CleanControlPayload.fromJson(message.payload);
        cleanControls(controls, payload.ids);
      } else if (message.action == MessageAction.removeControl) {
        var payload = RemoveControlPayload.fromJson(message.payload);
        removeControls(controls, payload.ids);
      }
    }
    return state.copyWith(controls: controls);
  } else if (action is UpdateControlPropsAction) {
    //
    // update control props
    //
    var controls = Map.of(state.controls);
    changeProps(controls, action.payload.props);
    return state.copyWith(controls: controls);
  } else if (action is AppendControlPropsAction) {
    //
    // append control props
    //
    var controls = Map.of(state.controls);
    appendProps(controls, action.payload.props);
    return state.copyWith(controls: controls);
  } else if (action is CleanControlAction) {
    //
    // clean controls
    //
    var controls = Map.of(state.controls);
    cleanControls(controls, action.payload.ids);
    return state.copyWith(controls: controls);
  } else if (action is RemoveControlAction) {
    //
    // remove controls
    //
    var controls = Map.of(state.controls);
    removeControls(controls, action.payload.ids);
    return state.copyWith(controls: controls);
  }

  return state;
}

addControls(Map<String, Control> controls, List<Control> newControls) {
  String firstParentId = "";
  for (var ctrl in newControls) {
    if (firstParentId == "") {
      firstParentId = ctrl.pid;
    }

    final existingControl = controls[ctrl.id];
    controls[ctrl.id] = ctrl;
    if (existingControl != null) {
      controls[ctrl.id] =
          ctrl.copyWith(childIds: List.from(existingControl.childIds));
    }

    if (ctrl.pid == firstParentId && existingControl == null) {
      // root control
      final parentCtrl = controls[ctrl.pid]!;
      if (ctrl.attrs["at"] == null) {
        // append to the end
        controls[parentCtrl.id] = parentCtrl.copyWith(
            childIds: List.from(parentCtrl.childIds)..add(ctrl.id));
      } else {
        // insert at specified position
        controls[parentCtrl.id] = parentCtrl.copyWith(
            childIds: List.from(parentCtrl.childIds)
              ..insert(int.parse(ctrl.attrs["at"]!), ctrl.id));
      }
    }
  }
}

changeProps(Map<String, Control> controls, List<Map<String, String>> allProps) {
  for (var props in allProps) {
    final ctrl = controls[props["i"]];
    if (ctrl != null) {
      var attrs = Map.of(ctrl.attrs);
      for (var propName in props.keys) {
        if (propName == "i") {
          continue;
        }
        var v = props[propName];
        if (v == null || v == "") {
          attrs.remove(propName);
        } else {
          attrs[propName] = v;
        }
      }
      controls[ctrl.id] = ctrl.copyWith(attrs: attrs);
    }
  }
}

appendProps(Map<String, Control> controls, List<Map<String, String>> allProps) {
  for (var props in allProps) {
    final ctrl = controls[props["i"]];
    if (ctrl != null) {
      var attrs = Map.of(ctrl.attrs);
      for (var propName in props.keys) {
        if (propName == "i") {
          continue;
        }
        var v = props[propName] ?? "";
        attrs[propName] = v + (props[propName] ?? "");
      }
      controls[ctrl.id] = ctrl.copyWith(attrs: attrs);
    }
  }
}

cleanControls(Map<String, Control> controls, List<String> ids) {
  for (var id in ids) {
    // remove all children
    final descendantIds = getAllDescendantIds(controls, id);
    for (var descendantId in descendantIds) {
      controls.remove(descendantId);
    }

    // cleanup children collection
    controls[id] = controls[id]!.copyWith(childIds: []);
  }
}

removeControls(Map<String, Control> controls, List<String> ids) {
  for (var id in ids) {
    final ctrl = controls[id];

    // remove all children
    final descendantIds = getAllDescendantIds(controls, id);
    for (var descendantId in descendantIds) {
      controls.remove(descendantId);
    }

    // delete control itself
    controls.remove(id);

    // remove control's ID from parent's children collection
    final parentCtrl = controls[ctrl!.pid];
    controls[parentCtrl!.id] = parentCtrl.copyWith(
        childIds:
            parentCtrl.childIds.where((childId) => childId != id).toList());
  }
}

List<String> getAllDescendantIds(Map<String, Control> controls, String id) {
  if (controls[id] != null) {
    List<String> childIds = [];
    for (String childId in controls[id]!.childIds) {
      childIds
        ..add(childId)
        ..addAll(getAllDescendantIds(controls, childId));
    }
    return childIds;
  }
  return [];
}
