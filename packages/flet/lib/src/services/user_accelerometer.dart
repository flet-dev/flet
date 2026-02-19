import 'package:sensors_plus/sensors_plus.dart';

import 'base_sensor.dart';

class UserAccelerometerService
    extends BaseSensorService<UserAccelerometerEvent> {
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
