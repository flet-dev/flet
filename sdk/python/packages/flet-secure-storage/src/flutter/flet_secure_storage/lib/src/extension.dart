import 'package:flet/flet.dart';

import 'secure_storage.dart';

class Extension extends FletExtension {
  @override
  FletService? createService(Control control) {
    switch (control.type) {
      case "SecureStorage":
        return SecureStorageService(control: control);
      default:
        return null;
    }
  }
}
