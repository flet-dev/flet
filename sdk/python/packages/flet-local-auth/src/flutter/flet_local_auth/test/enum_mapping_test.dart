import 'package:flutter_test/flutter_test.dart';
import 'package:local_auth/local_auth.dart';

import 'package:flet_local_auth/src/utils/local_auth.dart';

void main() {
  test('maps every BiometricType name', () {
    for (final type in BiometricType.values) {
      expect(parseBiometricTypeName(type), type.name);
    }
  });

  test('maps known LocalAuthExceptionCode values', () {
    for (final code in LocalAuthExceptionCode.values) {
      expect(parseLocalAuthExceptionCode(code.name), code);
    }
  });

  test('unknown LocalAuthExceptionCode falls back to unknownError', () {
    expect(
      parseLocalAuthExceptionCode('futureUpstreamCode'),
      LocalAuthExceptionCode.unknownError,
    );
  });
}
