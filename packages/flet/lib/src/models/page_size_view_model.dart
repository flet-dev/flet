import 'dart:ui';

import 'package:equatable/equatable.dart';

class PageSizeViewModel extends Equatable {
  final Map<String, double> breakpoints;
  final Size size;

  const PageSizeViewModel({required this.size, required this.breakpoints});

  @override
  List<Object?> get props => [size, breakpoints];
}
