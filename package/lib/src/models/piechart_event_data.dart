import 'package:equatable/equatable.dart';

class PieChartEventData extends Equatable {
  final String eventType;
  final int? sectionIndex;
  // final double? angle;
  // final double? radius;

  const PieChartEventData(
      {required this.eventType, required this.sectionIndex});

  Map<String, dynamic> toJson() =>
      <String, dynamic>{'type': eventType, 'section_index': sectionIndex};

  @override
  List<Object?> get props => [eventType, sectionIndex];
}
