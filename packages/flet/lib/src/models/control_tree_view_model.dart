import 'package:equatable/equatable.dart';

import 'control.dart';

class ControlTreeViewModel extends Equatable {
  final Control control;
  final List<ControlTreeViewModel> children;

  const ControlTreeViewModel({required this.control, required this.children});

  @override
  List<Object?> get props => [control, children];
}
