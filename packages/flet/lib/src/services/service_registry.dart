import 'package:flutter/cupertino.dart';

import '../flet_backend.dart';
import '../models/control.dart';
import 'service_binding.dart';

class ServiceRegistry {
  final Control control;
  final String propertyName;
  final FletBackend backend;
  final Map<int, ServiceBinding> _services = {};

  ServiceRegistry(
      {required this.control,
      required this.propertyName,
      required this.backend}) {
    debugPrint("Init service registry: ${control.id}");
    control.addListener(_onServicesUpdated);
    _onServicesUpdated();
  }

  void _onServicesUpdated() {
    var serviceControls = control.children(propertyName);
    debugPrint("_onServicesUpdated(${serviceControls.length})");

    // newly added services
    for (var serviceControl in serviceControls) {
      if (!_services.containsKey(serviceControl.id)) {
        _services[serviceControl.id] =
            ServiceBinding(control: serviceControl, backend: backend);
      }
    }

    // removed services
    for (var serviceId in _services.keys.toList()) {
      if (!serviceControls
          .any((serviceControl) => serviceControl.id == serviceId)) {
        _services[serviceId]!.dispose();
        _services.remove(serviceId);
      }
    }
  }
}
