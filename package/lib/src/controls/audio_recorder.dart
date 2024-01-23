import 'dart:async';

import 'package:flutter/widgets.dart';
import 'package:flutter_redux/flutter_redux.dart';
import 'package:record/record.dart';

import '../flet_server.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/page_args_model.dart';

class AudioRecorderControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final dynamic dispatch;
  final Widget? nextChild;

  const AudioRecorderControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.dispatch,
      required this.nextChild});

  @override
  State<AudioRecorderControl> createState() => _AudioRecorderControlState();
}

class _AudioRecorderControlState extends State<AudioRecorderControl> {
  AudioRecorder? record;
  FletServer? _server;

  @override
  void initState() {
    debugPrint("AudioRecorder.initState($hashCode)");
    record = widget.control.state["player"];
    if (record == null) {
      record = AudioRecorder();
      record = widget.control.state["player"] = record;
    }

    widget.control.onRemove.clear();
    widget.control.onRemove.add(_onRemove);
    super.initState();
  }

  void _onRemove() {
    debugPrint("AudioRecorder.remove($hashCode)");
    widget.control.state["player"]?.dispose();
    _server?.controlInvokeMethods.remove(widget.control.id);
  }

  @override
  void deactivate() {
    debugPrint("AudioRecorder.deactivate($hashCode)");
    super.deactivate();
  }

  Future<void> startRecording() async {
    debugPrint("AudioRecorder.startRecording($hashCode)");
    if (await record!.hasPermission()) {
      await record!.start(const RecordConfig(),
          path: '/Users/ndonkohenri/Desktop/myFile.m4a');
    }
  }

  Future<String?> stopRecording() async {
    debugPrint("AudioRecorder.stopRecording($hashCode)");
    final path = await record!.stop();
    debugPrint("AudioRecorder.stopRecording: $path");
    return path;
  }

  @override
  Widget build(BuildContext context) {
    debugPrint(
        "AudioRecorder build: ${widget.control.id} (${widget.control.hashCode})");

    startRecording();

    // TEST - wait for some seconds, then stop the recording
    Future.delayed(const Duration(seconds: 10));

    stopRecording();

    return StoreConnector<AppState, PageArgsModel>(
        distinct: true,
        converter: (store) => PageArgsModel.fromStore(store),
        builder: (context, pageArgs) {
          return const SizedBox.shrink();
        });
  }
}
