import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../models/boot_status.dart';
import '../utils/colors.dart';
import '../utils/numbers.dart';
import '../utils/theme.dart';

/// The built-in "flet" boot screen, used as the ultimate fallback whenever no
/// custom boot screen is configured or matched.
///
/// It always renders something (at minimum a configurable background color) so
/// the gap between the Flutter app starting and the Flet/Python app starting is
/// a controlled surface rather than a bare default scaffold.
///
/// Supported [options] (all optional):
///  - `theme_mode`: `auto` (default) | `light` | `dark`
///  - `bgcolor_light`, `bgcolor_dark`
///  - `spinner_color_light`, `spinner_color_dark`
///  - `spinner_size` (0 or absent → no spinner)
///  - `text_color_light`, `text_color_dark`
///  - `prepare_message`, `startup_message` (empty/absent → no message)
class FletBootScreen extends StatelessWidget {
  final Map<String, dynamic> options;
  final ValueListenable<BootStatus> status;

  const FletBootScreen(
      {super.key, required this.options, required this.status});

  bool _isDark(BuildContext context) {
    switch ((options["theme_mode"] as String?)?.toLowerCase()) {
      case "dark":
        return true;
      case "light":
        return false;
      default:
        return MediaQuery.platformBrightnessOf(context) == Brightness.dark;
    }
  }

  Color? _color(String key, bool dark) {
    final value = options[dark ? "${key}_dark" : "${key}_light"] as String?;
    return HexColor.fromString(null, value);
  }

  @override
  Widget build(BuildContext context) {
    final dark = _isDark(context);
    // Follow Flet's default theme (not the bare bootstrap MaterialApp theme) so
    // unset colors match what the app itself will use.
    final theme =
        parseTheme(null, context, dark ? Brightness.dark : Brightness.light);
    final bgcolor = _color("bgcolor", dark);
    final spinnerColor = _color("spinner_color", dark);
    final textColor = _color("text_color", dark);
    final spinnerSize = parseInt(options["spinner_size"], 0)!;

    return Theme(
      data: theme,
      child: ValueListenableBuilder<BootStatus>(
        valueListenable: status,
        builder: (context, bootStatus, _) {
          final child = bootStatus.error != null
              ? _buildError(context, bootStatus)
              : _buildLoading(context, bootStatus, spinnerSize, spinnerColor,
                  textColor);
          return Scaffold(
            // null → Flet theme's scaffold background.
            backgroundColor: bgcolor,
            body: Center(child: child),
          );
        },
      ),
    );
  }

  Widget _buildLoading(BuildContext context, BootStatus bootStatus,
      int spinnerSize, Color? spinnerColor, Color? textColor) {
    final message = bootStatus.stage == BootStage.preparing
        ? options["prepare_message"] as String?
        : options["startup_message"] as String?;

    final children = <Widget>[];
    if (spinnerSize > 0) {
      children.add(SizedBox(
        width: spinnerSize.toDouble(),
        height: spinnerSize.toDouble(),
        child: CircularProgressIndicator(strokeWidth: 3, color: spinnerColor),
      ));
    }
    if (message != null && message.isNotEmpty) {
      if (children.isNotEmpty) {
        children.add(const SizedBox(height: 10));
      }
      children.add(Text(
        message,
        style: Theme.of(context)
            .textTheme
            .bodySmall
            ?.copyWith(color: textColor),
      ));
    }

    return Column(mainAxisAlignment: MainAxisAlignment.center, children: children);
  }

  Widget _buildError(BuildContext context, BootStatus bootStatus) {
    final theme = Theme.of(context);
    final title = bootStatus.stage == BootStage.preparing
        ? "Error starting app"
        : "Error running app";
    final text = bootStatus.error ?? "";

    return Container(
      margin: const EdgeInsets.all(20),
      padding: const EdgeInsets.all(12),
      constraints: const BoxConstraints(maxWidth: 600),
      decoration: BoxDecoration(
          color: theme.colorScheme.errorContainer,
          borderRadius: BorderRadius.circular(8)),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Flexible(
                child: Row(mainAxisSize: MainAxisSize.min, children: [
                  Icon(Icons.error_outline,
                      color: theme.colorScheme.onErrorContainer, size: 24),
                  const SizedBox(width: 8),
                  Flexible(
                    child: Text(title,
                        style: theme.textTheme.titleSmall?.copyWith(
                            color: theme.colorScheme.onErrorContainer)),
                  ),
                ]),
              ),
              TextButton.icon(
                onPressed: () {
                  Clipboard.setData(ClipboardData(text: text));
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Copied to clipboard')),
                  );
                },
                icon: const Icon(Icons.copy, size: 16),
                label: const Text("Copy"),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Flexible(
            child: SingleChildScrollView(
              child: SelectableText(
                text,
                style: theme.textTheme.bodySmall
                    ?.copyWith(color: theme.colorScheme.onErrorContainer),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
