import 'package:flutter/widgets.dart';

import 'controls/banner.dart';
import 'controls/center.dart';
import 'controls/column.dart';
import 'controls/container.dart';
import 'controls/dropdown.dart';
import 'controls/line_chart.dart';
import 'controls/page.dart';
import 'controls/row.dart';
import 'controls/text.dart';
import 'controls/view.dart';
import 'controls/window.dart';
import 'flet_backend.dart';
import 'flet_extension.dart';
import 'flet_service.dart';
import 'models/control.dart';
import 'services/browser_context_menu.dart';
import 'services/clipboard.dart';
import 'services/shared_preferences.dart';
import 'services/url_launcher.dart';

class FletCoreExtension extends FletExtension {
  @override
  Widget? createWidget(Key? key, Control control) {
    switch (control.type) {
      case "Page":
        return PageControl(key: key, control: control);
      case "View":
        return ViewControl(key: key, control: control);
      case "Window":
        return WindowControl(key: key, control: control);
      case "Center":
        return CenterControl(key: key, control: control);
      case "Row":
        return RowControl(key: key, control: control);
      case "Column":
        return ColumnControl(key: key, control: control);
      case "Banner":
        return BannerControl(key: key, control: control);
      case "Text":
        return TextControl(key: key, control: control);
      case "Container":
        return ContainerControl(key: key, control: control);
      case "Dropdown":
        return DropdownControl(key: key, control: control);
      case "LineChart":
        return LineChartControl(key: key, control: control);
      default:
        return null;
    }
  }

  @override
  FletService? createService(Control control, FletBackend backend) {
    switch (control.type) {
      case "BrowserContextMenu":
        return BrowserContextMenuService(control, backend);
      case "Clipboard":
        return ClipboardService(control, backend);
      case "UrlLauncher":
        return UrlLauncherService(control, backend);
      case "SharedPreferences":
        return SharedPreferencesService(control, backend);
      default:
        return null;
    }
  }
}
