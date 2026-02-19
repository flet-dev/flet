import 'dart:async';

import 'package:battery_plus/battery_plus.dart';
import 'package:flutter/foundation.dart';

import '../flet_service.dart';
import '../utils/numbers.dart';

class BatteryService extends FletService {
  final Battery _battery = Battery();
  StreamSubscription<BatteryState>? _stateSub;

  BatteryService({required super.control});

  @override
  void init() {
    super.init();
    debugPrint("BatteryService(${control.id}).init");
    control.addInvokeMethodListener(_invokeMethod);
    _updateListeners();
  }

  @override
  void update() {
    _updateListeners();
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    switch (name) {
      case "get_battery_level":
        try {
          return await _battery.batteryLevel;
        } catch (e) {
          debugPrint(
              "BatteryService.get_battery_level: unavailable battery level ($e)");
          return null;
        }
      case "get_battery_state":
        final state = await _battery.batteryState;
        return state.name;
      case "is_in_battery_save_mode":
        return _battery.isInBatterySaveMode;
      default:
        throw Exception("Unknown Battery method: $name");
    }
  }

  void _updateListeners() {
    final listenState = control.getBool("on_state_change") == true;
    if (listenState && _stateSub == null) {
      _stateSub = _battery.onBatteryStateChanged.listen((state) {
        control.triggerEvent("state_change", {"state": state.name});
      }, onError: (error) {
        debugPrint("BatteryService: error listening to state changes: $error");
      });
    } else if (!listenState && _stateSub != null) {
      _stateSub?.cancel();
      _stateSub = null;
    }
  }

  @override
  void dispose() {
    debugPrint("BatteryService(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    _stateSub?.cancel();
    _stateSub = null;
    super.dispose();
  }
}
