import 'package:flutter/services.dart';

void setClipboard(String data) async {
  await Clipboard.setData(ClipboardData(text: data));
}

Future<String?> getClipboard() async {
  var data = await Clipboard.getData(Clipboard.kTextPlain);
  return data?.text;
}
