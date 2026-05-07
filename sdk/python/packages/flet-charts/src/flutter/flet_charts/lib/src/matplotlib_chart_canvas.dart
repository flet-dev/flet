import 'dart:async';
import 'dart:typed_data';
import 'dart:ui' as ui;

import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

/// Display widget for matplotlib WebAgg-style image streams.
///
/// Receives full and incremental "diff" PNG frames via control method calls
/// and composites them in CPU memory. Holds at most one [ui.Image] for
/// display at a time, replacing it on each apply. This avoids the per-frame
/// `Picture.toImage` allocations that the generic Canvas+capture path uses,
/// which on Flutter web (CanvasKit/WASM) accumulate and are not promptly
/// reclaimed by the JS GC during animations.
class MatplotlibChartCanvasControl extends StatefulWidget {
  final Control control;

  MatplotlibChartCanvasControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<MatplotlibChartCanvasControl> createState() =>
      _MatplotlibChartCanvasState();
}

class _MatplotlibChartCanvasState extends State<MatplotlibChartCanvasControl> {
  ui.Image? _displayImage;
  Uint8List? _backbuffer;
  int _bbWidth = 0;
  int _bbHeight = 0;

  // Serialize concurrent apply_full / apply_diff calls. Each invocation
  // awaits the previous one so the backbuffer mutations happen in order.
  Future<void>? _applyChain;

  Size _lastSize = Size.zero;
  int _lastResize = DateTime.now().millisecondsSinceEpoch;

