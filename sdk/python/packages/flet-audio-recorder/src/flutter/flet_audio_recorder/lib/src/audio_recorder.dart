import 'dart:async';
import 'dart:typed_data';

import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:http/http.dart' as http;
import 'package:record/record.dart';

import 'utils/audio_recorder.dart';

class AudioRecorderService extends FletService {
  AudioRecorderService({required super.control});

  AudioRecorder? recorder;
  StreamSubscription<RecordState>? _onStateChangedSubscription;
  StreamSubscription<Uint8List>? _recordStreamSubscription;
  _StreamingSession? _streamSession;

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
        final upload = args["upload"];
        final stream = control.hasEventHandler("stream");
        if (config != null && await recorder!.hasPermission()) {
          if (upload != null || stream) {
            return await _startStreamingRecording(config, upload, stream);
          }

          final out = control.backend.getAssetSource(args["output_path"] ?? "");
          if (!isWebPlatform() && !out.isFile) {
            // on non-web platforms, the output path must be a valid file path
            return false;
          }

          await recorder!.start(config, path: out.path);
          return true;
        }
        return false;
      case "stop_recording":
        if (_streamSession != null) {
          await recorder!.stop();
          await _streamSession?.completed.future;
          return null;
        }
        return await recorder!.stop();
      case "cancel_recording":
        if (_streamSession != null) {
          await _cancelStreamingRecording("Recording cancelled");
        }
        await recorder!.cancel();
        break;
      case "resume_recording":
        await recorder!.resume();
        break;
      case "pause_recording":
        await recorder!.pause();
        break;
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
    _recordStreamSubscription?.cancel();
    _streamSession?.dispose();
    recorder?.dispose();
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }

  Future<bool> _startStreamingRecording(
    RecordConfig config,
    Map<dynamic, dynamic>? uploadArgs,
    bool stream,
  ) async {
    if (config.encoder != AudioEncoder.pcm16bits) {
      _sendUploadEvent(
        error: "Streaming recordings require PCM16BITS encoder.",
      );
      return false;
    }

    await _recordStreamSubscription?.cancel();
    await _streamSession?.dispose();
    _recordStreamSubscription = null;
    _streamSession = null;

    final uploadConfig = uploadArgs != null
        ? _UploadConfig.fromMap(Map<String, dynamic>.from(uploadArgs))
        : null;

    http.StreamedRequest? request;
    if (uploadConfig != null) {
      final uploadUrl = _getFullUploadUrl(
        control.backend.pageUri,
        uploadConfig.url,
      );
      request = http.StreamedRequest(uploadConfig.method, Uri.parse(uploadUrl));
      if (uploadConfig.headers != null) {
        request.headers.addAll(uploadConfig.headers!);
      }
    }

    final session = _StreamingSession(
      stream: stream,
      uploadConfig: uploadConfig,
      request: request,
    );
    _streamSession = session;

    try {
      final audioStream = await recorder!.startStream(config);

      if (uploadConfig != null) {
        _sendUploadEvent(
          fileName: uploadConfig.fileName,
          progress: 0.0,
          bytesUploaded: 0,
        );
      }

      _recordStreamSubscription = audioStream.listen(
        (chunk) {
          session.bytesSent += chunk.length;
          session.request?.sink.add(chunk);

          if (session.request != null) {
            _sendUploadEvent(
              fileName: uploadConfig?.fileName,
              bytesUploaded: session.bytesSent,
            );
          }

          if (session.stream) {
            _sendStreamEvent(
              chunk,
              sequence: session.nextSequence(),
              bytesStreamed: session.bytesSent,
            );
          }
        },
        onError: (error) async {
          if (uploadConfig != null) {
            _sendUploadEvent(
              fileName: uploadConfig.fileName,
              error: error.toString(),
            );
          }
          await _cancelStreamingRecording();
        },
        onDone: () async {
          await _finishStreamingRecording();
        },
        cancelOnError: true,
      );

      session.startUpload();
      return true;
    } catch (error) {
      if (uploadConfig != null) {
        _sendUploadEvent(
          fileName: uploadConfig.fileName,
          error: error.toString(),
        );
      }
      session.complete();
      _streamSession = null;
      return false;
    }
  }

  Future<void> _finishStreamingRecording() async {
    final session = _streamSession;
    if (session == null) {
      return;
    }

    try {
      await session.request?.sink.close();
      final responseFuture = session.responseFuture;
      if (session.request != null && responseFuture != null) {
        final response = await responseFuture;
        if (response.statusCode < 200 || response.statusCode > 204) {
          final body = await http.Response.fromStream(response);
          _sendUploadEvent(
            fileName: session.uploadConfig?.fileName,
            error:
                "Upload endpoint returned code ${response.statusCode}: ${body.body}",
          );
        } else {
          _sendUploadEvent(
            fileName: session.uploadConfig?.fileName,
            progress: 1.0,
            bytesUploaded: session.bytesSent,
          );
        }
      }
    } catch (error) {
      if (session.uploadConfig != null) {
        _sendUploadEvent(
          fileName: session.uploadConfig?.fileName,
          error: error.toString(),
        );
      }
    } finally {
      session.complete();
      await _recordStreamSubscription?.cancel();
      _recordStreamSubscription = null;
      _streamSession = null;
    }
  }

  Future<void> _cancelStreamingRecording([String? error]) async {
    final session = _streamSession;
    if (session == null) {
      return;
    }

    try {
      await _recordStreamSubscription?.cancel();
      _recordStreamSubscription = null;
      await session.request?.sink.close();
      if (session.uploadConfig != null) {
        _sendUploadEvent(
          fileName: session.uploadConfig?.fileName,
          error: error ?? "Recording cancelled",
        );
      }
    } finally {
      session.complete();
      _streamSession = null;
    }
  }

  void _sendUploadEvent({
    String? fileName,
    double? progress,
    int? bytesUploaded,
    String? error,
  }) {
    control.triggerEvent("upload", {
      "file_name": fileName,
      "progress": progress,
      "bytes_uploaded": bytesUploaded,
      "error": error,
    });
  }

  void _sendStreamEvent(
    Uint8List chunk, {
    required int sequence,
    required int bytesStreamed,
  }) {
    control.triggerEvent("stream", {
      "chunk": chunk,
      "sequence": sequence,
      "bytes_streamed": bytesStreamed,
    });
  }

  String _getFullUploadUrl(Uri pageUri, String uploadUrl) {
    final uploadUri = Uri.parse(uploadUrl);
    if (uploadUri.hasAuthority) {
      return uploadUrl;
    }
    return Uri(
      scheme: pageUri.scheme,
      host: pageUri.host,
      port: pageUri.port,
      path: uploadUri.path,
      query: uploadUri.query,
    ).toString();
  }
}

