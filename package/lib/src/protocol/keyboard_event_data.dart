class KeyboardEventData {
  final String key;
  final bool isShiftPressed;
  final bool isControlPressed;
  final bool isAltPressed;
  final bool isMetaPressed;

  KeyboardEventData(
      {required this.key,
      required this.isShiftPressed,
      required this.isControlPressed,
      required this.isAltPressed,
      required this.isMetaPressed});

  Map<String, dynamic> toJson() => <String, dynamic>{
        'key': key,
        'shift': isShiftPressed,
        'ctrl': isControlPressed,
        'alt': isAltPressed,
        'meta': isMetaPressed
      };
}
