import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';

import 'datatable2.dart';

class Extension extends FletExtension {
  @override
  Widget? createWidget(Key? key, Control control) {
    switch (control.type) {
      case "DataTable2":
        return DataTable2Control(key: key, control: control);
      default:
        return null;
    }
  }
}
