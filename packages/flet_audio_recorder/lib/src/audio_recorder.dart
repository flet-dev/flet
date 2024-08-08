import 'dart:async';
import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:record/record.dart';

import 'utils/audio_recorder.dart';

class AudioRecorderControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final FletControlBackend backend;

  const AudioRecorderControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.backend});

  @override
  State<AudioRecorderControl> createState() => _AudioRecorderControlState();
}

class _AudioRecorderControlState extends State<AudioRecorderControl>
    with FletStoreMixin {
  AudioRecorder? recorder;
  void Function(RecordState)? _onStateChanged;
  StreamSubscription? _onStateChangedSubscription;

  @override
  void initState() {
    debugPrint("AudioRecorder.initState($hashCode)");
    recorder = widget.control.state["recorder"];
    if (recorder == null) {
      recorder = AudioRecorder();
      recorder = widget.control.state["recorder"] = recorder;
    }

    _onStateChangedSubscription = recorder?.onStateChanged().listen((state) {
      _onStateChanged?.call(state);
    });

    widget.control.onRemove.clear();
    widget.control.onRemove.add(_onRemove);
    super.initState();
  }

  void _onRemove() {
    debugPrint("AudioRecorder.remove($hashCode)");
    widget.control.state["recorder"]?.dispose();
    widget.backend.unsubscribeMethods(widget.control.id);
  }

  @override
  void deactivate() {
    debugPrint("AudioRecorder.deactivate($hashCode)");
    _onStateChangedSubscription?.cancel();
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

    _onStateChanged = (state) {
      debugPrint("AudioRecorder($hashCode) - state_changed: ${state.name}");
      var s = state.name.toString();
      if (s == "record") {
        s = "recording";
      } else if (s == "pause") {
        s = "paused";
      } else if (s == "stop") {
        s = "stopped";
      }
      widget.backend.triggerControlEvent(widget.control.id, "state_changed", s);
    };

    () async {
      widget.backend.subscribeMethods(widget.control.id,
          (methodName, args) async {
        switch (methodName) {
          case "start_recording":
            if (await recorder!.hasPermission()) {
              if (args["outputPath"] != null) {
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
                    path: args["outputPath"]!);
                return "true";
              }
              break;
            }
            return null;
          case "stop_recording":
            debugPrint("AudioRecorder.stopRecording($hashCode)");
            String? out = await recorder!.stop();
            return out;
          case "cancel_recording":
            debugPrint("AudioRecorder.cancelRecording($hashCode)");
            await recorder!.cancel();
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
            break;
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
      });
    }();

    return const SizedBox.shrink();
  }
}
