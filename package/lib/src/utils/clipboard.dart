import 'package:flutter/services.dart';

Future setClipboard(String value) async {
  await Clipboard.setData(ClipboardData(text: value));
}

Future<String?> getClipboard() async {
  return (await Clipboard.getData(Clipboard.kTextPlain))?.text;
}
