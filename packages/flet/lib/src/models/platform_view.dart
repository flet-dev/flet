import 'dart:ui';

class PlatformView {
  int viewId;
  FlutterView flutterView;
  Map<dynamic, dynamic> initialData;

  PlatformView(
      {required this.viewId,
      required this.flutterView,
      required this.initialData});

  Map<String, dynamic> toMap() {
    return {"view_id": viewId, "initial_data": initialData};
  }
}
