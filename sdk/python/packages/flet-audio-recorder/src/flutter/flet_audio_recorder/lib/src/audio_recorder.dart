import 'dart:async';

import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:record/record.dart';

import 'utils/audio_recorder.dart';

class AudioRecorderService extends FletService {
  AudioRecorderService({required super.control});

  AudioRecorder? recorder;
  StreamSubscription? _onStateChangedSubscription;

  @override
  void init() {
    super.init();
    debugPrint("AudioRecorder.init($hashCode)");
    control.addInvokeMethodListener(_invokeMethod);

    recorder = AudioRecorder();

    _onStateChangedSubscription = recorder!.onStateChanged().listen((state) {
      _onStateChanged.call(state);
    });
  }

  void _onStateChanged(RecordState state) {
    var stateMap = {
      RecordState.record: "recording",
      RecordState.pause: "paused",
      RecordState.stop: "stopped",
    };
    control.triggerEvent("state_change", stateMap[state]);
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("AudioRecorder.$name($args)");
    switch (name) {
      case "start_recording":
        final config = parseRecordConfig(args["configuration"]);
        if (config != null && await recorder!.hasPermission()) {
          final out = control.backend.getAssetSource(args["output_path"] ?? "");
          if (!isWebPlatform() && !out.isFile) {
            // on non-web/IO platforms, the output path must be a valid file path
            return false;
          }

          await recorder!.start(config, path: out.path);
          return true;
        }
        return false;
      case "stop_recording":
        return await recorder!.stop();
      case "cancel_recording":
        await recorder!.cancel();
      case "resume_recording":
        await recorder!.resume();
      case "pause_recording":
        await recorder!.pause();
      case "is_supported_encoder":
        var encoder = parseAudioEncoder(args["encoder"]);
        if (encoder != null) {
          return await recorder!.isEncoderSupported(encoder);
        }
        break;
      case "is_paused":
        return await recorder!.isPaused();
      case "is_recording":
        return await recorder!.isRecording();
      case "has_permission":
        return await recorder!.hasPermission();
      case "get_input_devices":
        List<InputDevice> devices = await recorder!.listInputDevices();
        return devices.asMap().map((k, v) {
          return MapEntry(v.id, v.label);
        });
      default:
        throw Exception("Unknown AudioRecorder method: $name");
    }
  }

  @override
  void dispose() {
    debugPrint("AudioRecorder(${control.id}).dispose()");
    _onStateChangedSubscription?.cancel();
    recorder?.dispose();
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }
}
