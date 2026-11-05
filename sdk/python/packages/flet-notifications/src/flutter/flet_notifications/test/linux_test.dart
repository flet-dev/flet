import 'package:flet_notifications/src/utils/details.dart'
    as notification_details;
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;
import 'package:flutter_test/flutter_test.dart';

import 'fakes.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  setUp(resetNotifications);

  test("Linux timeouts accept duration maps and retain sentinel values",
      () async {
    final cases = <(Object?, int)>[
      ({"seconds": 5}, 5000),
      // Without a timeout the notification server decides.
      (null, -1),
    ];
    for (final (timeout, expected) in cases) {
      final details = notification_details.parseNotificationDetails(
        actions: const [],
        details: {
          "options": {
            "linux": {"timeout": timeout}
          }
        },
      );
      expect(details.linux!.timeout.value, expected);
    }
  });

  test("Linux categories are selected by their freedesktop names", () {
    fln.LinuxNotificationCategory? category(String value) =>
        notification_details
            .parseNotificationDetails(
              actions: const [],
              details: {
                "options": {
                  "linux": {"category": value},
                },
              },
            )
            .linux!
            .category;
    expect(
        category("email.arrived"), fln.LinuxNotificationCategory.emailArrived);
    // Misspelled upstream; the freedesktop name stays the reliable key.
    expect(category("presence.offline"),
        fln.LinuxNotificationCategory.presenceOffile);
    expect(category("emailArrived"), isNull);
  });
}
