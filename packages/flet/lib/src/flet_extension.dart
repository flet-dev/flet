import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';

import 'flet_service.dart';
import 'models/boot_status.dart';
import 'models/control.dart';

abstract class FletExtension {
  void ensureInitialized() {}

  Widget? createWidget(Key? key, Control control) {
    return null;
  }

  FletService? createService(Control control) {
    return null;
  }

  IconData? createIconData(int iconCode) {
    return null;
  }

  /// Wraps the app's content, below the app's theme and localizations and
  /// above its navigator. Widgets the extension provides here, such as an
  /// inherited theme, can be found by everything the app shows, including
  /// routes and overlays that the navigator opens (dialogs and popups), which
  /// widgets placed around a single control can't reach.
  ///
  /// Returns [child] unchanged by default.
  Widget wrapApp(BuildContext context, Widget child) {
    return child;
  }

  /// Creates a custom boot screen identified by [name].
  ///
  /// A single extension can provide multiple named boot screens. Return null
  /// if this extension does not handle the given [name] (the next extension is
  /// then tried, ultimately falling back to the built-in "flet" screen).
  ///
  /// [options] is the boot screen's settings table from `pyproject.toml`.
  /// [status] notifies the widget of the current boot [BootStatus] (stage and
  /// any startup error) — watch it with a [ValueListenableBuilder].
  Widget? createBootScreen(
      String name, Map<String, dynamic> options, ValueListenable<BootStatus> status) {
    return null;
  }
}
