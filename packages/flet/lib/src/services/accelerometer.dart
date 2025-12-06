import 'package:sensors_plus/sensors_plus.dart';

import 'base_sensor.dart';

class AccelerometerService extends BaseSensorService<AccelerometerEvent> {
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
      "timestamp": event.timestamp,
    };
  }
}
