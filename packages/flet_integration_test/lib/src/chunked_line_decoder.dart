import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';

/// Stream transformer which decodes UTF-8 bytes into newline-delimited strings
/// while enforcing a maximum line length.
class ChunkedLineDecoder extends StreamTransformerBase<Uint8List, String> {
  final int maxLineLength;

  const ChunkedLineDecoder({this.maxLineLength = 16 * 1024 * 1024});

  @override
  Stream<String> bind(Stream<Uint8List> stream) {
    final stringStream = stream.cast<List<int>>().transform(utf8.decoder);
    late StreamSubscription<String> subscription;
    late StreamController<String> controller;
    var pending = "";

    void emitLine(String line) {
      if (line.length > maxLineLength) {
        throw StateError(
          "Line length exceeds allowed limit of $maxLineLength characters.",
        );
      }
      controller.add(line);
    }

    controller = StreamController<String>(
      onListen: () {
        subscription = stringStream.listen(
          (chunk) {
            pending += chunk;
            while (true) {
              final newlineIndex = pending.indexOf('\n');
              if (newlineIndex == -1) {
                if (pending.length > maxLineLength) {
                  controller.addError(StateError(
                    "Line length exceeds allowed limit of $maxLineLength characters.",
                  ));
                  subscription.cancel();
                }
                break;
              }
              final line = pending.substring(0, newlineIndex);
              emitLine(line);
              pending = pending.substring(newlineIndex + 1);
            }
          },
          onError: controller.addError,
          onDone: () {
            if (pending.isNotEmpty) {
              if (pending.length > maxLineLength) {
                controller.addError(StateError(
                  "Line length exceeds allowed limit of $maxLineLength characters.",
                ));
              } else {
                controller.add(pending);
              }
            }
            controller.close();
          },
          cancelOnError: false,
        );
      },
      onPause: () => subscription.pause(),
      onResume: () => subscription.resume(),
      onCancel: () => subscription.cancel(),
    );

    return controller.stream;
  }
}
