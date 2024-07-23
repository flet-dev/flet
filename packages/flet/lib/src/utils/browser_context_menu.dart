import 'package:flutter/services.dart';

Future<void> disableBrowserContextMenu() async {
  return BrowserContextMenu.disableContextMenu();
}

Future<void> enableBrowserContextMenu() async {
  return BrowserContextMenu.enableContextMenu();
}
