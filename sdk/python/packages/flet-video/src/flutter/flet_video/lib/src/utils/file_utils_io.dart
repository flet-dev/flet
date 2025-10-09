import 'dart:io';

/// Only available on non‐web platforms.
/// Returns the file's contents if it exists, or null otherwise.
String? readFileAsStringIfExists(String path) {
  final file = File(path);
  if (file.existsSync()) return file.readAsStringSync();
  return null;
}
