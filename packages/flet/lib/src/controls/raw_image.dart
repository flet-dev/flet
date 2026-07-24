import 'dart:async';
import 'dart:typed_data';
import 'dart:ui' as ui;

import 'package:flutter/material.dart';

import '../flet_backend.dart';
import '../models/control.dart';
import '../transport/data_channel.dart';
import '../utils/frame_stream.dart';
import '../utils/images.dart';
import '../utils/numbers.dart';
import 'base_controls.dart';

/// Display widget for pixel-frame streams pushed from Python.
///
/// Frames arrive over a dedicated [DataChannel] rather than the regular
/// Flet protocol, so the bytes skip MsgPack encode/decode. At most one
/// decoded [ui.Image] is alive at a time: each applied frame replaces the
/// previous one, which is disposed in a post-frame callback. That bound is
/// what keeps the widget safe on Flutter web (CanvasKit/WASM), where Dart
/// GC doesn't promptly reclaim native SkImage refs.
///
/// Wire format on the data channel (one opcode byte + payload):
///
///   [0x01][encoded bytes]                → decode (PNG/JPEG/WebP), replace
///   [0x03]                               → clear
///   [0x04][w u32 LE][h u32 LE][RGBA8888] → raw full frame (premultiplied)
///
/// After every applied frame the widget sends a 1-byte `[0xFF]` ack back
/// to Python — the producer awaits it, which is the backpressure that
/// paces `render()` loops to display speed.
///
/// While the browser tab is hidden the main-thread compositor is
/// suspended, but a Pyodide `render()` loop runs in a Web Worker that the
/// browser does *not* throttle. If frames kept being decoded and applied
/// they would pile up as undisposed [ui.Image]s and post-frame callbacks
/// that never run, and the whole backlog would flush into the engine on
/// resume — flooding it with per-frame exceptions. So while hidden the
/// widget stops decoding entirely: it coalesces to the most recent frame,
/// acks each one immediately (keeping the producer loop alive without a
/// backlog), and applies only that latest frame when the tab returns.
class RawImageControl extends StatefulWidget {
  final Control control;

  RawImageControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<RawImageControl> createState() => _RawImageControlState();
}

