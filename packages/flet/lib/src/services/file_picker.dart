import 'package:file_picker/file_picker.dart';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

import '../flet_service.dart';
import '../utils/file_picker.dart';
import '../utils/file_picker_web_options.dart'
    if (dart.library.js_interop) '../utils/file_picker_web_options_web.dart';
import '../utils/numbers.dart';
import '../utils/platform.dart';
import '../utils/platform_utils_web.dart'
    if (dart.library.io) '../utils/platform_utils_non_web.dart';

class FilePickerService extends FletService {
  FilePickerService({required super.control});

  Map<int, PlatformFile> _files = {};

  @override
  void init() {
    super.init();
    debugPrint("FilePickerService(${control.id}).init: ${control.properties}");
    control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void dispose() {
    debugPrint("FilePickerService(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("FilePicker.$name($args)");
    var dialogTitle = args["dialog_title"];
    var fileType = parseFileType(args["file_type"], FileType.any)!;
    var initialDirectory = args["initial_directory"];
    var allowedExtensions = (args["allowed_extensions"] as List?)
        ?.map((e) => e.toString())
        .toList();
    var withData = parseBool(args["with_data"], false)!;
    var cancelUploadOnWindowBlur =
        parseBool(args["cancel_upload_on_window_blur"], true)!;
    var compressionQuality = parseInt(args["compression_quality"], 0)!;
    var srcBytes = args["src_bytes"];

    if (allowedExtensions != null && allowedExtensions.isNotEmpty) {
      fileType = FileType.custom;
    }
    switch (name) {
      case "upload":
        var files = args["files"];
        if (files != null) {
          uploadFiles(files, control.backend.pageUri);
        }
      case "pick_files":
        var fromGesture = args["_from_gesture"] == true;

        // Not reached from a gesture and the browser has already told us it
        // will not open the dialog: fail now with something actionable, rather
        // than leaving the caller waiting out its timeout on nothing.
        if (!fromGesture && isGestureGatedDialogBlocked()) {
          throw Exception(
              "This browser only opens a file picker while it is handling a "
              "user's click, so pick_files() cannot open one - by the time it "
              "reaches your Python code the click is over. Attach "
              "ft.PickFiles(...) to the control's `action` property instead "
              "and handle FilePicker.on_result. "
              "See https://flet.dev/docs/cookbook/client-actions");
        }

        // Note for future edits: nothing may be awaited between entering this
        // method and the FilePicker.pickFiles() / pickFile() call below. On
        // the gesture path an async gap discards the browser's user
        // activation and the dialog silently never opens. See
        // flet-dev/flet#3710.
        final webOptions = filePickerWebOptions(
            cancelUploadOnWindowBlur: cancelUploadOnWindowBlur);
        final List<PlatformFile> picked;
        if (args["allow_multiple"] == true) {
          picked = await FilePicker.pickFiles(
              dialogTitle: dialogTitle,
              initialDirectory: initialDirectory,
              type: fileType,
              allowedExtensions: allowedExtensions,
              compressionQuality: compressionQuality,
              windowsOptions: const WindowsOptions(lockParentWindow: true),
              linuxOptions: const LinuxOptions(lockParentWindow: true),
              webOptions: webOptions);
        } else {
          final file = await FilePicker.pickFile(
              dialogTitle: dialogTitle,
              initialDirectory: initialDirectory,
              type: fileType,
              allowedExtensions: allowedExtensions,
              compressionQuality: compressionQuality,
              windowsOptions: const WindowsOptions(lockParentWindow: true),
              linuxOptions: const LinuxOptions(lockParentWindow: true),
              webOptions: webOptions);
          picked = file != null ? [file] : [];
        }
        _files = Map.of(picked.asMap());
        var pickedFiles = <Map<String, dynamic>>[];
        for (var file in _files.entries) {
          pickedFiles.add(FilePickerFile(
                  id: file.key, // use entry's index as id
                  name: file.value.name,
                  path: kIsWeb ? null : file.value.path,
                  size: file.value.lengthSync() ?? await file.value.length() ?? 0,
                  bytes: withData ? await file.value.readAsBytes() : null)
              .toMap());
        }
        if (fromGesture) {
          // A gesture-triggered pick has no caller to return to.
          control.triggerEvent("result", {"files": pickedFiles});
        }
        return pickedFiles;
      case "save_file":
        if ((kIsWeb || isAndroidMobile() || isIOSMobile()) &&
            srcBytes == null) {
          throw Exception(
              "\"src_bytes\" is required when saving a file on Web, Android and iOS.");
        }
        if (kIsWeb && args["file_name"] == null) {
          throw Exception(
              "\"file_name\" is required when saving a file on Web.");
        }
        // file_picker 13 always writes the file. Without bytes (desktop) the
        // app writes it itself at the returned path, so start it empty.
        final saved = await FilePicker.saveFile(
            dialogTitle: dialogTitle,
            fileName: args["file_name"] ??
                (isAndroidMobile() || isIOSMobile() ? "new-file" : ""),
            initialDirectory: initialDirectory,
            bytes: srcBytes != null
                ? Uint8List.fromList(List<int>.from(srcBytes))
                : Uint8List(0),
            windowsOptions: const WindowsOptions(lockParentWindow: true),
            linuxOptions: const LinuxOptions(lockParentWindow: true));
        if (saved == null) {
          return null;
        }
        return saved.scheme == "file" ? saved.toFilePath() : saved.toString();
      case "get_directory_path":
        if (kIsWeb) {
          throw Exception("Get Directory Path dialog is not supported on web.");
        }
        return await FilePicker.getDirectoryPath(
          dialogTitle: dialogTitle,
          initialDirectory: initialDirectory,
          windowsOptions: const WindowsOptions(lockParentWindow: true),
          linuxOptions: const LinuxOptions(lockParentWindow: true),
        );
      default:
        throw Exception("Unknown FilePicker method: $name");
    }
  }

  Future uploadFiles(List<dynamic> files, Uri pageUri) async {
    var uploadFiles = files.map((u) => FilePickerUploadFile(
        id: u["id"],
        name: u["name"],
        uploadUrl: u["upload_url"],
        method: u["method"]));

    final targets = takeUploadTargets(uploadFiles.toList(), _files);

    for (var (uf, file) in targets) {
      if (file != null) {
        try {
          await uploadFile(
              file, getFullUploadUrl(pageUri, uf.uploadUrl), uf.method);
        } catch (e) {
          sendProgress(file.name, null, e.toString());
        }
      } else {
        debugPrint(
            "FilePicker Error: File '${uf.name}' (id: ${uf.id}) not found.");
        // Report it, or the caller waits forever for this file's upload.
        sendProgress(
            uf.name ?? "", null, "File not found among the picked files.");
      }
    }
  }

  Future uploadFile(PlatformFile file, String uploadUrl, String method) async {
    final size = file.lengthSync() ?? await file.length();
    if (size == null) {
      throw Exception("Cannot read the size of ${file.name}");
    }
    final fileReadStream = file.readAsByteStream();
    debugPrint("Uploading ${file.name}");
    final streamedRequest = http.StreamedRequest(method, Uri.parse(uploadUrl))
      ..headers.addAll({
        //'Cache-Control': 'no-cache',
      });
    streamedRequest.contentLength = size;

    // send 0%
    sendProgress(file.name, 0, null);

    double lastSent = 0; // send every 10%
    double progress = 0;
    int bytesSent = 0;
    fileReadStream.listen((chunk) async {
      //debugPrint(chunk.length);
      streamedRequest.sink.add(chunk);
      bytesSent += chunk.length;
      progress = size == 0 ? 1.0 : bytesSent / size;
      if (progress >= lastSent) {
        lastSent += 0.1;
        if (progress != 1.0) {
          sendProgress(file.name, progress, null);
        }
      }
    }, onDone: () {
      streamedRequest.sink.close();
    });

    var streamedResponse = await streamedRequest.send();
    var response = await http.Response.fromStream(streamedResponse);
    if (response.statusCode < 200 || response.statusCode > 204) {
      sendProgress(file.name, null,
          "Upload endpoint returned code ${response.statusCode}: ${response.body}");
    } else {
      // send 100%
      sendProgress(file.name, progress, null);
    }
  }

  void sendProgress(String name, double? progress, String? error) {
    control.triggerEvent(
        "upload",
        FilePickerUploadProgressEvent(
                name: name, progress: progress, error: error)
            .toMap());
  }

  String getFullUploadUrl(Uri pageUri, String uploadUrl) {
    Uri uploadUri = Uri.parse(uploadUrl);
    if (!uploadUri.hasAuthority) {
      return Uri(
              scheme: pageUri.scheme,
              host: pageUri.host,
              port: pageUri.port,
              path: uploadUri.path,
              query: uploadUri.query)
          .toString();
    } else {
      return uploadUrl;
    }
  }
}
