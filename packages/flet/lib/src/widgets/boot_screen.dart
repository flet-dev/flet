import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';

import '../flet_extension.dart';
import '../models/boot_status.dart';
import 'flet_boot_screen.dart';

/// Resolves the boot screen widget named [name] by asking each extension in
/// turn (first non-null wins), falling back to the built-in [FletBootScreen].
///
/// The fallback lives here — not in any extension — so it works identically in
/// both boot phases (the prepare phase's extension list does not include the
/// core extension). This guarantees a boot screen is ALWAYS rendered.
Widget resolveBootScreen({
  required String name,
  required Map<String, dynamic> options,
  required List<FletExtension> extensions,
  required ValueListenable<BootStatus> status,
}) {
  for (final ext in extensions) {
    final widget = ext.createBootScreen(name, options, status);
    if (widget != null) return widget;
  }
  return FletBootScreen(options: options, status: status);
}
