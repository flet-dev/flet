import 'dart:typed_data';

import 'package:collection/collection.dart';
import 'package:file_picker/file_picker.dart';
import 'enums.dart';

import '../models/control.dart';

class FilePickerResultEvent {
  final String? path;
  final List<FilePickerFile>? files;

  FilePickerResultEvent({required this.path, required this.files});

  Map<String, dynamic> toMap() => <String, dynamic>{
        'path': path,
        'files': files?.map((FilePickerFile f) => f.toMap()).toList()
      };
}

class FilePickerFile {
  final int id;
  final String name;
  final String? path;
  final int size;
  final Uint8List? bytes;

  FilePickerFile(
      {required this.id,
      required this.name,
      required this.path,
      required this.size,
      required this.bytes});

  Map<String, dynamic> toMap() => <String, dynamic>{
        'id': id,
        'name': name,
        'path': path,
        'size': size,
        'bytes': bytes
      };
}

class FilePickerUploadFile {
  final int? id;
  final String? name;
  final String uploadUrl;
  final String method;

  FilePickerUploadFile(
      {required this.id,
      required this.name,
      required this.uploadUrl,
      required this.method});
}

class FilePickerUploadProgressEvent {
  final String name;
  final double? progress;
  final String? error;

  FilePickerUploadProgressEvent(
      {required this.name, required this.progress, required this.error});

  Map<String, dynamic> toMap() => <String, dynamic>{
        'file_name': name,
        'progress': progress,
        'error': error
      };
}

FileType? parseFileType(String? value, [FileType? defaultValue]) {
  return parseEnum(FileType.values, value, defaultValue);
}

extension FilePickerParsers on Control {
  FileType? getFileType(String propertyName, [FileType? defaultValue]) {
    return parseFileType(get(propertyName), defaultValue);
  }
}

/// Reserves picked files for upload using their original selection IDs, falling
/// back to names. Removes each target before any asynchronous upload starts:
/// streams can only be consumed once, including after a failed upload, and must
/// not be shared by duplicate requests or overlapping upload calls.
List<(FilePickerUploadFile, PlatformFile?)> takeUploadTargets(
    List<FilePickerUploadFile> uploads, Map<int, PlatformFile> picked) {
  return [
    for (var uf in uploads)
      (
        uf,
        picked.remove(uf.id) ??
            picked.remove(picked.entries
                .firstWhereOrNull((entry) => entry.value.name == uf.name)
                ?.key)
      )
  ];
}
