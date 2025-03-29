import 'package:flutter/widgets.dart';

import 'controls/center.dart';
import 'controls/container.dart';
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
  Widget? createWidget(Control control) {
    switch (control.type) {
      case "Page":
        return PageControl(control: control);
      case "View":
        return ViewControl(control: control);
      case "Window":
        return WindowControl(control: control);
      case "Center":
        return CenterControl(control: control);
      case "Row":
        return RowControl(control: control);
      case "Text":
        return TextControl(control: control);
      case "Container":
        return ContainerControl(control: control);
      case "LineChart":
        return LineChartControl(control: control);
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
