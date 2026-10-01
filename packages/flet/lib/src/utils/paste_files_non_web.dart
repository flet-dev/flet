import 'dart:typed_data';

/// A file pasted into the app.
typedef PastedFile = ({String name, String mimeType, Uint8List bytes});

/// Web only: native platforms have no paste event; TextField reads an
/// image from the clipboard on Ctrl/Cmd+V instead.
void Function() listenPastedFiles(void Function(List<PastedFile>) onFiles) {
  return () {};
}
