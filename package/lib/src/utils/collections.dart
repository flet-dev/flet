import 'dart:typed_data';

int arrayIndexOf(Uint8List haystack, Uint8List needle) {
  var len = needle.length;
  var limit = haystack.length - len;
  for (var i = 0; i <= limit; i++) {
    var k = 0;
    for (; k < len; k++) {
      if (needle[k] != haystack[i + k]) break;
    }
    if (k == len) return i;
  }
  return -1;
}
