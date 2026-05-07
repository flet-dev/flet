import 'dart:async';
import 'dart:typed_data';
import 'dart:ui' as ui;

import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart';

/// Display widget for matplotlib WebAgg-style image streams.
///
/// Two rendering strategies, picked at runtime by platform:
///
/// - **GPU + flatten** (native): keeps an `_backdrop` plus a list of pending
///   diff `ui.Image`s, paints all of them per frame, and bakes them into a
///   fresh backdrop via `Picture.toImage` every [_GpuMatplotlibChartCanvasState._flattenInterval]
///   diffs. Fast (no GPU↔CPU readback) and memory-stable on native runtimes
///   where Dart GC is aggressive enough to reclaim layer-held SkImage refs.
///
/// - **CPU composite** (web): decodes each PNG to RGBA bytes, composites
///   onto a single backbuffer in Dart, and uploads ONE fresh `ui.Image` per
///   frame. Slower per frame, but holds at most one `ui.Image` at a time so
///   layer-ref accumulation stays bounded under Flutter web (CanvasKit/WASM)
///   where Dart GC doesn't promptly reclaim native SkImage refs.
class MatplotlibChartCanvasControl extends StatefulWidget {
  final Control control;

  MatplotlibChartCanvasControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  // ignore: no_logic_in_create_state
  State<MatplotlibChartCanvasControl> createState() => kIsWeb
      ? _CpuMatplotlibChartCanvasState()
      : _GpuMatplotlibChartCanvasState();
}

// ---------------------------------------------------------------------------
// Shared helpers
// ---------------------------------------------------------------------------

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

abstract class _MatplotlibChartCanvasStateBase
    extends State<MatplotlibChartCanvasControl> {
  // Serialize concurrent apply_full / apply_diff calls so backdrop mutations
  // happen in arrival order.
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
    disposeResources();
    super.dispose();
  }

  /// Subclass hook — release any held `ui.Image`s / backbuffers.
  void disposeResources();

  Future<void> applyFull(Uint8List bytes);
  Future<void> applyDiff(Uint8List bytes);
  Future<void> clearAll();
  CustomPainter buildPainter();

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    switch (name) {
      case "apply_full":
        await _enqueue(() => applyFull(_extractBytes(args)));
        return;
      case "apply_diff":
        await _enqueue(() => applyDiff(_extractBytes(args)));
        return;
      case "clear":
        await _enqueue(clearAll);
        return;
      default:
        throw Exception("Unknown MatplotlibChartCanvas method: $name");
    }
  }

  Future<void> _enqueue(Future<void> Function() task) {
    final prev = _applyChain ?? Future.value();
    final next = prev.then((_) => task());
    _applyChain = next.catchError((_) {});
    return next;
  }

  void _maybeReportResize(Size size) {
    final resizeInterval = widget.control.getInt("resize_interval", 10)!;
    final now = DateTime.now().millisecondsSinceEpoch;
    if ((now - _lastResize > resizeInterval && _lastSize != size) ||
        _lastSize.isEmpty) {
      _lastSize = size;
      _lastResize = now;
      widget.control
          .triggerEvent("resize", {"w": size.width, "h": size.height});
    }
  }

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        WidgetsBinding.instance.addPostFrameCallback((_) {
          if (!mounted) return;
          _maybeReportResize(constraints.biggest);
        });
        return CustomPaint(
          size: constraints.biggest,
          painter: buildPainter(),
        );
      },
    );
  }
}

/// Decodes PNG bytes to a [ui.Image], staying GPU-resident.
Future<ui.Image?> _decodeImage(Uint8List bytes) async {
  if (bytes.isEmpty) {
    debugPrint("MatplotlibChartCanvas: skipping empty image bytes");
    return null;
  }
  // Defensive copy; Safari's WASM runtime can free underlying buffers across
  // async boundaries and trigger "EncodingError: Loading error.".
  final owned = Uint8List.fromList(bytes);
  ui.Codec? codec;
  try {
    codec = await ui.instantiateImageCodec(owned, allowUpscaling: false);
    final frame = await codec.getNextFrame();
    return frame.image;
  } catch (e) {
    debugPrint(
        "MatplotlibChartCanvas: decode failed (${owned.length} bytes): $e");
    rethrow;
  } finally {
    codec?.dispose();
  }
}

// ---------------------------------------------------------------------------
// GPU + flatten strategy (native runtimes)
// ---------------------------------------------------------------------------

