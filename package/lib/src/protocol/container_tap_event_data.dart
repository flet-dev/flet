class ContainerTapEventData {
  final double localX;
  final double localY;
  final double globalX;
  final double globalY;

  ContainerTapEventData(
      {required this.localX,
      required this.localY,
      required this.globalX,
      required this.globalY});

  Map<String, dynamic> toJson() => <String, dynamic>{
        'lx': localX,
        'ly': localY,
        'gx': globalX,
        'gy': globalY
      };
}