  @override
  void initState() {
    super.initState();
    widget.control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void dispose() {
    widget.control.removeInvokeMethodListener(_invokeMethod);
    _displayImage?.dispose();
    _displayImage = null;
    _backbuffer = null;
    super.dispose();
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    switch (name) {
      case "apply_full":
        await _enqueue(() => _applyFull(_extractBytes(args)));
        return;
      case "apply_diff":
        await _enqueue(() => _applyDiff(_extractBytes(args)));
        return;
      case "clear":
        await _enqueue(() async {
          _disposeDisplay();
          _backbuffer = null;
          _bbWidth = 0;
          _bbHeight = 0;
          if (mounted) setState(() {});
        });
        return;
      default:
        throw Exception("Unknown MatplotlibChartCanvas method: $name");
    }
  }

  Uint8List _extractBytes(dynamic args) {
    final v = args is Map ? args["bytes"] : args;
    if (v is Uint8List) return v;
    if (v is ByteData) {
      return v.buffer.asUint8List(v.offsetInBytes, v.lengthInBytes);
    }
    if (v is List<int>) return Uint8List.fromList(v);
    if (v is List && v.every((e) => e is int)) {
      return Uint8List.fromList(v.cast<int>());
    }
    throw ArgumentError("Expected bytes for image data, got ${v.runtimeType}");
  }

  // Chains apply operations so they run sequentially. Without this,
  // overlapping awaits could let a later diff be composited before an
  // earlier full frame finished decoding, producing tearing.
  Future<void> _enqueue(Future<void> Function() task) {
    final prev = _applyChain ?? Future.value();
    final next = prev.then((_) => task());
    _applyChain = next.catchError((_) {});
    return next;
  }

  Future<void> _applyFull(Uint8List bytes) async {
    final decoded = await _decodeRgba(bytes);
    if (decoded == null) return;

    _backbuffer = decoded.bytes;
    _bbWidth = decoded.width;
    _bbHeight = decoded.height;

    final image = await _makeImage(decoded.bytes, decoded.width, decoded.height);
    _swapDisplay(image);
  }

  Future<void> _applyDiff(Uint8List bytes) async {
    if (_backbuffer == null) {
      // No baseline yet — treat as full so we don't render a transparent
      // diff with no underlying frame.
      await _applyFull(bytes);
      return;
    }

    final decoded = await _decodeRgba(bytes);
    if (decoded == null) return;

    // Diffs from matplotlib are sized to the figure buffer. If the frame
    // size has changed since the last full frame (e.g. resize race),
    // promote to a full replace.
    if (decoded.width != _bbWidth ||
        decoded.height != _bbHeight ||
        decoded.bytes.length != _backbuffer!.length) {
      _backbuffer = decoded.bytes;
      _bbWidth = decoded.width;
      _bbHeight = decoded.height;
      final image =
          await _makeImage(decoded.bytes, decoded.width, decoded.height);
      _swapDisplay(image);
      return;
    }

    // Composite: matplotlib's diff PNG has alpha=0 for unchanged pixels.
    // Where alpha != 0, copy the new pixel into the backbuffer.
    final bb = _backbuffer!.buffer.asUint32List();
    final df = decoded.bytes.buffer.asUint32List();
    for (int i = 0; i < df.length; i++) {
      // RGBA8888 on little-endian: alpha is the highest byte (0xFF000000).
      if ((df[i] & 0xFF000000) != 0) {
        bb[i] = df[i];
      }
    }

    final image = await _makeImage(_backbuffer!, _bbWidth, _bbHeight);
    _swapDisplay(image);
  }

  Future<_DecodedRgba?> _decodeRgba(Uint8List bytes) async {
    if (bytes.isEmpty) {
      debugPrint("MatplotlibChartCanvas: skipping empty image bytes");
      return null;
    }
    // Take a defensive copy. msgpack_dart sometimes hands us a Uint8List
    // backed by a buffer that's reused/freed by Safari's WASM runtime,
    // causing CanvasKit's async decoder to throw "EncodingError: Loading
    // error." after the original buffer is gone.
    final owned = Uint8List.fromList(bytes);
    ui.Codec? codec;
    ui.Image? img;
    try {
      codec = await ui.instantiateImageCodec(owned, allowUpscaling: false);
      final frame = await codec.getNextFrame();
      img = frame.image;
      final byteData =
          await img.toByteData(format: ui.ImageByteFormat.rawRgba);
      if (byteData == null) return null;
      return _DecodedRgba(
        bytes: byteData.buffer.asUint8List(),
        width: img.width,
        height: img.height,
      );
    } catch (e) {
      debugPrint(
          "MatplotlibChartCanvas: decode failed (${owned.length} bytes): $e");
      rethrow;
    } finally {
      img?.dispose();
      codec?.dispose();
    }
  }

  Future<ui.Image> _makeImage(Uint8List rgba, int width, int height) {
    final completer = Completer<ui.Image>();
    ui.decodeImageFromPixels(
      rgba,
      width,
      height,
      ui.PixelFormat.rgba8888,
      completer.complete,
    );
    return completer.future;
  }

  void _swapDisplay(ui.Image newImage) {
    final old = _displayImage;
    _displayImage = newImage;
    if (mounted) setState(() {});
    if (old != null) {
      // Defer disposal to the next frame so any in-flight paint that still
      // references the old image completes first.
      WidgetsBinding.instance.addPostFrameCallback((_) {
        old.dispose();
      });
    }
  }

  void _disposeDisplay() {
    final old = _displayImage;
    _displayImage = null;
    if (old != null) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        old.dispose();
      });
    }
  }

  void _maybeReportResize(Size size) {
    final resizeInterval = widget.control.getInt("resize_interval", 10)!;
    final now = DateTime.now().millisecondsSinceEpoch;
    if ((now - _lastResize > resizeInterval && _lastSize != size) ||
        _lastSize.isEmpty) {
      _lastSize = size;
      _lastResize = now;
      widget.control.triggerEvent("resize", {"w": size.width, "h": size.height});
    }
  }

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        // Fire on_resize on layout. matplotlib uses this to know the target
        // figure size.
        WidgetsBinding.instance.addPostFrameCallback((_) {
          if (!mounted) return;
          _maybeReportResize(constraints.biggest);
        });
        return CustomPaint(
          size: constraints.biggest,
          painter: _MatplotlibImagePainter(_displayImage),
        );
      },
    );
  }
}

class _DecodedRgba {
  final Uint8List bytes;
  final int width;
  final int height;
  _DecodedRgba({required this.bytes, required this.width, required this.height});
}

class _MatplotlibImagePainter extends CustomPainter {
  final ui.Image? image;

  _MatplotlibImagePainter(this.image);

  @override
  void paint(Canvas canvas, Size size) {
    final img = image;
    if (img == null) return;
    final src =
        Rect.fromLTWH(0, 0, img.width.toDouble(), img.height.toDouble());
    final dst = Rect.fromLTWH(0, 0, size.width, size.height);
    canvas.drawImageRect(img, src, dst, Paint());
  }

  @override
  bool shouldRepaint(_MatplotlibImagePainter old) => old.image != image;
}
