import 'dart:async';
import 'dart:convert';

import 'package:flutter/widgets.dart';
import 'package:record/record.dart';

import '../flet_app_services.dart';
import '../flet_server.dart';
import '../models/control.dart';
import '../utils/audio_recorder.dart';

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
  AudioRecorder? recorder;
  FletServer? _server;

  @override
  void initState() {
    debugPrint("AudioRecorder.initState($hashCode)");
    recorder = widget.control.state["player"];
    if (recorder == null) {
      recorder = AudioRecorder();
      recorder = widget.control.state["player"] = recorder;
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

  Future<String?> stopRecording() async {
    debugPrint("AudioRecorder.stopRecording($hashCode)");
    final path = await recorder!.stop();
    return path;
  }

  @override
  Widget build(BuildContext context) {
    debugPrint(
        "AudioRecorder build: ${widget.control.id} (${widget.control.hashCode})");

    int bitRate = widget.control.attrInt("bitRate", 128000)!;
    int sampleRate = widget.control.attrInt("sampleRate", 44100)!;
    int numChannels = widget.control.attrInt("channels", 2)!;
    bool autoGain = widget.control.attrBool("autoGain", false)!;
    bool cancelEcho = widget.control.attrBool("cancelEcho", false)!;
    bool suppressNoise = widget.control.attrBool("suppressNoise", false)!;
    AudioEncoder audioEncoder =
        parseAudioEncoder(widget.control.attrString("audioEncoder", "wav"))!;

    var server = FletAppServices.of(context).server;

    () async {
      _server = server;
      _server?.controlInvokeMethods[widget.control.id] =
          (methodName, args) async {
        switch (methodName) {
          case "start_recording":
            if (await recorder!.hasPermission()) {
              await recorder!.start(
                  RecordConfig(
                    encoder: audioEncoder,
                    bitRate: bitRate,
                    sampleRate: sampleRate,
                    numChannels: numChannels,
                    autoGain: autoGain,
                    echoCancel: cancelEcho,
                    noiseSuppress: suppressNoise,
                  ),
                  path: args["outputPath"] ??
                      ""); // FIX: a better default value just in case
            }
            break;
          case "stop_recording":
            debugPrint("AudioRecorder.stopRecording($hashCode)");
            return await recorder!.stop();
          case "resume_recording":
            debugPrint("AudioRecorder.resumeRecording($hashCode)");
            await recorder!.resume();
          case "pause_recording":
            debugPrint("AudioRecorder.pauseRecording($hashCode)");
            await recorder!.pause();
          case "is_supported_encoder":
            debugPrint("AudioRecorder.isEncoderSupported($hashCode)");
            if (parseAudioEncoder(args["encoder"]) != null) {
              bool isSupported = await recorder!.isEncoderSupported(
                  parseAudioEncoder(args["encoder"]) ?? AudioEncoder.wav);
              return isSupported.toString();
            }
            return null;
          case "is_paused":
            debugPrint("AudioRecorder.isPaused($hashCode)");
            bool isPaused = await recorder!.isPaused();
            return isPaused.toString();
          case "is_recording":
            debugPrint("AudioRecorder.isRecording($hashCode)");
            bool isRecording = await recorder!.isRecording();
            return isRecording.toString();
          case "has_permission":
            debugPrint("AudioRecorder.hasPermission($hashCode)");
            bool hasPermission = await recorder!.hasPermission();
            return hasPermission.toString();
          case "get_input_devices":
            debugPrint("AudioRecorder.getInputDevices($hashCode)");
            List<InputDevice> devices = await recorder!.listInputDevices();
            String devicesJson = json.encode(devices.asMap().map((key, value) {
              return MapEntry(key, (value.id, value.label));
            }).toString());
            return devicesJson;
        }
        return null;
      };
    }();

    return const SizedBox.shrink();
  }
}
