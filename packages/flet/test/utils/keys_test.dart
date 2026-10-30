import 'package:flet/src/utils/keys.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  for (final (value, expected) in <(Object, Key)>[
    ('item', const ValueKey<String>('item')),
    (42, const ValueKey<int>(42)),
    (42.0, const ValueKey<double>(42.0)),
    (true, const ValueKey<bool>(true)),
  ]) {
    test('preserves ${expected.runtimeType} for raw and explicit keys', () {
      for (final encoded in [
        value,
        {'_type': 'value', 'value': value},
      ]) {
        final key = parseKey(encoded)!;
        expect(key, isA<ControlValueKey>());
        expect(valueKeyFromValue(key.value), expected);
      }
    });
  }

  test('does not collapse keys with different value types', () {
    expect(valueKeyFromValue(42), isNot(valueKeyFromValue('42')));
    expect(valueKeyFromValue(42), isNot(valueKeyFromValue(42.0)));
    expect(valueKeyFromValue(true), isNot(valueKeyFromValue('true')));
  });

  test('keeps scroll keys distinct from value keys', () {
    final key = parseKey({'_type': 'scroll', 'value': 'item'});
    expect(key, isA<ControlScrollKey>());
    expect(key, isNot(const ControlValueKey('item')));
    expect(parseKey(null), isNull);
  });
}
