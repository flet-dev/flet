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
        // Isolate failures per service. ServiceBinding throws for a control
        // type no extension can build ("Unknown service"), and letting that
        // escape aborts this loop, so every service *after* the offending one
        // is silently never bound — later invokeMethod calls on them then hang
        // until they time out. Skip the bad entry and keep going instead.
        try {
          _services[serviceControl.id] =
              ServiceBinding(control: serviceControl, backend: backend);
        } catch (e) {
          debugPrint(
              "Error creating service ${serviceControl.type}(${serviceControl.id}): $e");
        }
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

  void dispose() {
    control.removeListener(_onServicesUpdated);
    for (var service in _services.values) {
      service.dispose();
    }
    _services.clear();
  }
}
