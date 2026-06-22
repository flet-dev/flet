import 'dart:typed_data';

/// One bidirectional byte channel between Dart and Python, dedicated to a
/// single widget's bulk-data traffic.
///
/// The Dart side of an extension widget opens one via
/// [FletBackend.openDataChannel] in `initState`, then announces it to Python
/// by firing a `data_channel_open` control event carrying
/// `{channel_name, channel_id: id}` — Python's handler retrieves the
/// matching `DataChannel` via `Control.get_data_channel(channel_id)`.
///
/// Bytes flow over a transport chosen by the active [DataChannelFactory]:
/// a dedicated `PythonBridge` per channel in embedded native mode, or a
/// raw-byte frame muxed over the regular Flet protocol transport in dev /
/// web modes (see `ProtocolMuxedDataChannelFactory`).
///
/// **Isolate scope.** [FletBackend.openDataChannel] runs on the main Isolate
/// (it goes through `FletBackend.of(BuildContext)`). The returned channel —
/// and, in embedded mode, the backing `PythonBridge` — therefore lives on
/// the main Isolate. For per-Isolate bridges in worker Isolates, construct
/// `PythonBridge` directly from `package:serious_python` and send the port
/// back to the main Isolate via `SendPort` for the `data_channel_open`
/// fire.
abstract class DataChannel {
  /// Stable identifier carried in the `data_channel_open` event payload so
  /// Python can attach to the same channel. Implementation-specific: for
  /// the `PythonBridge`-backed factory this is the Dart native port number,
  /// for the muxed fallback it is a monotonic u32 minted by the factory.
  int get id;

  /// Bytes pushed from Python via this channel. Hot path — consumers should
  /// avoid synchronous heavy work in the listener and instead enqueue to a
  /// worker.
  Stream<Uint8List> get messages;

  /// Send bytes Dart → Python. Returns `false` only during the brief startup
  /// window before the Python side has attached (embedded mode); widget
  /// code should treat this as transient and retry / queue accordingly.
  bool send(Uint8List bytes);

  /// Releases the channel. Must be called from the widget's `dispose()`.
  /// Idempotent.
  void close();
}

/// Factory injected by the embedder. The `flet build` template injects a
/// `PythonBridge`-backed factory for native mode; web / dev / Pyodide
/// deployments leave this `null` and `FletBackend` falls back to the
/// built-in `ProtocolMuxedDataChannelFactory` that rides the existing
/// Flet protocol transport.
abstract class DataChannelFactory {
  /// Opens a fresh data channel. Each call mints a new id; a control may
  /// open as many channels as it needs.
  DataChannel open();
}
