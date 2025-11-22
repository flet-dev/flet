import 'dart:typed_data';

/// Returns the first index of `needle` inside `haystack`, or `-1` if not found.
///
/// This performs a naive byte-wise search (O(haystack.length * needle.length)
/// worst-case). If `needle` is empty the function returns `0`.
///
/// Example:
/// ```dart
/// arrayIndexOf(Uint8List.fromList([1, 2, 3, 4]), Uint8List.fromList([2, 3])) == 1;
/// ```
int arrayIndexOf(Uint8List haystack, Uint8List needle) {
  final len = needle.length;
  if (len == 0) return 0;
  final limit = haystack.length - len;
  for (var i = 0; i <= limit; i++) {
    var k = 0;
    for (; k < len; k++) {
      if (needle[k] != haystack[i + k]) break;
    }
    if (k == len) return i;
  }
  return -1;
}
