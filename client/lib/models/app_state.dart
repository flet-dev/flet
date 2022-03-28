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
  final Map<String, Control> controls;

  const AppState(
      {required this.isLoading,
      required this.error,
      required this.sessionId,
      required this.controls});

  factory AppState.initial() =>
      const AppState(isLoading: true, error: "", sessionId: "", controls: {});

  AppState copyWith(
          {bool? isLoading,
          String? error,
          String? sessionId,
          Map<String, Control>? controls}) =>
      AppState(
          isLoading: isLoading ?? this.isLoading,
          error: error ?? this.error,
          sessionId: sessionId ?? this.sessionId,
          controls: controls ?? this.controls);

  @override
  List<Object?> get props => [isLoading, error, sessionId, controls];
}
