import 'dart:io';
import 'dart:typed_data';

Future<bool> isPrivateHost(String host) async {
  String? ip;
  var addr = InternetAddress.tryParse(host);
  if (addr == null) {
    InternetAddress ipAddr;
    try {
      ipAddr = (await InternetAddress.lookup(host)).first;
    } on SocketException {
      throw Exception("Cannot resolve host: $host");
    }
    if (ipAddr.rawAddress.length == 16) {
      return ipAddr.isLinkLocal || ipAddr.isLoopback;
    }
    ip = ipAddr.address;
  } else {
    ip = addr.address;
  }
  var f = ipToInt(ip);
  var private = [
    ["127.0.0.0", "255.0.0.0"],
    ["192.168.0.0", "255.255.0.0"],
    ["172.16.0.0", "255.240.0.0"],
    ["10.0.0.0", "255.0.0.0"],
  ];
  for (var net in private) {
    if ((f & ipToInt(net[1])) == ipToInt(net[0])) {
      return true;
    }
  }
  return false;
}

int ipToInt(String ip) {
  ByteData byteData = ByteData.view(
      Int8List.fromList(InternetAddress(ip).rawAddress.toList()).buffer);
  return byteData.getUint32(0, Endian.big);
}
