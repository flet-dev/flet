import 'transport/data_channel.dart';
import 'transport/flet_backend_channel.dart';

/// An in-process `dart_bridge` transport allocated (on the Dart side) for one
/// embedded [FletApp].
///
/// `dart_bridge` channels are keyed by a Dart-allocated native port, so the port
/// must originate here and be handed to the Python side, which then serves it
/// with a `FletDartBridgeServer`. [port] is that native port; the embedded app's
/// backend talks over the channel via [channelBuilder] / [dataChannelFactory].
/// Call [dispose] when the embedded app is torn down.
class EmbeddedDartBridge {
  final int port;
  final FletBackendChannelBuilder channelBuilder;
  final DataChannelFactory dataChannelFactory;
  final void Function() dispose;

  EmbeddedDartBridge({
    required this.port,
    required this.channelBuilder,
    required this.dataChannelFactory,
    required this.dispose,
  });
}

/// Allocates an [EmbeddedDartBridge] for an embedded FletApp addressed as
/// `dartbridge://`.
///
/// Registered at startup by the build's `native_runtime.dart` (which owns
/// `serious_python`'s `PythonBridge`). Left null on web and on desktop/dev
/// builds where `dart_bridge` isn't available — there an embedded FletApp with a
/// `dartbridge://` url is expected to fall back to a socket URL instead.
typedef EmbeddedDartBridgeConnector = EmbeddedDartBridge Function();

/// Process-global hook; see [EmbeddedDartBridgeConnector].
EmbeddedDartBridgeConnector? embeddedDartBridgeConnector;
