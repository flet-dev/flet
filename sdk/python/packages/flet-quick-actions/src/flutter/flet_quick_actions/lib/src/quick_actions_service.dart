import 'dart:async';

import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:quick_actions/quick_actions.dart';

class QuickActionsService extends FletService {
  QuickActionsService({required super.control});

  final QuickActions _quickActions = QuickActions();
  bool _initialized = false;

  String? _pendingAction;

  Future<void> _ensureInitialized() async {
    if (_initialized) return;
    _initialized = true;

    debugPrint("QuickActionsService(${control.id})._ensureInitialized");

    control.addInvokeMethodListener(_invokeMethod);

    await _quickActions.initialize((String type) {
      debugPrint("QuickActionsService: action tapped: '$type'");
      if (control.hasEventHandler("action")) {
        control.triggerEvent("action", type);
      } else {
        _pendingAction = type;
        debugPrint(
          "QuickActionsService: buffered action '$type' "
          "(no Python handler attached yet)",
        );
      }
    });
  }

  @override
  void init() {
    super.init();
    debugPrint("QuickActionsService(${control.id}).init");
    unawaited(_ensureInitialized());
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("QuickActions.$name($args)");
    await _ensureInitialized();

    if (isMobilePlatform()) {
      switch (name) {
        case "set_shortcuts":
          final raw = args["shortcuts"] as List? ?? const [];
          final items = raw.map((e) {
            final map = e as Map;
            return ShortcutItem(
              type: map["type"] as String,
              localizedTitle: map["localized_title"] as String,
              localizedSubtitle: map["localized_subtitle"] as String?,
              icon: map["icon"] as String?,
            );
          }).toList();

          debugPrint(
            "QuickActionsService: setShortcutItems(${items.length} items)",
          );
          return await _quickActions.setShortcutItems(items);

        case "clear_shortcuts":
          debugPrint("QuickActionsService: clearShortcutItems");
          return await _quickActions.clearShortcutItems();

        case "get_pending_action":
          final action = _pendingAction;
          _pendingAction = null;
          debugPrint("QuickActionsService: get_pending_action -> $action");
          return action;

        default:
          throw Exception("Unknown QuickActions method: $name");
      }
    } else {
      throw Exception(
          "QuickActions service is supported only on Android and iOS devices.");
    }
  }

  @override
  void dispose() {
    debugPrint("QuickActionsService(${control.id}).dispose");
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }
}