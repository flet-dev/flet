import 'package:equatable/equatable.dart';

class BarChartEventData extends Equatable {
  final String eventType;
  final int? groupIndex;
  final int? rodIndex;
  final int? stackItemIndex;

  const BarChartEventData(
      {required this.eventType,
      required this.groupIndex,
      required this.rodIndex,
      required this.stackItemIndex});

  Map<String, dynamic> toJson() => <String, dynamic>{
        'type': eventType,
        'group_index': groupIndex,
        'rod_index': rodIndex,
        'stack_item_index': stackItemIndex
      };

  @override
  List<Object?> get props => [eventType, groupIndex, rodIndex, stackItemIndex];
}
