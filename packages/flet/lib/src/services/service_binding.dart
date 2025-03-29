import '../flet_backend.dart';
import '../flet_service.dart';
import '../models/control.dart';

class ServiceBinding {
  final Control control;
  final FletBackend backend;
  FletService? _service;

  ServiceBinding({required this.control, required this.backend}) {
    for (var extension in backend.extensions) {
      _service = extension.createService(control, backend);
      if (_service != null) {
        break;
      }
    }
    if (_service == null) {
      throw Exception("Unknown service: ${control.type}");
    }
    _service?.init();
    control.addListener(_onControlUpdated);
  }

  void dispose() {
    control.removeListener(_onControlUpdated);
    _service?.dispose();
  }

  void _onControlUpdated() {
    _service?.update();
  }
}
