import 'package:sensors_plus/sensors_plus.dart';

import 'base_sensor.dart';

class GyroscopeService extends BaseSensorService<GyroscopeEvent> {
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
      "timestamp": event.timestamp,
    };
  }
}
