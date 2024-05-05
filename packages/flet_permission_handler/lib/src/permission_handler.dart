import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'utils/permission_handler.dart';

class PermissionHandlerControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final FletControlBackend backend;

  const PermissionHandlerControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.backend});

  @override
  State<PermissionHandlerControl> createState() =>
      _PermissionHandlerControlState();
}

class _PermissionHandlerControlState extends State<PermissionHandlerControl>
    with FletStoreMixin {
  @override
  void initState() {
    debugPrint("PermissionHandler.initState($hashCode)");
    widget.control.onRemove.clear();
    widget.control.onRemove.add(_onRemove);
    super.initState();
  }

  void _onRemove() {
    debugPrint("PermissionHandler.remove($hashCode)");
    widget.backend.unsubscribeMethods(widget.control.id);
  }

  @override
  void deactivate() {
    debugPrint("PermissionHandler.deactivate($hashCode)");
    super.deactivate();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint(
        "PermissionHandler build: ${widget.control.id} (${widget.control.hashCode})");
    
    () async {
      widget.backend.subscribeMethods(widget.control.id,
          (methodName, args) async {
        switch (methodName) {
          case "checkPermission":
            return checkPermission(args['permissionOf']!);
          case "requestPermission":
            return requestPermission(args['permissionOf']!);
        }
        return null;
      });
    }();

    return const SizedBox.shrink();
  }
}
