import 'dart:async';

import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:flutter/foundation.dart';

import '../flet_service.dart';
import '../utils/numbers.dart';

class ConnectivityService extends FletService {
  final Connectivity _connectivity = Connectivity();
  StreamSubscription<List<ConnectivityResult>>? _subscription;

  ConnectivityService({required super.control});

  @override
  void init() {
    super.init();
    debugPrint("ConnectivityService(${control.id}).init");
    control.addInvokeMethodListener(_invokeMethod);
    _updateListeners();
  }

  @override
  void update() {
    _updateListeners();
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    switch (name) {
      case "get_connectivity":
        final results = await _connectivity.checkConnectivity();
        return results.map((r) => r.name).toList();
      default:
        throw Exception("Unknown Connectivity method: $name");
    }
  }

  void _updateListeners() {
    final listenChange = control.getBool("on_change") == true;
    if (listenChange && _subscription == null) {
      _subscription = _connectivity.onConnectivityChanged.listen(
          (List<ConnectivityResult> result) {
        control.triggerEvent(
            "change", {"connectivity": result.map((r) => r.name).toList()});
      }, onError: (error) {
        debugPrint(
            "ConnectivityService: error listening to connectivity: $error");
      });
    } else if (!listenChange && _subscription != null) {
      _subscription?.cancel();
      _subscription = null;
    }
  }

  @override
  void dispose() {
    debugPrint("ConnectivityService(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    _subscription?.cancel();
    _subscription = null;
    super.dispose();
  }
}
