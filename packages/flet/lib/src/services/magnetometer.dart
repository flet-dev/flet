import 'package:sensors_plus/sensors_plus.dart';

import 'base_sensor.dart';

class MagnetometerService extends BaseSensorService<MagnetometerEvent> {
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
      "timestamp": event.timestamp,
    };
  }
}
