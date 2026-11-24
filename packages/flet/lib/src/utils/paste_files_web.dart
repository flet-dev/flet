import 'dart:js_interop';
import 'dart:typed_data';

import 'package:web/web.dart' as web;

/// A file pasted into the app (web: from the browser's `paste` event).
typedef PastedFile = ({String name, String mimeType, Uint8List bytes});

/// Listens to the browser's `paste` event and reports the pasted files
/// (a screenshot, an image copied from a page, files copied in the OS file
/// manager). The files arrive with the event itself, so no clipboard
/// permission is needed and it works in every browser, Safari included.
///
/// A paste that carries files is consumed: the browser would otherwise also
/// insert text for it (e.g. the file name) into the focused field. A paste
/// of text alone is left alone. Returns a function that stops listening.
void Function() listenPastedFiles(void Function(List<PastedFile>) onFiles) {
  final handler = ((web.Event event) {
    final data = (event as web.ClipboardEvent).clipboardData;
    final files = data?.files;
    if (files == null || files.length == 0) return;
    event.preventDefault();
    final list = [for (var i = 0; i < files.length; i++) files.item(i)!];
    Future.wait(list.map((f) async => (
          name: f.name,
          mimeType: f.type,
          bytes: (await f.arrayBuffer().toDart).toDart.asUint8List(),
        ))).then(onFiles);
  }).toJS;
  web.document.addEventListener("paste", handler);
  return () => web.document.removeEventListener("paste", handler);
}
