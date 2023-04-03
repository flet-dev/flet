import 'package:equatable/equatable.dart';
import 'package:flet/src/models/control_view_model.dart';
import 'package:flutter/material.dart';

import 'control.dart';

class Counter {
  int value;
  Counter(this.value);
}

class AppState extends Equatable {
  final Uri? pageUri;
  final String assetsDir;
  final Map<String, Widget Function(Control?, ControlViewModel)>?
      controlsMapping;
  final String route;
  final String sessionId;
  final bool isLoading;
  final bool isRegistered;
  final int reconnectingTimeout;
  final String error;
  final Size size;
  final Brightness displayBrightness;
  final Map<String, double> sizeBreakpoints;
  final Map<String, Control> controls;

  const AppState(
      {required this.pageUri,
      required this.assetsDir,
      required this.controlsMapping,
      required this.route,
      required this.sessionId,
      required this.isLoading,
      required this.isRegistered,
      required this.reconnectingTimeout,
      required this.error,
      required this.size,
      required this.sizeBreakpoints,
      required this.displayBrightness,
      required this.controls});

  factory AppState.initial() => const AppState(
      pageUri: null,
      assetsDir: "",
      controlsMapping: null,
      route: "",
      sessionId: "",
      isLoading: true,
      isRegistered: false,
      reconnectingTimeout: 0,
      error: "",
      size: Size(0, 0),
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
            type: "page",
            name: "",
            childIds: [],
            attrs: {})
      });

  AppState copyWith(
          {Uri? pageUri,
          String? assetsDir,
          String? route,
          String? sessionId,
          bool? isLoading,
          bool? isRegistered,
          int? reconnectingTimeout,
          String? error,
          Size? size,
          Map<String, double>? sizeBreakpoints,
          Brightness? displayBrightness,
          Map<String, Control>? controls,
          Map<String, Widget Function(Control?, ControlViewModel)>?
              controlsMapping}) =>
      AppState(
        pageUri: pageUri ?? this.pageUri,
        assetsDir: assetsDir ?? this.assetsDir,
        route: route ?? this.route,
        sessionId: sessionId ?? this.sessionId,
        isLoading: isLoading ?? this.isLoading,
        isRegistered: isRegistered ?? this.isRegistered,
        reconnectingTimeout: reconnectingTimeout ?? this.reconnectingTimeout,
        error: error ?? this.error,
        size: size ?? this.size,
        sizeBreakpoints: sizeBreakpoints ?? this.sizeBreakpoints,
        displayBrightness: displayBrightness ?? this.displayBrightness,
        controls: controls ?? this.controls,
        controlsMapping: controlsMapping ?? this.controlsMapping,
      );

  @override
  List<Object?> get props => [isLoading, error, sessionId, controls];
}
