import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:permission_handler/permission_handler.dart';

import 'utils/permission_handler.dart';

class PermissionHandlerService extends FletService {
  PermissionHandlerService({required super.control});

  @override
  void init() {
    super.init();
    debugPrint("PermissionHandler(${control.id}).init: ${control.properties}");
    control.addInvokeMethodListener(_invokeMethod);
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("PermissionHandler.$name($args)");
    switch (name) {
      case "get_status":
        return await parsePermission(args['permission'])?.status.then((value) {
          return value.name;
        });
      case "request":
        var permission = parsePermission(args['permission']);
        if (permission != null) {
          Future<PermissionStatus> status = permission.request();
          return await status.then((value) async {
            return value.name;
          });
        }
        break;
      case "open_app_settings":
        return await openAppSettings();
      default:
        throw Exception("Unknown PermissionHandler method: $name");
    }
  }

  @override
  void dispose() {
    debugPrint("PermissionHandler(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }
}
