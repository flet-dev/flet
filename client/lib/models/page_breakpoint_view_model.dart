import 'dart:ui';

import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';

class PageBreakpointViewModel extends Equatable {
  final String breakpoint;
  final Map<String, double> breakpoints;

  const PageBreakpointViewModel(
      {required this.breakpoint, required this.breakpoints});

  static PageBreakpointViewModel fromStore(Store<AppState> store) {
    return PageBreakpointViewModel(
        breakpoint: store.state.sizeBreakpoint,
        breakpoints: store.state.sizeBreakpoints);
  }

  @override
  List<Object?> get props => [breakpoint, breakpoints];
}
