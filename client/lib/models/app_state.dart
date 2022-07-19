import 'dart:ui';

import 'package:equatable/equatable.dart';
import 'package:flet_view/models/control_type.dart';

import 'control.dart';

class Counter {
  int value;
  Counter(this.value);
}

class AppState extends Equatable {
  final Uri? pageUri;
  final String route;
  final String sessionId;
  final bool isLoading;
  final int reconnectingTimeout;
  final String error;
  final Size size;
  final String sizeBreakpoint;
  final Brightness displayBrightness;
  final Map<String, double> sizeBreakpoints;
  final Map<String, Control> controls;

  const AppState(
      {required this.pageUri,
      required this.route,
      required this.sessionId,
      required this.isLoading,
      required this.reconnectingTimeout,
      required this.error,
      required this.size,
      required this.sizeBreakpoint,
      required this.sizeBreakpoints,
      required this.displayBrightness,
      required this.controls});

  factory AppState.initial() => const AppState(
      pageUri: null,
      route: "",
      sessionId: "",
      isLoading: true,
      reconnectingTimeout: 0,
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
      displayBrightness: Brightness.light,
      controls: {
        "page": Control(
            id: "page",
            pid: "",
            type: ControlType.page,
            name: "",
            childIds: [],
            attrs: {})
      });

  AppState copyWith(
          {Uri? pageUri,
          String? route,
          String? sessionId,
          bool? isLoading,
          int? reconnectingTimeout,
          String? error,
          Size? size,
          String? sizeBreakpoint,
          Map<String, double>? sizeBreakpoints,
          Brightness? displayBrightness,
          Map<String, Control>? controls}) =>
      AppState(
          pageUri: pageUri ?? this.pageUri,
          route: route ?? this.route,
          sessionId: sessionId ?? this.sessionId,
          isLoading: isLoading ?? this.isLoading,
          reconnectingTimeout: reconnectingTimeout ?? this.reconnectingTimeout,
          error: error ?? this.error,
          size: size ?? this.size,
          sizeBreakpoint: sizeBreakpoint ?? this.sizeBreakpoint,
          sizeBreakpoints: sizeBreakpoints ?? this.sizeBreakpoints,
          displayBrightness: displayBrightness ?? this.displayBrightness,
          controls: controls ?? this.controls);

  @override
  List<Object?> get props => [isLoading, error, sessionId, controls];
}
