import 'dart:typed_data';

int fnv1aHash(Uint8List bytes) {
  const int fnvOffset = 0x811C9DC5;
  const int fnvPrime = 0x01000193;

  int hash = fnvOffset;
  for (final byte in bytes) {
    hash ^= byte;
    hash = (hash * fnvPrime) & 0xFFFFFFFF; // 32-bit overflow
  }
  return hash;
}
