import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:permission_handler/permission_handler.dart';

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
    debugPrint("PermissionHandler build: ${widget.control.id}");

    () async {
      widget.backend.subscribeMethods(widget.control.id,
          (methodName, args) async {
        switch (methodName) {
          case "check_permission":
            return await parsePermission(args['of'])?.status.then((value) {
              debugPrint("PermissionHandler.check_permission: $value");
              return value.name;
            });
          case "request_permission":
            var p = parsePermission(args['of']);
            if (p != null) {
              Future<PermissionStatus> permissionStatus = p.request();
              return await permissionStatus.then((value) async {
                return value.name;
              });
            }
            break;
          case "open_app_settings":
            return await openAppSettings().then((value) => value.toString());
        }
        return null;
      });
    }();

    return const SizedBox.shrink();
  }
}
