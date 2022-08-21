library flet;

export 'src/flet_app.dart';
export 'src/utils.dart';
export 'src/utils/platform_utils_non_web.dart'
    if (dart.library.js) "src/utils/platform_utils_web.dart";
