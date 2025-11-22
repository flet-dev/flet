import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:sensors_plus/sensors_plus.dart';

import '../flet_service.dart';
import '../utils/numbers.dart';
import '../utils/time.dart';

abstract class _SensorStreamService<T> extends FletService {
  _SensorStreamService({required super.control});

  StreamSubscription<T>? _subscription;
  bool _enabled = true;
  bool _hasReadingSubscribers = false;
  bool _hasErrorSubscribers = false;
  Duration _interval = SensorInterval.normalInterval;
  bool _cancelOnError = true;

  Duration get defaultInterval => SensorInterval.normalInterval;

  String get eventName => "reading";

  Stream<T> sensorStream(Duration samplingPeriod);

  Map<String, dynamic> serializeEvent(T event);

  @override
  void init() {
    super.init();
    _updateConfig(forceRestart: true);
  }

  @override
  void update() {
    _updateConfig();
  }

  void _updateConfig({bool forceRestart = false}) {
    var enabled = control.getBool("enabled", true) ?? true;
    var interval =
        control.getDuration("interval", defaultInterval) ?? defaultInterval;
    if (interval.isNegative) {
      interval = defaultInterval;
    }
    var hasReadingSubscribers = control.getBool("on_$eventName") == true;
    var hasErrorSubscribers = control.getBool("on_error") == true;
    var cancelOnError = control.getBool("cancel_on_error", true) ?? true;

    if (forceRestart ||
        enabled != _enabled ||
        interval != _interval ||
        hasReadingSubscribers != _hasReadingSubscribers ||
        hasErrorSubscribers != _hasErrorSubscribers ||
        cancelOnError != _cancelOnError) {
      _enabled = enabled;
      _interval = interval;
      _hasReadingSubscribers = hasReadingSubscribers;
      _hasErrorSubscribers = hasErrorSubscribers;
      _cancelOnError = cancelOnError;
      _restart();
    }
  }

  void _restart() {
    _subscription?.cancel();
    _subscription = null;

    if (!_enabled || (!_hasReadingSubscribers && !_hasErrorSubscribers)) {
      return;
    }

    final samplingPeriod = _interval;
    try {
      _subscription = sensorStream(samplingPeriod).listen(
        (event) {
          if (_hasReadingSubscribers) {
            final payload = serializeEvent(event);
            control.triggerEvent(eventName, payload);
          }
        },
        onError: (error, stackTrace) {
          if (_hasErrorSubscribers) {
            control.triggerEvent("error",
                {"message": error?.toString() ?? "Unknown sensor error"});
          } else {
            debugPrint(
                "Error listening to ${control.type} sensor stream: $error");
          }
        },
        cancelOnError: _cancelOnError,
      );
    } catch (error) {
      debugPrint("Failed to initialize ${control.type} sensor stream: $error");
    }
  }

  @override
  void dispose() {
    _subscription?.cancel();
    _subscription = null;
    super.dispose();
  }
}

class AccelerometerService extends _SensorStreamService<AccelerometerEvent> {
  AccelerometerService({required super.control});

  @override
  Stream<AccelerometerEvent> sensorStream(Duration samplingPeriod) {
    return accelerometerEventStream(samplingPeriod: samplingPeriod);
  }

  @override
  Map<String, dynamic> serializeEvent(AccelerometerEvent event) {
    return {
      "x": event.x,
      "y": event.y,
      "z": event.z,
      "timestamp": event.timestamp.microsecondsSinceEpoch,
    };
  }
}

class UserAccelerometerService
    extends _SensorStreamService<UserAccelerometerEvent> {
  UserAccelerometerService({required super.control});

  @override
  Stream<UserAccelerometerEvent> sensorStream(Duration samplingPeriod) {
    return userAccelerometerEventStream(samplingPeriod: samplingPeriod);
  }

  @override
  Map<String, dynamic> serializeEvent(UserAccelerometerEvent event) {
    return {
      "x": event.x,
      "y": event.y,
      "z": event.z,
      "timestamp": event.timestamp.microsecondsSinceEpoch,
    };
  }
}

class GyroscopeService extends _SensorStreamService<GyroscopeEvent> {
  GyroscopeService({required super.control});

  @override
  Stream<GyroscopeEvent> sensorStream(Duration samplingPeriod) {
    return gyroscopeEventStream(samplingPeriod: samplingPeriod);
  }

  @override
  Map<String, dynamic> serializeEvent(GyroscopeEvent event) {
    return {
      "x": event.x,
      "y": event.y,
      "z": event.z,
      "timestamp": event.timestamp.microsecondsSinceEpoch,
    };
  }
}

class MagnetometerService extends _SensorStreamService<MagnetometerEvent> {
  MagnetometerService({required super.control});

  @override
  Stream<MagnetometerEvent> sensorStream(Duration samplingPeriod) {
    return magnetometerEventStream(samplingPeriod: samplingPeriod);
  }

  @override
  Map<String, dynamic> serializeEvent(MagnetometerEvent event) {
    return {
      "x": event.x,
      "y": event.y,
      "z": event.z,
      "timestamp": event.timestamp.microsecondsSinceEpoch,
    };
  }
}

class BarometerService extends _SensorStreamService<BarometerEvent> {
  BarometerService({required super.control});

  @override
  Stream<BarometerEvent> sensorStream(Duration samplingPeriod) {
    return barometerEventStream(samplingPeriod: samplingPeriod);
  }

  @override
  Map<String, dynamic> serializeEvent(BarometerEvent event) {
    return {
      "pressure": event.pressure,
      "timestamp": event.timestamp.microsecondsSinceEpoch,
    };
  }
}
