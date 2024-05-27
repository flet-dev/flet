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
    debugPrint(
        "PermissionHandler build: ${widget.control.id} (${widget.control.hashCode})");

    () async {
      widget.backend.subscribeMethods(widget.control.id,
          (methodName, args) async {
        switch (methodName) {
          case "check_permission":
            bool? isGranted = await parsePermission(args['of'])?.isGranted;
            bool? isDenied = await parsePermission(args['of'])?.isDenied;
            bool? isPermanentlyDenied =
                await parsePermission(args['of'])?.isPermanentlyDenied;
            bool? isLimited = await parsePermission(args['of'])?.isLimited;
            bool? isProvisional =
                await parsePermission(args['of'])?.isProvisional;
            bool? isRestricted =
                await parsePermission(args['of'])?.isRestricted;

            if (isGranted == true) {
              return "granted";
            } else if (isDenied == true) {
              return "denied";
            } else if (isPermanentlyDenied == true) {
              return "permanentlyDenied";
            } else if (isLimited == true) {
              return "limited";
            } else if (isProvisional == true) {
              return "provisional";
            } else if (isRestricted == true) {
              return "restricted";
            }
            return null;
          case "request_permission":
            Future<PermissionStatus> permissionStatus =
                parsePermission(args['of'])!.request();
            return permissionStatus.then((value) async {
              return value.name;
            });
        }
        return null;
      });
    }();

    return const SizedBox.shrink();
  }
}
