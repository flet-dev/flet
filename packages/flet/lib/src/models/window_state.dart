class WindowState {
  bool maximized;
  bool minimized;
  bool fullScreen;
  bool alwaysOnTop;
  bool focused;
  bool visible;
  bool minimizable;
  bool maximizable;
  bool resizable;
  bool preventClose;
  bool skipTaskBar;
  double width;
  double height;
  double top;
  double left;
  double opacity;

  WindowState({
    required this.maximized,
    required this.minimized,
    required this.fullScreen,
    required this.alwaysOnTop,
    required this.focused,
    required this.visible,
    required this.minimizable,
    required this.maximizable,
    required this.resizable,
    required this.preventClose,
    required this.skipTaskBar,
    required this.width,
    required this.height,
    required this.top,
    required this.left,
    required this.opacity,
  });

  Map<String, dynamic> toJson() => <String, dynamic>{
        'maximized': maximized,
        'minimized': minimized,
        'full_screen': fullScreen,
        'always_on_top': alwaysOnTop,
        'focused': focused,
        'visible': visible,
        'minimizable': minimizable,
        'maximizable': maximizable,
        'resizable': resizable,
        'prevent_close': preventClose,
        'skip_task_bar': skipTaskBar,
        'width': width,
        'height': height,
        'top': top,
        'left': left,
        'opacity': opacity,
      };

  @override
  String toString() {
    return toJson().toString();
  }
}
