import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

/// Web stub for the Windows and Linux WebView.
///
/// `webview_all_windows` and `webview_all_linux` both import `dart:io`, so the
/// real implementation cannot be compiled by either dart2js or dart2wasm. It is
/// swapped in behind a `dart.library.io` conditional import; the web platform
/// is served by [WebviewWeb] instead, so this is never rendered.
class WebviewDesktop extends StatelessWidget {
  final Control control;

  const WebviewDesktop({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    return const ErrorControl("Webview is not yet supported on this platform.");
  }
}
