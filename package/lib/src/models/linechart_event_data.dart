import 'package:equatable/equatable.dart';

class LineChartEventData extends Equatable {
  final String eventType;
  final List<LineChartEventDataSpot> barSpots;

  const LineChartEventData({required this.eventType, required this.barSpots});

  Map<String, dynamic> toJson() => <String, dynamic>{
        'type': eventType,
        'spots': barSpots,
      };

  @override
  List<Object?> get props => [eventType, barSpots];
}

class LineChartEventDataSpot extends Equatable {
  final int barIndex;
  final int spotIndex;

  const LineChartEventDataSpot(
      {required this.barIndex, required this.spotIndex});

  Map<String, dynamic> toJson() => <String, dynamic>{
        'bar_index': barIndex,
        'spot_index': spotIndex,
      };

  @override
  List<Object?> get props => [barIndex, spotIndex];
}
