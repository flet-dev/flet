import 'package:equatable/equatable.dart';

class LineChartDataPointViewModel extends Equatable {
  final double x;
  final double y;

  const LineChartDataPointViewModel({required this.x, required this.y});

  @override
  List<Object?> get props => [x, y];
}
