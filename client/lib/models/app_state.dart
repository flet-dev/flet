import 'dart:ui';

import 'package:equatable/equatable.dart';
import 'control.dart';

class Counter {
  int value;
  Counter(this.value);
}

class AppState extends Equatable {
  final bool isLoading;
  final String error;
  final String sessionId;
  final Size size;
  final String sizeBreakpoint;
  final Map<String, double> sizeBreakpoints;
  final Map<String, Control> controls;

  const AppState(
      {required this.isLoading,
      required this.error,
      required this.sessionId,
      required this.size,
      required this.sizeBreakpoint,
      required this.sizeBreakpoints,
      required this.controls});

  factory AppState.initial() => const AppState(
          isLoading: true,
          error: "",
          sessionId: "",
          size: Size(0, 0),
          sizeBreakpoint: "",
          sizeBreakpoints: {
            "xs": 0,
            "sm": 576,
            "md": 768,
            "lg": 992,
            "xl": 1200,
            "xxl": 1400
          },
          controls: {});

  AppState copyWith(
          {bool? isLoading,
          String? error,
          String? sessionId,
          Size? size,
          String? sizeBreakpoint,
          Map<String, double>? sizeBreakpoints,
          Map<String, Control>? controls}) =>
      AppState(
          isLoading: isLoading ?? this.isLoading,
          error: error ?? this.error,
          sessionId: sessionId ?? this.sessionId,
          size: size ?? this.size,
          sizeBreakpoint: sizeBreakpoint ?? this.sizeBreakpoint,
          sizeBreakpoints: sizeBreakpoints ?? this.sizeBreakpoints,
          controls: controls ?? this.controls);

  @override
  List<Object?> get props => [isLoading, error, sessionId, controls];
}
