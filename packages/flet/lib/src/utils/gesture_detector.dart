import 'package:flutter/gestures.dart';

class MultiTouchGestureRecognizer extends MultiTapGestureRecognizer {
  late MultiTouchGestureRecognizerCallback onMultiTap;
  var numberOfTouches = 0;
  int minNumberOfTouches = 0;

  MultiTouchGestureRecognizer() {
    super.onTapDown = (pointer, details) => addTouch(pointer, details);
    super.onTapUp = (pointer, details) => removeTouch(pointer, details);
    super.onTapCancel = (pointer) => cancelTouch(pointer);
    super.onTap = (pointer) => captureDefaultTap(pointer);
  }

  void addTouch(int pointer, TapDownDetails details) {
    //debugPrint("Add touch: $pointer");
    numberOfTouches++;
    if (numberOfTouches == minNumberOfTouches) {
      onMultiTap(true);
      numberOfTouches = 0;
    }
  }

  void removeTouch(int pointer, TapUpDetails details) {
    onRemoveTouch(pointer);
  }

  void cancelTouch(int pointer) {
    onRemoveTouch(pointer);
  }

  void onRemoveTouch(int pointer) {
    //debugPrint("Remove touch: $pointer");
    onMultiTap(false);
    numberOfTouches = 0;
  }

  void captureDefaultTap(int pointer) {}

  @override
  set onTapDown(onTapDown) {}

  @override
  set onTapUp(onTapUp) {}

  @override
  set onTapCancel(onTapCancel) {}

  @override
  set onTap(onTap) {}
}

typedef MultiTouchGestureRecognizerCallback = void Function(
    bool correctNumberOfTouches);
