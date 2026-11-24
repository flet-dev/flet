import 'package:file_picker/file_picker.dart';
import 'package:file_picker_web/file_picker_web.dart';

/// The web picker's options. Files are read on demand
/// (`PlatformFile.readAsBytes()` / `readAsByteStream()`), never preloaded:
/// `withData` defaults to true in file_picker_web 4.
WebOptions filePickerWebOptions({required bool cancelUploadOnWindowBlur}) =>
    FilePickerWebOptions(
        // ignore: deprecated_member_use
        withData: false,
        cancelUploadOnWindowBlur: cancelUploadOnWindowBlur);