class _GpuMatplotlibChartCanvasState
    extends _MatplotlibChartCanvasStateBase {
  // Number of diffs to accumulate before flattening into a fresh backdrop.
  // Larger = fewer Picture.toImage calls; smaller = lower transient memory.
  static const int _flattenInterval = 10;

  ui.Image? _backdrop;
  final List<ui.Image> _diffs = [];

  @override
  void disposeResources() {
    _backdrop?.dispose();
    _backdrop = null;
    for (final img in _diffs) {
      img.dispose();
    }
    _diffs.clear();
  }

  @override
  Future<void> applyFull(Uint8List bytes) async {
    final image = await _decodeImage(bytes);
    if (image == null) return;
    _replaceBackdrop(image);
    _disposeDiffs();
    if (mounted) setState(() {});
  }

  @override
  Future<void> applyDiff(Uint8List bytes) async {
    if (_backdrop == null) {
      // No baseline yet — first frame must be a full.
      await applyFull(bytes);
      return;
    }
    final image = await _decodeImage(bytes);
    if (image == null) return;
    _diffs.add(image);
    if (_diffs.length >= _flattenInterval) {
      await _flatten();
    }
    if (mounted) setState(() {});
  }

  @override
  Future<void> clearAll() async {
    _replaceBackdrop(null);
    _disposeDiffs();
    if (mounted) setState(() {});
  }

  /// Bakes [_backdrop] + pending [_diffs] into a single new backdrop via
  /// `Picture.toImage`, replaces [_backdrop], and drops the diffs.
  Future<void> _flatten() async {
    final backdrop = _backdrop;
    if (backdrop == null || _diffs.isEmpty) return;

    final w = backdrop.width;
    final h = backdrop.height;

    final recorder = ui.PictureRecorder();
    final canvas = Canvas(recorder);
    final paint = Paint();
    canvas.drawImage(backdrop, Offset.zero, paint);
    for (final diff in _diffs) {
      canvas.drawImage(diff, Offset.zero, paint);
    }

    final picture = recorder.endRecording();
    final ui.Image newBackdrop;
    try {
      newBackdrop = await picture.toImage(w, h);
    } finally {
      picture.dispose();
    }

    _replaceBackdrop(newBackdrop);
    _disposeDiffs();
  }

  void _replaceBackdrop(ui.Image? image) {
    final old = _backdrop;
    _backdrop = image;
    if (old != null) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        old.dispose();
      });
    }
  }

  void _disposeDiffs() {
    if (_diffs.isEmpty) return;
    final old = List<ui.Image>.of(_diffs);
    _diffs.clear();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      for (final img in old) {
        img.dispose();
      }
    });
  }

  @override
  CustomPainter buildPainter() => _GpuMatplotlibImagePainter(
        backdrop: _backdrop,
        diffs: List<ui.Image>.unmodifiable(_diffs),
      );
}

class _GpuMatplotlibImagePainter extends CustomPainter {
  final ui.Image? backdrop;
  final List<ui.Image> diffs;

  const _GpuMatplotlibImagePainter({
    required this.backdrop,
    required this.diffs,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final bg = backdrop;
    if (bg == null) return;
    final dst = Rect.fromLTWH(0, 0, size.width, size.height);
    final paint = Paint();
    final bgSrc =
        Rect.fromLTWH(0, 0, bg.width.toDouble(), bg.height.toDouble());
    canvas.drawImageRect(bg, bgSrc, dst, paint);
    for (final diff in diffs) {
      final src =
          Rect.fromLTWH(0, 0, diff.width.toDouble(), diff.height.toDouble());
      canvas.drawImageRect(diff, src, dst, paint);
    }
  }

  @override
  bool shouldRepaint(_GpuMatplotlibImagePainter old) {
    return backdrop != old.backdrop || diffs.length != old.diffs.length;
  }
}

// ---------------------------------------------------------------------------
// CPU composite strategy (web — CanvasKit/WASM)
// ---------------------------------------------------------------------------

class _CpuMatplotlibChartCanvasState
    extends _MatplotlibChartCanvasStateBase {
  ui.Image? _displayImage;
  Uint8List? _backbuffer;
  int _bbWidth = 0;
  int _bbHeight = 0;

  @override
  void disposeResources() {
    _displayImage?.dispose();
    _displayImage = null;
    _backbuffer = null;
  }

  @override
  Future<void> applyFull(Uint8List bytes) async {
    final decoded = await _decodeRgba(bytes);
    if (decoded == null) return;

    _backbuffer = decoded.bytes;
    _bbWidth = decoded.width;
    _bbHeight = decoded.height;

    final image = await _makeImage(decoded.bytes, decoded.width, decoded.height);
    _swapDisplay(image);
  }

  @override
  Future<void> applyDiff(Uint8List bytes) async {
    if (_backbuffer == null) {
      // No baseline yet — treat as full.
      await applyFull(bytes);
      return;
    }

    final decoded = await _decodeRgba(bytes);
    if (decoded == null) return;

    // Promote to a full replace if the frame size changed.
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

  @override
  Future<void> clearAll() async {
    final old = _displayImage;
    _displayImage = null;
    _backbuffer = null;
    _bbWidth = 0;
    _bbHeight = 0;
    if (old != null) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        old.dispose();
      });
    }
    if (mounted) setState(() {});
  }

  Future<_DecodedRgba?> _decodeRgba(Uint8List bytes) async {
    final img = await _decodeImage(bytes);
    if (img == null) return null;
    try {
      final byteData =
          await img.toByteData(format: ui.ImageByteFormat.rawRgba);
      if (byteData == null) return null;
      return _DecodedRgba(
        bytes: byteData.buffer.asUint8List(),
        width: img.width,
        height: img.height,
      );
    } finally {
      img.dispose();
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
      WidgetsBinding.instance.addPostFrameCallback((_) {
        old.dispose();
      });
    }
  }

  @override
  CustomPainter buildPainter() =>
      _CpuMatplotlibImagePainter(image: _displayImage);
}

class _DecodedRgba {
  final Uint8List bytes;
  final int width;
  final int height;
  _DecodedRgba(
      {required this.bytes, required this.width, required this.height});
}

class _CpuMatplotlibImagePainter extends CustomPainter {
  final ui.Image? image;

  const _CpuMatplotlibImagePainter({required this.image});

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
  bool shouldRepaint(_CpuMatplotlibImagePainter old) => old.image != image;
}
