import 'package:flutter/widgets.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../services/service_registry.dart';
import 'base_controls.dart';

class ServiceHostControl extends StatefulWidget {
  final Control control;

  const ServiceHostControl({super.key, required this.control});

  @override
  State<ServiceHostControl> createState() => _ServiceHostControlState();
}

class _ServiceHostControlState extends State<ServiceHostControl> {
  ServiceRegistry? _registry;

  @override
  void initState() {
    debugPrint("ServiceHost.initState: ${widget.control.id}");
    super.initState();

    if (_registry == null) {
      _registry = ServiceRegistry(
          control: widget.control,
          propertyName: "services",
          backend: widget.control.backend);
    }
  }

  @override
  void dispose() {
    _registry?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("ServiceHost.build: ${widget.control.id}");
    return BaseControl(
        control: widget.control,
        child:
            widget.control.buildWidget("content") ?? const SizedBox.shrink());
  }
}
