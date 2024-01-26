import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:url_launcher/url_launcher.dart';

import 'actions.dart';
import 'flet_server.dart';
import 'models/app_state.dart';
import 'models/control.dart';
import 'models/window_media_data.dart';
import 'protocol/add_page_controls_payload.dart';
import 'protocol/clean_control_payload.dart';
import 'protocol/invoke_method_result.dart';
import 'protocol/message.dart';
import 'protocol/remove_control_payload.dart';
import 'protocol/update_control_props_payload.dart';
import 'utils/client_storage.dart';
import 'utils/desktop.dart';
import 'utils/launch_url.dart';
import 'utils/platform_utils_non_web.dart'
    if (dart.library.js) "utils/platform_utils_web.dart";
import 'utils/session_store_non_web.dart'
    if (dart.library.js) "utils/session_store_web.dart";
import 'utils/uri.dart';

enum Actions { increment, setText, setError }

AppState appReducer(AppState state, dynamic action) {
  if (action is PageLoadAction) {
    var sessionId = SessionStore.sessionId;
    return state.copyWith(
        pageUri: action.pageUri,
        assetsDir: action.assetsDir,
        sessionId: sessionId,
        isLoading: true);
  } else if (action is PageSizeChangeAction) {
    //
    // page size changed
    //
    debugPrint("New page size: ${action.newPageSize}");

    var page = state.controls["page"];
    var controls = Map.of(state.controls);
    if (page != null && !state.isLoading) {
      var pageAttrs = Map.of(page.attrs);
      pageAttrs["width"] = action.newPageSize.width.toString();
      pageAttrs["height"] = action.newPageSize.height.toString();

      List<Map<String, String>> props = [
        {"i": "page", "width": action.newPageSize.width.toString()},
        {"i": "page", "height": action.newPageSize.height.toString()},
      ];

      if (action.wmd != null) {
        addWindowMediaEventProps(action.wmd!, pageAttrs, props);
      }
      controls[page.id] = page.copyWith(attrs: pageAttrs);
      action.server.updateControlProps(props: props);
      action.server.sendPageEvent(
          eventTarget: "page",
          eventName: "resize",
          eventData:
              "${action.newPageSize.width},${action.newPageSize.height}");
    }

    return state.copyWith(
        isRegistered: true, controls: controls, size: action.newPageSize);
  } else if (action is SetPageRouteAction) {
    //
    // page route changed
    //
    var page = state.controls["page"];
    var controls = Map.of(state.controls);
    String? deepLinkingRoute;

    if (page != null) {
      var pageAttrs = Map.of(page.attrs);
      pageAttrs["route"] = action.route;
      controls[page.id] = page.copyWith(attrs: pageAttrs);

      if (state.route == "" && state.isLoading) {
        // registering a client
        debugPrint("Registering web client with route: ${action.route}");
        String pageName = getWebPageName(state.pageUri!);

        getWindowMediaData().then((wmd) {
          action.server.registerWebClient(
              pageName: pageName,
              pageRoute: action.route,
              pageWidth: state.size.width.toString(),
              pageHeight: state.size.height.toString(),
              windowWidth: wmd.width != null ? wmd.width.toString() : "",
              windowHeight: wmd.height != null ? wmd.height.toString() : "",
              windowTop: wmd.top != null ? wmd.top.toString() : "",
              windowLeft: wmd.left != null ? wmd.left.toString() : "",
              isPWA: isProgressiveWebApp().toString(),
              isWeb: kIsWeb.toString(),
              isDebug: kDebugMode.toString(),
              platform: defaultTargetPlatform.name.toLowerCase(),
              platformBrightness: state.displayBrightness.name.toString());

          action.server.connect(address: state.pageUri!.toString());
        });
      } else if (state.isLoading) {
        // buffer route
        deepLinkingRoute = action.route;
      } else {
        // existing route change
        debugPrint("New page route: ${action.route}");
        sendRouteChangeEvent(action.server, action.route);
      }
    }

    return state.copyWith(
        controls: controls,
        route: action.route,
        deepLinkingRoute: deepLinkingRoute);
  } else if (action is WindowEventAction) {
    //
    // window event
    //

    debugPrint("Window event: ${action.eventName}");

    var page = state.controls["page"];
    var controls = Map.of(state.controls);
    if (page != null && !state.isLoading) {
      var pageAttrs = Map.of(page.attrs);
      List<Map<String, String>> props = [];
      addWindowMediaEventProps(action.wmd, pageAttrs, props);

      controls[page.id] = page.copyWith(attrs: pageAttrs);
      action.server.updateControlProps(props: props);
      action.server.sendPageEvent(
          eventTarget: "page",
          eventName: "window_event",
          eventData: action.eventName);
    }

    return state.copyWith(controls: controls);
  } else if (action is PageBrightnessChangeAction) {
    //
    // platform brightness changed
    //
    debugPrint("New platform brightness: ${action.brightness.name}");

    var page = state.controls["page"];
    var controls = Map.of(state.controls);
    if (page != null && !state.isLoading) {
      var pageAttrs = Map.of(page.attrs);
      pageAttrs["platformBrightness"] = action.brightness.name.toString();

      List<Map<String, String>> props = [
        {"i": "page", "platformBrightness": action.brightness.name.toString()},
      ];

      controls[page.id] = page.copyWith(attrs: pageAttrs);
      action.server.updateControlProps(props: props);
      action.server.sendPageEvent(
          eventTarget: "page",
          eventName: "platformBrightnessChange",
          eventData: action.brightness.name.toString());
    }
    return state.copyWith(displayBrightness: action.brightness);
  } else if (action is RegisterWebClientAction) {
    //
    // register web client
    //
    if (action.payload.error != null && action.payload.error!.isNotEmpty) {
      // error or inactive app
      return state.copyWith(
          isLoading: action.payload.appInactive,
          reconnectDelayMs: 0,
          error: action.payload.error);
    } else {
      final sessionId = action.payload.session!.id;

      // store sessionId in a cookie
      SessionStore.sessionId = sessionId;

      if (state.deepLinkingRoute != "") {
        debugPrint(
            "Sending buffered deep link route: ${state.deepLinkingRoute}");
        sendRouteChangeEvent(action.server, state.deepLinkingRoute);
      }

      // connected to the session
      return state.copyWith(
          isLoading: false,
          deepLinkingRoute: "",
          reconnectDelayMs: 0,
          sessionId: sessionId,
          error: "",
          controls: action.payload.session!.controls);
    }
  } else if (action is PageReconnectingAction) {
    //
    // reconnecting WebSocket
    //
    return state.copyWith(
        isLoading: true,
        error: "", //action.connectMessage,
        reconnectDelayMs: action.nextReconnectDelayMs);
  } else if (action is AppBecomeActiveAction) {
    //
    // app become active
    //
    action.server.registerWebClientInternal();
    return state.copyWith(error: "");
  } else if (action is AppBecomeInactiveAction) {
    //
    // app become inactive
    //
    return state.copyWith(isLoading: true, error: "");
  } else if (action is SessionCrashedAction) {
    //
    // session crashed
    //
    return state.copyWith(error: action.payload.message);
  } else if (action is InvokeMethodAction) {
    debugPrint(
        "InvokeMethodAction: ${action.payload.methodName} (controlId: ${action.payload.controlId}) (${action.payload.args})");
    if (action.payload.controlId != "") {
      // control-specific method
      var handler =
          action.server.controlInvokeMethods[action.payload.controlId];
      if (handler != null) {
        handler(action.payload.methodName, action.payload.args)
            .then((result) => action.server.sendPageEvent(
                eventTarget: "page",
                eventName: "invoke_method_result",
                eventData: json.encode(InvokeMethodResult(
                    methodId: action.payload.methodId,
                    result: result.toString()))))
            .onError((error, stackTrace) => action.server.sendPageEvent(
                eventTarget: "page",
                eventName: "invoke_method_result",
                eventData: json.encode(InvokeMethodResult(
                    methodId: action.payload.methodId,
                    error: error.toString()))));
      }
    } else {
      // global methods
      switch (action.payload.methodName) {
        case "closeInAppWebView":
          closeInAppWebView();
          break;
        case "launchUrl":
          openWebBrowser(action.payload.args["url"]!,
              webWindowName: action.payload.args["web_window_name"],
              webPopupWindow:
                  action.payload.args["web_popup_window"]?.toLowerCase() ==
                      "true",
              windowWidth:
                  int.tryParse(action.payload.args["window_width"] ?? ""),
              windowHeight:
                  int.tryParse(action.payload.args["window_height"] ?? ""));
          break;
        case "canLaunchUrl":
          canLaunchUrl(Uri.parse(action.payload.args["url"]!)).then((value) =>
              action.server.sendPageEvent(
                  eventTarget: "page",
                  eventName: "invoke_method_result",
                  eventData: json.encode(InvokeMethodResult(
                      methodId: action.payload.methodId,
                      result: value.toString()))));
          break;
        case "windowToFront":
          windowToFront();
          break;
      }
      var clientStoragePrefix = "clientStorage:";
      if (action.payload.methodName.startsWith(clientStoragePrefix)) {
        invokeClientStorage(
            action.payload.methodId,
            action.payload.methodName.substring(clientStoragePrefix.length),
            action.payload.args,
            action.server);
      }
    }
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

addWindowMediaEventProps(WindowMediaData wmd, Map<String, String> pageAttrs,
    List<Map<String, String>> props) {
  pageAttrs["windowwidth"] = wmd.width != null ? wmd.width.toString() : "";
  pageAttrs["windowheight"] = wmd.height != null ? wmd.height.toString() : "";
  pageAttrs["windowtop"] = wmd.top != null ? wmd.top.toString() : "";
  pageAttrs["windowleft"] = wmd.left != null ? wmd.left.toString() : "";
  pageAttrs["windowminimized"] =
      wmd.isMinimized != null ? wmd.isMinimized.toString() : "";
  pageAttrs["windowmaximized"] =
      wmd.isMaximized != null ? wmd.isMaximized.toString() : "";
  pageAttrs["windowfocused"] =
      wmd.isFocused != null ? wmd.isFocused.toString() : "";
  pageAttrs["windowfullscreen"] =
      wmd.isFullScreen != null ? wmd.isFullScreen.toString() : "";

  props.addAll([
    {"i": "page", "windowwidth": wmd.width != null ? wmd.width.toString() : ""},
    {
      "i": "page",
      "windowheight": wmd.height != null ? wmd.height.toString() : ""
    },
    {"i": "page", "windowtop": wmd.top != null ? wmd.top.toString() : ""},
    {"i": "page", "windowleft": wmd.left != null ? wmd.left.toString() : ""},
    {
      "i": "page",
      "windowminimized":
          wmd.isMinimized != null ? wmd.isMinimized.toString() : ""
    },
    {
      "i": "page",
      "windowmaximized":
          wmd.isMaximized != null ? wmd.isMaximized.toString() : ""
    },
    {
      "i": "page",
      "windowfocused": wmd.isFocused != null ? wmd.isFocused.toString() : ""
    },
    {
      "i": "page",
      "windowfullscreen":
          wmd.isFullScreen != null ? wmd.isFullScreen.toString() : ""
    },
  ]);
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
    if (ctrl != null) {
      for (var handler in ctrl.onRemove) {
        handler();
      }
    }
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

void sendRouteChangeEvent(FletServer server, String route) {
  List<Map<String, String>> props = [
    {"i": "page", "route": route},
  ];
  server.updateControlProps(props: props);
  server.sendPageEvent(
      eventTarget: "page", eventName: "route_change", eventData: route);
}
