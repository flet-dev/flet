import 'dart:ui';

import 'package:equatable/equatable.dart';
import 'control.dart';

class Counter {
  int value;
  Counter(this.value);
}

class AppState extends Equatable {
  final Uri? pageUri;
  final String sessionId;
  final bool isLoading;
  final String error;
  final Size size;
  final String sizeBreakpoint;
  final Map<String, double> sizeBreakpoints;
  final Map<String, Control> controls;

  const AppState(
      {required this.pageUri,
      required this.sessionId,
      required this.isLoading,
      required this.error,
      required this.size,
      required this.sizeBreakpoint,
      required this.sizeBreakpoints,
      required this.controls});

  factory AppState.initial() => const AppState(
          pageUri: null,
          sessionId: "",
          isLoading: true,
          error: "",
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
          {Uri? pageUri,
          String? sessionId,
          bool? isLoading,
          String? error,
          Size? size,
          String? sizeBreakpoint,
          Map<String, double>? sizeBreakpoints,
          Map<String, Control>? controls}) =>
      AppState(
          pageUri: pageUri ?? this.pageUri,
          sessionId: sessionId ?? this.sessionId,
          isLoading: isLoading ?? this.isLoading,
          error: error ?? this.error,
          size: size ?? this.size,
          sizeBreakpoint: sizeBreakpoint ?? this.sizeBreakpoint,
          sizeBreakpoints: sizeBreakpoints ?? this.sizeBreakpoints,
          controls: controls ?? this.controls);

  @override
  List<Object?> get props => [isLoading, error, sessionId, controls];
}
