import 'dart:async';
import 'dart:typed_data';

import 'package:camera/camera.dart';
import 'package:flet/flet.dart';
// ignore: implementation_imports
import 'package:flet/src/controls/control_widget.dart';
import 'package:flutter/material.dart';

import 'utils/camera.dart';

class CameraControl extends StatefulWidget {
  final Control control;

  const CameraControl({super.key, required this.control});

  @override
  State<CameraControl> createState() => _CameraControlState();
}

class _CameraControlState extends State<CameraControl> {
  CameraController? _controller;
  bool _previewEnabled = true;
  bool _processingImage = false;

  @override
  void initState() {
    super.initState();
    _previewEnabled = widget.control.getBool("preview_enabled", true)!;
    widget.control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void didUpdateWidget(covariant CameraControl oldWidget) {
    super.didUpdateWidget(oldWidget);
    final enabled = widget.control.getBool("preview_enabled", true)!;
    if (enabled != _previewEnabled) {
      setState(() => _previewEnabled = enabled);
    }
  }

  @override
  void dispose() {
    widget.control.removeInvokeMethodListener(_invokeMethod);
    _processingImage = false;
    _detachController();
    super.dispose();
  }

  void _attachController(CameraController controller) {
    _detachController();
    _controller = controller;
    controller.addListener(_onControllerValueChanged);
  }

  void _detachController() {
    final controller = _controller;
    if (controller != null) {
      controller.removeListener(_onControllerValueChanged);
      controller.dispose();
    }
    _controller = null;
  }

  void _onControllerValueChanged() {
    final controller = _controller;
    if (controller == null) {
      return;
    }
    if (widget.control.getBool("on_state_change", false)!) {
      widget.control
          .triggerEvent("state_change", cameraValueToMap(controller.value));
    }
    if (mounted) {
      setState(() {});
    }
  }

  CameraController _requireController() {
    final controller = _controller;
    if (controller == null) {
      throw Exception("Camera is not initialized. Call initialize() first.");
    }
    return controller;
  }

  Future<Map<String, dynamic>> _initializeController(
      Map<dynamic, dynamic> args) async {
    final description = parseCameraDescription(args["description"]);
    if (description == null) {
      throw Exception("Camera description is required for initialization.");
    }

    final resolutionPreset =
        parseResolutionPreset(args["resolution_preset"], ResolutionPreset.max);
    final enableAudio =
        args["enable_audio"] is bool ? args["enable_audio"] as bool : true;
    final fps = args["fps"] is num ? (args["fps"] as num).round() : null;
    final videoBitrate = args["video_bitrate"] is num
        ? (args["video_bitrate"] as num).round()
        : null;
    final audioBitrate = args["audio_bitrate"] is num
        ? (args["audio_bitrate"] as num).round()
        : null;
    final imageFormatGroup =
        parseImageFormatGroup(args["image_format_group"]) ??
            ImageFormatGroup.unknown;

    final controller = CameraController(
      description,
      resolutionPreset,
      enableAudio: enableAudio,
      fps: fps,
      videoBitrate: videoBitrate,
      audioBitrate: audioBitrate,
      imageFormatGroup: imageFormatGroup,
    );

    _attachController(controller);
    await controller.initialize();
    return cameraValueToMap(controller.value);
  }

  Future<void> _startImageStream() async {
    final controller = _requireController();
    await controller.startImageStream((CameraImage image) {
      if (!widget.control.getBool("on_stream_image", false)!) {
        return;
      }
      if (_processingImage) {
        return;
      }
      _processingImage = true;
      unawaited(_processStreamImage(image));
    });
  }

  Future<void> _processStreamImage(CameraImage image) async {
    try {
      final Uint8List encoded = encodeCameraImage(image);
      if (encoded.isEmpty) {
        return;
      }
      widget.control
          .triggerEvent("stream_image", cameraImageToMap(image, encoded));
    } finally {
      _processingImage = false;
    }
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("Camera.$name($args)");
    switch (name) {
      case "get_available_cameras":
        final cameras = await availableCameras();
        return cameras.map((c) => cameraDescriptionToMap(c)).toList();
      case "initialize":
        await _initializeController(args is Map ? args : {});
      case "get_exposure_offset_step_size":
        return await _requireController().getExposureOffsetStepSize();
      case "get_max_exposure_offset":
        return await _requireController().getMaxExposureOffset();
      case "get_max_zoom_level":
        return await _requireController().getMaxZoomLevel();
      case "get_min_exposure_offset":
        return await _requireController().getMinExposureOffset();
      case "get_min_zoom_level":
        return await _requireController().getMinZoomLevel();
      case "lock_capture_orientation":
        final orientation = parseDeviceOrientation(args["orientation"]);
        await _requireController().lockCaptureOrientation(orientation);
        break;
      case "unlock_capture_orientation":
        await _requireController().unlockCaptureOrientation();
        break;
      case "pause_preview":
        await _requireController().pausePreview();
        break;
      case "resume_preview":
        await _requireController().resumePreview();
        break;
      case "take_picture":
        final file = await _requireController().takePicture();
        return await file.readAsBytes();
      case "prepare_for_video_recording":
        await _requireController().prepareForVideoRecording();
        break;
      case "start_video_recording":
        await _requireController().startVideoRecording();
        break;
      case "pause_video_recording":
        await _requireController().pauseVideoRecording();
        break;
      case "resume_video_recording":
        await _requireController().resumeVideoRecording();
        break;
      case "stop_video_recording":
        final file = await _requireController().stopVideoRecording();
        return await file.readAsBytes();
      case "supports_image_streaming":
        return _requireController().supportsImageStreaming();
      case "start_image_stream":
        await _startImageStream();
        break;
      case "stop_image_stream":
        await _requireController().stopImageStream();
        _processingImage = false;
        break;
      case "set_description":
        final description = parseCameraDescription(args["description"]);
        if (description != null) {
          await _requireController().setDescription(description);
        }
        break;
      case "set_exposure_mode":
        final mode = parseExposureMode(args["mode"]);
        if (mode != null) {
          await _requireController().setExposureMode(mode);
        }
        break;
      case "set_exposure_offset":
        final offset = args["offset"];
        if (offset is num) {
          return await _requireController()
              .setExposureOffset(offset.toDouble());
        }
        break;
      case "set_exposure_point":
        final point = parseOffset(args["point"]);
        await _requireController().setExposurePoint(point);
        break;
      case "set_flash_mode":
        final mode = parseFlashMode(args["mode"]);
        if (mode != null) {
          await _requireController().setFlashMode(mode);
        }
        break;
      case "set_focus_mode":
        final mode = parseFocusMode(args["mode"]);
        if (mode != null) {
          await _requireController().setFocusMode(mode);
        }
        break;
      case "set_focus_point":
        final point = parseOffset(args["point"]);
        await _requireController().setFocusPoint(point);
        break;
      case "set_zoom_level":
        final zoom = args["zoom"];
        if (zoom is num) {
          await _requireController().setZoomLevel(zoom.toDouble());
        }
        break;
      default:
        throw Exception("Unknown Camera method: $name");
    }
    return null;
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Camera build: ${widget.control.id}");

    Widget preview = const SizedBox.shrink();
    final controller = _controller;

    if (_previewEnabled &&
        controller != null &&
        controller.value.isInitialized) {
      final contentCtrl = widget.control.child("content");
      final contentWidget =
          contentCtrl != null ? ControlWidget(control: contentCtrl) : null;
      preview = CameraPreview(controller, child: contentWidget);
    }

    return LayoutControl(control: widget.control, child: preview);
  }
}
