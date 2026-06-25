import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'controls/control_widget.dart';
import 'flet_app_errors_handler.dart';
import 'flet_backend.dart';
import 'flet_extension.dart';
import 'models/boot_status.dart';
import 'models/control.dart';
import 'testing/tester.dart';
import 'transport/data_channel.dart';
import 'transport/flet_backend_channel.dart';

/// FletApp - The top-level widget that initializes everything
class FletApp extends StatefulWidget {
  final String pageUrl;
  final String assetsDir;
  final String? bootScreenName;
  final Map<String, dynamic>? bootScreenOptions;
  /// Optional shared boot status notifier. When provided (e.g. by a persistent
  /// boot overlay in the app bootstrap), the backend updates it instead of
  /// owning its own, so the same notifier spans both boot phases.
  final ValueNotifier<BootStatus>? bootStatus;
  final String? appErrorMessage;
  final int? controlId;
  final String? title;
  final FletAppErrorsHandler? errorsHandler;
  final int? reconnectIntervalMs;
  final int? reconnectTimeoutMs;
  final List<FletExtension>? extensions;
  final Map<String, dynamic>? args;
  final bool? forcePyodide;
  final Tester? tester;
  final bool multiView;

  /// Optional escape hatch for embedders that bring their own transport
  /// (e.g. `serious_python`'s in-process FFI bridge). When set, this builder
  /// is invoked from [FletBackend.connect] in place of the URL-scheme
  /// factory; [pageUrl] is then irrelevant for transport selection.
  final FletBackendChannelBuilder? channelBuilder;

  /// Optional factory for high-throughput byte channels (see [DataChannel]).
  /// Embedders that ship an in-process Python runtime can inject a
  /// `PythonBridge`-backed factory here; when `null`, `FletBackend` falls
  /// back to a built-in factory that muxes raw bytes over the regular Flet
  /// protocol channel.
  final DataChannelFactory? dataChannelFactory;

  const FletApp(
      {super.key,
      required this.pageUrl,
      required this.assetsDir,
      this.bootScreenName,
      this.bootScreenOptions,
      this.bootStatus,
      this.appErrorMessage,
      this.controlId,
      this.title,
      this.errorsHandler,
      this.reconnectIntervalMs,
      this.reconnectTimeoutMs,
      this.extensions,
      this.args,
      this.forcePyodide,
      this.tester,
      this.multiView = false,
      this.channelBuilder,
      this.dataChannelFactory});

  @override
  State<FletApp> createState() => _FletAppState();
}

class _FletAppState extends State<FletApp> {
  FletBackend? backend;

  @override
  void deactivate() {
    backend?.dispose();
    super.deactivate();
  }

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider<FletBackend>(
      create: (context) {
        return FletBackend(
            bootScreenName: widget.bootScreenName ?? "flet",
            bootScreenOptions: widget.bootScreenOptions ?? const {},
            bootStatus: widget.bootStatus,
            appErrorMessage: widget.appErrorMessage,
            controlId: widget.controlId,
            reconnectIntervalMs: widget.reconnectIntervalMs,
            reconnectTimeoutMs: widget.reconnectTimeoutMs,
            pageUri: Uri.parse(widget.pageUrl),
            assetsDir: widget.assetsDir,
            errorsHandler: widget.errorsHandler,
            extensions: widget.extensions ?? [],
            args: widget.args,
            forcePyodide: widget.forcePyodide,
            tester: widget.tester,
            multiView: widget.multiView,
            channelBuilder: widget.channelBuilder,
            dataChannelFactory: widget.dataChannelFactory,
            parentFletBackend:
                Provider.of<FletBackend?>(context, listen: false));
      },
      child: Selector<FletBackend, Control>(
        selector: (_, backend) => backend.page,
        builder: (_, page, __) => ControlWidget(control: page),
      ),
    );
  }
}