class _RawImageControlState extends State<RawImageControl>
    with FrameStreamVisibility<RawImageControl> {
  // Serialize concurrent frame applies so swaps happen in arrival order.
  Future<void>? _applyChain;

  DataChannel? _channel;
  StreamSubscription<Uint8List>? _channelSub;

  ui.Image? _image;

  // The most recent frame received while hidden (raw opcode + payload,
  // owned copy). Applied once when the tab becomes visible again; older
  // frames received while hidden are dropped. Null when nothing is
  // pending or the tab is visible.
  Uint8List? _deferredFrame;

  // 1-byte ack sent back to Python after each apply completes; the Python
  // side awaits it, giving `render()` its round-trip backpressure.
  static final Uint8List _frameAppliedAck = Uint8List.fromList([0xFF]);

  @override
  void onVisibilityRestored() {
    // Paint the latest frame that arrived while hidden (if any). It was
    // already acked on arrival, so apply it without acking again.
    final deferred = _deferredFrame;
    _deferredFrame = null;
    if (deferred != null) {
      _applyFrame(deferred, ack: false);
    }
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    // Open the data channel lazily on first dependency lookup — we need
    // BuildContext to reach FletBackend, which isn't available in initState.
    if (_channel != null) return;
    _channel = FletBackend.of(context).openDataChannel();
    _channelSub = _channel!.messages.listen(_onChannelFrame);
    // Announce the channel to Python via the standard convention event.
    widget.control.triggerEvent("data_channel_open", {
      "channel_name": "frames",
      "channel_id": _channel!.id,
    });
  }

  @override
  void dispose() {
    _channelSub?.cancel();
    _channelSub = null;
    _channel?.close();
    _channel = null;
    _image?.dispose();
    _image = null;
    super.dispose();
  }

  /// Inbound DataChannel frame. Applies it immediately when visible;
  /// while hidden, coalesces to the latest frame (see [_applyFrame] for
  /// the wire format).
  void _onChannelFrame(Uint8List bytes) {
    if (bytes.isEmpty) return;
    if (!visible) {
      // Tab hidden: the compositor is suspended, so decoding and applying
      // would build a backlog that floods the engine on resume. Drop any
      // earlier hidden frame, keep only this latest one to paint on
      // resume, and ack immediately so the producer loop stays alive.
      // Owned copy: the transport may reuse the inbound buffer before the
      // tab returns.
      _deferredFrame = Uint8List.fromList(bytes);
      _channel?.send(_frameAppliedAck);
      return;
    }
    _applyFrame(bytes, ack: true);
  }

  /// Decode and apply a frame. Wire format:
  ///   [0x01][encoded bytes]                → apply encoded (PNG/JPEG/WebP)
  ///   [0x03]                               → clear
  ///   [0x04][w u32 LE][h u32 LE][RGBA8888] → apply raw (premultiplied)
  ///
  /// When [ack] is true a `[0xFF]` frame-applied ack is sent once the apply
  /// completes. Frames deferred while hidden pass [ack] `false` because they
  /// were already acked on arrival.
  void _applyFrame(Uint8List bytes, {required bool ack}) {
    if (bytes.isEmpty) return;
    // Zero-copy slice of the same underlying buffer.
    final payload = Uint8List.sublistView(bytes, 1);
    switch (bytes[0]) {
      case 0x01:
        _enqueue(() => _applyEncoded(payload), ack: ack);
        break;
      case 0x03:
        _enqueue(_clear, ack: ack);
        break;
      case 0x04:
        _enqueue(() => _applyRaw(payload), ack: ack);
        break;
      default:
        debugPrint(
            "RawImage: unknown data-channel opcode 0x${bytes[0].toRadixString(16)}");
        // Ack anyway so a newer Python side never hangs its render loop
        // waiting on a frame this (older) client can't apply.
        if (ack) _channel?.send(_frameAppliedAck);
    }
  }

  void _enqueue(Future<void> Function() task, {required bool ack}) {
    final prev = _applyChain ?? Future.value();
    final next = prev.then((_) => task());
    _applyChain = next.catchError((_) {});
    if (ack) {
      next.whenComplete(() {
        _channel?.send(_frameAppliedAck);
      });
    }
  }

  Future<void> _applyEncoded(Uint8List bytes) async {
    if (bytes.isEmpty) {
      debugPrint("RawImage: skipping empty image bytes");
      return;
    }
    // Defensive copy; Safari's WASM runtime can free underlying buffers
    // across async boundaries and trigger "EncodingError: Loading error.".
    final owned = Uint8List.fromList(bytes);
    ui.Codec? codec;
    try {
      codec = await ui.instantiateImageCodec(owned, allowUpscaling: false);
      final frame = await codec.getNextFrame();
      _swapImage(frame.image);
    } catch (e) {
      debugPrint("RawImage: decode failed (${owned.length} bytes): $e");
    } finally {
      codec?.dispose();
    }
  }

  Future<void> _applyRaw(Uint8List payload) async {
    if (payload.length < 8) return;
    final bd = ByteData.sublistView(payload, 0, 8);
    final w = bd.getUint32(0, Endian.little);
    final h = bd.getUint32(4, Endian.little);
    if (w == 0 || h == 0 || payload.length - 8 != w * h * 4) {
      // Skip the frame; the ack still goes out via `_enqueueAndAck`, so
      // Python never stalls on a bad frame.
      debugPrint("RawImage: bad raw frame ${payload.length - 8} != $w*$h*4");
      return;
    }
    // Owned copy: the transport may reuse the inbound buffer, Safari's WASM
    // runtime can free views across async gaps, and decodeImageFromPixels
    // implementations may read from the underlying buffer after this call
    // returns.
    final pixels = Uint8List.fromList(Uint8List.sublistView(payload, 8));
    final completer = Completer<ui.Image>();
    ui.decodeImageFromPixels(
        pixels, w, h, ui.PixelFormat.rgba8888, completer.complete);
    _swapImage(await completer.future);
  }

  Future<void> _clear() async {
    _swapImage(null);
  }

  void _swapImage(ui.Image? newImage) {
    final old = _image;
    _image = newImage;
    if (mounted) setState(() {});
    if (old != null) {
      // Dispose after the frame that stops painting it.
      WidgetsBinding.instance.addPostFrameCallback((_) {
        old.dispose();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return LayoutControl(
      control: widget.control,
      child: RawImage(
        image: _image, // null before the first frame — paints nothing
        fit: widget.control.getBoxFit("fit"),
        filterQuality: widget.control
            .getFilterQuality("filter_quality", FilterQuality.low)!,
        scale: widget.control.getDouble("scale", 1.0)!,
      ),
    );
  }
}
