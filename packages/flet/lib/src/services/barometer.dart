import 'package:sensors_plus/sensors_plus.dart';

import 'base_sensor.dart';

class BarometerService extends BaseSensorService<BarometerEvent> {
  BarometerService({required super.control});

  @override
  Stream<BarometerEvent> sensorStream(Duration samplingPeriod) {
    return barometerEventStream(samplingPeriod: samplingPeriod);
  }

  @override
  Map<String, dynamic> serializeEvent(BarometerEvent event) {
    return {
      "pressure": event.pressure,
      "timestamp": event.timestamp,
    };
  }
}
