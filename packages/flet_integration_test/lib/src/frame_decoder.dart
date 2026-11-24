import 'dart:async';
import 'dart:typed_data';

/// Decodes a byte stream of length-prefixed frames into individual frame
/// payloads. Each frame is a big-endian uint32 length followed by that many
/// payload bytes. More robust than a newline delimiter — payloads may contain
/// arbitrary bytes (e.g. base64 screenshots) without escaping.
class FrameDecoder extends StreamTransformerBase<Uint8List, Uint8List> {
  final int maxFrameLength;

  const FrameDecoder({this.maxFrameLength = 64 * 1024 * 1024});

  /// Encodes [payload] as a length-prefixed frame.
  static Uint8List encode(List<int> payload) {
    final frame = Uint8List(4 + payload.length);
    ByteData.view(frame.buffer).setUint32(0, payload.length, Endian.big);
    frame.setRange(4, frame.length, payload);
    return frame;
  }

  @override
  Stream<Uint8List> bind(Stream<Uint8List> stream) {
    var buffer = Uint8List(0);
    late StreamController<Uint8List> controller;
    StreamSubscription<Uint8List>? subscription;

    void onChunk(Uint8List chunk) {
      final merged = Uint8List(buffer.length + chunk.length)
        ..setRange(0, buffer.length, buffer)
        ..setRange(buffer.length, buffer.length + chunk.length, chunk);
      buffer = merged;

      while (buffer.length >= 4) {
        final length =
            ByteData.sublistView(buffer, 0, 4).getUint32(0, Endian.big);
        if (length > maxFrameLength) {
          controller.addError(
            StateError("Frame length $length exceeds limit $maxFrameLength."),
          );
          subscription?.cancel();
          return;
        }
        if (buffer.length < 4 + length) break;
        controller.add(Uint8List.fromList(buffer.sublist(4, 4 + length)));
        buffer = Uint8List.fromList(buffer.sublist(4 + length));
      }
    }

    controller = StreamController<Uint8List>(
      onListen: () {
        subscription = stream.listen(
          onChunk,
          onError: controller.addError,
          onDone: controller.close,
          cancelOnError: false,
        );
      },
      onPause: () => subscription?.pause(),
      onResume: () => subscription?.resume(),
      onCancel: () => subscription?.cancel(),
    );

    return controller.stream;
  }
}
