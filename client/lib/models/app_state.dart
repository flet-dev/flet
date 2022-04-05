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
  final Map<String, Control> controls;

  const AppState(
      {required this.isLoading,
      required this.error,
      required this.sessionId,
      required this.size,
      required this.controls});

  factory AppState.initial() => const AppState(
      isLoading: true,
      error: "",
      sessionId: "",
      size: Size(0, 0),
      controls: {});

  AppState copyWith(
          {bool? isLoading,
          String? error,
          String? sessionId,
          Size? size,
          Map<String, Control>? controls}) =>
      AppState(
          isLoading: isLoading ?? this.isLoading,
          error: error ?? this.error,
          sessionId: sessionId ?? this.sessionId,
          size: size ?? this.size,
          controls: controls ?? this.controls);

  @override
  List<Object?> get props => [isLoading, error, sessionId, controls];
}
