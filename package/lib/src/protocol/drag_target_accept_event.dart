class DragTargetAcceptEvent {
  final String srcId;
  final double x;
  final double y;

  DragTargetAcceptEvent({
    required this.srcId,
    required this.x,
    required this.y,
  });

  Map<String, dynamic> toJson() => <String, dynamic>{
        'src_id': srcId,
        'x': x,
        'y': y,
      };
}
