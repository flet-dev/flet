class KeyboardEvent {
  final String key;
  final int physicalKey;
  final bool isShiftPressed;
  final bool isControlPressed;
  final bool isAltPressed;
  final bool isMetaPressed;

  KeyboardEvent(
      {required this.key,
      required this.physicalKey,
      required this.isShiftPressed,
      required this.isControlPressed,
      required this.isAltPressed,
      required this.isMetaPressed});

  Map<String, dynamic> toMap() => <String, dynamic>{
        'key': key,
        'physical_key': physicalKey,
        'shift': isShiftPressed,
        'ctrl': isControlPressed,
        'alt': isAltPressed,
        'meta': isMetaPressed
      };
}
