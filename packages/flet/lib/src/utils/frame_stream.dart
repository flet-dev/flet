import 'dart:ui' as ui;

import 'package:flutter/widgets.dart';

/// Visibility awareness for controls that consume a Python-pushed frame
/// stream (e.g. `RawImage`, `MatplotlibChartCanvas`).
///
/// While the browser tab is backgrounded (or a desktop window minimized) the
/// Flutter frame pipeline is suspended: `setState` schedules a frame that is
/// never produced, so `addPostFrameCallback` callbacks never run. The frame
/// producer, meanwhile, keeps streaming — a Pyodide worker and a remote
/// server over a WebSocket are both oblivious to client visibility and
/// neither is throttled by it. If the widget kept decoding frames and
/// deferring old-image disposal to post-frame callbacks, decoded [ui.Image]s
/// and pending disposals would pile up unbounded in the Dart heap and flush
/// into the engine all at once on resume, flooding it with exceptions.
///
/// This is a client-side problem, independent of transport, so the fix lives
/// here rather than in any one control. Mixers:
///
///  - read [visible] to stop decoding / uploading / `setState`-ing while
///    hidden (keeping only cheap offscreen state up to date), and
///  - dispose replaced images through [disposeReplaced] / [disposeReplacedAll],
///    which free immediately while hidden instead of deferring to a
///    post-frame callback that won't fire.
///
/// When visibility returns, [onVisibilityRestored] is invoked so the mixer can
/// present the latest frame it accumulated while hidden.
mixin FrameStreamVisibility<T extends StatefulWidget> on State<T> {
  AppLifecycleListener? _lifecycleListener;
  bool _visible = true;

  /// Whether the tab / window is currently visible.
  bool get visible => _visible;

  /// Called once each time visibility is restored, after [visible] flips back
  /// to true. Implementations should present the frame accumulated while
  /// hidden (typically by enqueuing work on their apply chain — no ack, since
  /// those frames were already acked as they arrived).
  void onVisibilityRestored();

  @override
  void initState() {
    super.initState();
    final state = WidgetsBinding.instance.lifecycleState;
    _visible = state == null ||
        state == AppLifecycleState.resumed ||
        state == AppLifecycleState.inactive;
    _lifecycleListener = AppLifecycleListener(
      onShow: _handleVisible,
      onResume: _handleVisible,
      onHide: _handleHidden,
      onPause: _handleHidden,
    );
  }

  @override
  void dispose() {
    _lifecycleListener?.dispose();
    _lifecycleListener = null;
    super.dispose();
  }

  void _handleHidden() {
    _visible = false;
  }

  void _handleVisible() {
    if (_visible) return;
    _visible = true;
    onVisibilityRestored();
  }

  /// Dispose an image that has just been replaced. When visible, disposal is
  /// deferred to a post-frame callback so the frame still painting it can
  /// finish first; when hidden, nothing is painting it and post-frame
  /// callbacks won't fire until resume, so it is freed immediately to keep
  /// replaced images from piling up.
  void disposeReplaced(ui.Image image) {
    if (_visible) {
      WidgetsBinding.instance.addPostFrameCallback((_) => image.dispose());
    } else {
      image.dispose();
    }
  }

  void disposeReplacedAll(List<ui.Image> images) {
    if (images.isEmpty) return;
    if (_visible) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        for (final img in images) {
          img.dispose();
        }
      });
    } else {
      for (final img in images) {
        img.dispose();
      }
    }
  }
}
