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

  // Subscription to the raw PCM audio stream produced by `recorder.startStream`.
  // Only active while a streaming recording (upload and/or Python-side stream)
  // is in progress; `null` for regular file-based recordings.
  StreamSubscription<Uint8List>? _recordStreamSubscription;

  // Holds the state of the current streaming recording (upload request,
  // bytes counter, completion signal). `null` when no streaming is active.
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
          // If either upload or stream is requested, switch to the
          // streaming code path (PCM chunks instead of file output).
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
        // For streaming recordings there is no output file to return; instead
        // we stop the recorder and wait for the audio stream's `onDone` handler
        // (`_finishStreamingRecording`) to flush and close the upload request.
        if (_streamSession != null) {
          await recorder!.stop();
          await _streamSession?.completed.future;
          return null;
        }
        return await recorder!.stop();
      case "cancel_recording":
        // Tear down any in-flight streaming session before cancelling the
        // recorder so partial uploads are aborted and listeners are notified.
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

  /// Starts a streaming recording.
  ///
  /// Depending on the arguments, the raw PCM chunks produced by the recorder
  /// are either:
  ///   * forwarded to a remote HTTP endpoint via a chunked `StreamedRequest`
  ///     (when [uploadArgs] is provided), and/or
  ///   * pushed to Python as "stream" events (when [stream] is `true`).
  ///
  /// Both sinks can be active at the same time. Returns `true` if the
  /// recorder successfully started streaming, `false` otherwise.
  Future<bool> _startStreamingRecording(
    RecordConfig config,
    Map<dynamic, dynamic>? uploadArgs,
    bool stream,
  ) async {
    // The `record` package only exposes a raw byte stream for PCM16; other
    // encoders don't have a portable streaming path, so we fail fast here.
    if (config.encoder != AudioEncoder.pcm16bits) {
      _sendUploadEvent(
        error: "Streaming recordings require PCM16BITS encoder.",
      );
      return false;
    }

    // Defensive cleanup: ensure no previous streaming session is lingering
    // before we start a new one (e.g. if the user restarts without stopping).
    await _recordStreamSubscription?.cancel();
    await _streamSession?.dispose();
    _recordStreamSubscription = null;
    _streamSession = null;

    final uploadConfig = uploadArgs != null
        ? _UploadConfig.fromMap(Map<String, dynamic>.from(uploadArgs))
        : null;

    // Build a chunked HTTP request up front. We don't call `.send()` yet — that
    // happens after the audio subscription is wired up so the first chunks are not lost.
    http.StreamedRequest? request;
    if (uploadConfig != null) {
      final uploadUrl =
          _getFullUploadUrl(control.backend.pageUri, uploadConfig.url);
      request = http.StreamedRequest(uploadConfig.method, Uri.parse(uploadUrl));
      if (uploadConfig.headers != null) {
        request.headers.addAll(uploadConfig.headers!);
      }
    }

    final session = _StreamingSession(
        stream: stream, uploadConfig: uploadConfig, request: request);
    _streamSession = session;

    try {
      final audioStream = await recorder!.startStream(config);

      // Emit an initial 0% progress event so listeners can show an upload
      // started state before any bytes are produced by the microphone.
      if (uploadConfig != null) {
        _sendUploadEvent(
            fileName: uploadConfig.fileName, progress: 0.0, bytesUploaded: 0);
      }

      _recordStreamSubscription = audioStream.listen(
        (chunk) {
          // For every audio chunk produced by the recorder: count it, feed
          // it to the HTTP upload sink (if any), and forward it to Python
          // (if a stream handler is subscribed).
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
          // The recorder stopped normally — finalize the upload and notify.
          await _finishStreamingRecording();
        },
        cancelOnError: true,
      );

      // Kick off the HTTP request now that the sink will receive chunks.
      session.startUpload();
      return true;
    } catch (error) {
      // Anything thrown while starting the stream (permissions, network,
      // recorder errors) is reported and the session is discarded.
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

  /// Finalizes a streaming recording after the audio stream's `onDone` fires.
  ///
  /// Closes the HTTP request sink, awaits the server response, and emits a
  /// final progress or error event to Python. Always resets the streaming
  /// state, even on failure, so a new recording can be started afterwards.
  Future<void> _finishStreamingRecording() async {
    final session = _streamSession;
    if (session == null) {
      return;
    }

    try {
      // Closing the sink signals the end of the chunked request body so the
      // server can finish processing and return a response.
      await session.request?.sink.close();
      final responseFuture = session.responseFuture;
      if (session.request != null && responseFuture != null) {
        final response = await responseFuture;
        // successful
        if (response.statusCode >= 200 && response.statusCode <= 204) {
          _sendUploadEvent(
            fileName: session.uploadConfig?.fileName,
            progress: 1.0,
            bytesUploaded: session.bytesSent,
          );
        } else {
          // not successful
          final body = await http.Response.fromStream(response);
          _sendUploadEvent(
            fileName: session.uploadConfig?.fileName,
            error:
                "Upload endpoint returned code ${response.statusCode}: ${body.body}",
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
      // Whatever happened, release the subscription and signal the
      // `stop_recording` awaiter that the session has fully wound down.
      session.complete();
      await _recordStreamSubscription?.cancel();
      _recordStreamSubscription = null;
      _streamSession = null;
    }
  }

  /// Aborts the current streaming recording.
  ///
  /// Called when the user cancels a recording or the audio stream emits an
  /// error. Closes the upload sink without waiting for a response, notifies
  /// Python with [error] (defaulting to "Recording cancelled"), and resets
  /// the streaming state.
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

  /// Fires the "upload" event on the Python-side control with the current
  /// upload progress or an error message. Any field may be null when not
  /// applicable (e.g. `progress` is null for per-chunk progress pings).
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

  /// Fires the "stream" event with a single PCM [chunk] and its monotonically
  /// increasing [sequence] number, allowing the Python side to reassemble the
  /// audio in order and detect gaps.
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

  /// Resolves a possibly-relative [uploadUrl] against the current [pageUri].
  ///
  /// If [uploadUrl] already contains an authority (scheme + host) it is used
  /// verbatim; otherwise its path/query are combined with the page's
  /// scheme/host/port so that relative upload endpoints work out of the box.
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

/// Value object describing where/how the streamed recording should be
/// uploaded. Built from the `upload` dict passed from Python on `start_recording`.
class _UploadConfig {
  const _UploadConfig({
    required this.url,
    required this.method,
    this.headers,
    this.fileName,
  });

  /// Parses the raw map received from Python.
  factory _UploadConfig.fromMap(Map<String, dynamic> value) {
    final headers = value["headers"];
    return _UploadConfig(
      url: value["upload_url"],
      method: (value["method"] ?? "PUT").toString().toUpperCase(),
      headers: headers != null ? Map<String, String>.from(headers) : null,
      fileName: value["file_name"],
    );
  }

  /// Destination URL — may be absolute or relative to the Flet page URI.
  final String url;

  /// HTTP method to use for the upload (e.g. `PUT` or `POST`).
  final String method;

  /// Optional request headers (e.g. auth, content-type).
  final Map<String, String>? headers;

  /// Optional file name echoed back in upload events so Python listeners
  /// can correlate progress updates with a specific recording.
  final String? fileName;
}

/// Bundles everything needed to track a single streaming recording:
///   * whether Python is listening to `stream` events,
///   * the upload config and HTTP request (if uploading),
///   * byte/sequence counters, and
///   * a `Completer` used by `stop_recording` to await clean shutdown.
class _StreamingSession {
  _StreamingSession({required this.stream, this.uploadConfig, this.request})
      : completed = Completer<void>();

  /// `true` when Python has a handler attached for the "stream" event.
  final bool stream;

  /// Upload target for this session, or `null` when only streaming to Python.
  final _UploadConfig? uploadConfig;

  /// Chunked HTTP request receiving the PCM bytes, or `null` when not uploading.
  final http.StreamedRequest? request;

  /// Resolves once the session has fully torn down (success, error, or
  /// cancellation). Awaited by `stop_recording` so callers can rely on the
  /// upload being flushed before the method returns.
  final Completer<void> completed;

  /// Future of the server response to the chunked upload. Populated by
  /// [startUpload] and awaited by `_finishStreamingRecording`.
  Future<http.StreamedResponse>? responseFuture;

  /// Total number of audio bytes produced so far — used for progress events
  /// and as the final uploaded-bytes count.
  int bytesSent = 0;

  /// Monotonic counter for stream events, incremented by [nextSequence].
  int _sequence = 0;

  /// Starts sending the chunked request. Must be called after the audio
  /// subscription has been attached so no chunks are dropped.
  void startUpload() {
    if (request != null) {
      responseFuture = request!.send();
    }
  }

  /// Returns the next sequence number for a "stream" event (starts at 1).
  int nextSequence() {
    _sequence += 1;
    return _sequence;
  }

  /// Marks the session as fully wound down. Safe to call multiple times.
  void complete() {
    if (!completed.isCompleted) {
      completed.complete();
    }
  }

  /// Best-effort cleanup used when the service itself is being disposed
  /// (e.g. the control is removed from the page mid-recording).
  Future<void> dispose() async {
    try {
      await request?.sink.close();
    } catch (_) {
      // Ignore sink shutdown errors during service disposal.
    }
    complete();
  }
}
