import 'package:file_picker/file_picker.dart';

/// The web picker's options (non-web builds: the defaults, which they
/// ignore). `FilePickerWebOptions` lives in the web-only `file_picker_web`.
WebOptions filePickerWebOptions({required bool cancelUploadOnWindowBlur}) =>
    const WebOptions();