class _UploadConfig {
  const _UploadConfig({
    required this.url,
    required this.method,
    this.headers,
    this.fileName,
  });

  factory _UploadConfig.fromMap(Map<String, dynamic> value) {
    final headers = value["headers"];
    return _UploadConfig(
      url: value["upload_url"],
      method: (value["method"] ?? "PUT").toString().toUpperCase(),
      headers: headers != null ? Map<String, String>.from(headers) : null,
      fileName: value["file_name"],
    );
  }

  final String url;
  final String method;
  final Map<String, String>? headers;
  final String? fileName;
}

class _StreamingSession {
  _StreamingSession({required this.stream, this.uploadConfig, this.request})
    : completed = Completer<void>();

  final bool stream;
  final _UploadConfig? uploadConfig;
  final http.StreamedRequest? request;
  final Completer<void> completed;
  Future<http.StreamedResponse>? responseFuture;
  int bytesSent = 0;
  int _sequence = 0;

  void startUpload() {
    if (request != null) {
      responseFuture = request!.send();
    }
  }

  int nextSequence() {
    _sequence += 1;
    return _sequence;
  }

  void complete() {
    if (!completed.isCompleted) {
      completed.complete();
    }
  }

  Future<void> dispose() async {
    try {
      await request?.sink.close();
    } catch (_) {
      // Ignore sink shutdown errors during service disposal.
    }
    complete();
  }
}
