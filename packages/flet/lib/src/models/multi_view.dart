import 'dart:ui';

class MultiView {
  int viewId;
  FlutterView flutterView;
  Map<dynamic, dynamic> initialData;

  MultiView(
      {required this.viewId,
      required this.flutterView,
      required this.initialData});

  Map<String, dynamic> toMap() {
    return {"view_id": viewId, "initial_data": initialData};
  }
}
