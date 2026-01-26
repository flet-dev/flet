import 'package:collection/collection.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

import '../flet_service.dart';
import '../utils/file_picker.dart';
import '../utils/platform.dart';

class FilePickerService extends FletService {
  FilePickerService({required super.control});

  List<PlatformFile>? _files;

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
    var srcBytes = args["src_bytes"];

    if (allowedExtensions != null && allowedExtensions.isNotEmpty) {
      fileType = FileType.custom;
    }
    switch (name) {
      case "upload":
        var files = args["files"];
        if (files != null && _files != null) {
          uploadFiles(files, control.backend.pageUri);
        }
      case "pick_files":
        _files = (await FilePicker.pickFiles(
                dialogTitle: dialogTitle,
                initialDirectory: initialDirectory,
                lockParentWindow: true,
                type: fileType,
                allowedExtensions: allowedExtensions,
                allowMultiple: args["allow_multiple"],
                withData: false,
                withReadStream: true))
            ?.files;
        return _files != null
            ? _files!.asMap().entries.map((file) {
                return FilePickerFile(
                        id: file.key, // use entry's index as id
                        name: file.value.name,
                        path: kIsWeb ? null : file.value.path,
                        size: file.value.size)
                    .toMap();
              }).toList()
            : [];
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
        return await FilePicker.saveFile(
            dialogTitle: dialogTitle,
            fileName: args["file_name"] != null || !isIOSMobile()
                ? args["file_name"]
                : "new-file",
            initialDirectory: initialDirectory,
            lockParentWindow: true,
            type: fileType,
            allowedExtensions: allowedExtensions,
            bytes: srcBytes);
      case "get_directory_path":
        if (kIsWeb) {
          throw Exception("Get Directory Path dialog is not supported on web.");
        }
        return await FilePicker.getDirectoryPath(
          dialogTitle: dialogTitle,
          initialDirectory: initialDirectory,
          lockParentWindow: true,
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

    for (var uf in uploadFiles) {
      var file = ((uf.id != null && uf.id! >= 0 && uf.id! < _files!.length)
              ? _files![uf.id!]
              : null) // by id
          ??
          _files!.firstWhereOrNull((f) => f.name == uf.name); // by name

      if (file != null) {
        try {
          await uploadFile(
              file, getFullUploadUrl(pageUri, uf.uploadUrl), uf.method);
          _files!.remove(file); // Remove the uploaded file
        } catch (e) {
          sendProgress(file.name, null, e.toString());
        }
      } else {
        debugPrint(
            "FilePicker Error: File '${uf.name}' (id: ${uf.id}) not found.");
      }
    }
  }

  Future uploadFile(PlatformFile file, String uploadUrl, String method) async {
    final fileReadStream = file.readStream;
    if (fileReadStream == null) {
      throw Exception('Cannot read file from null stream');
    }
    debugPrint("Uploading ${file.name}");
    final streamedRequest = http.StreamedRequest(method, Uri.parse(uploadUrl))
      ..headers.addAll({
        //'Cache-Control': 'no-cache',
      });
    streamedRequest.contentLength = file.size;

    // send 0%
    sendProgress(file.name, 0, null);

    double lastSent = 0; // send every 10%
    double progress = 0;
    int bytesSent = 0;
    fileReadStream.listen((chunk) async {
      //debugPrint(chunk.length);
      streamedRequest.sink.add(chunk);
      bytesSent += chunk.length;
      progress = bytesSent / file.size;
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
