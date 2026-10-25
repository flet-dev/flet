import 'dart:typed_data';

import 'package:flet_notifications/src/platforms/android_styles.dart';
import 'package:flet_notifications/src/utils/errors.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;
import 'package:flutter_test/flutter_test.dart';

void main() {
  test("picture and inbox styles retain native content and optional fields",
      () {
    final picture = parseStyle({
      "_type": "big_picture",
      "image": {
        "_type": "bytes",
        "data": Uint8List.fromList([1, 2, 3]),
      },
      "large_icon": {"_type": "drawable", "name": "avatar"},
      "content_title": "Photo",
      "summary_text": "Summary",
    }) as fln.BigPictureStyleInformation;
    expect((picture.bigPicture as fln.ByteArrayAndroidBitmap).data, [1, 2, 3]);
    expect((picture.largeIcon as fln.DrawableResourceAndroidBitmap).data,
        "avatar");
    expect(picture.contentTitle, "Photo");
    expect(picture.summaryText, "Summary");
    final inbox = parseStyle({
      "_type": "inbox",
      "lines": ["First", "Second"],
      "content_title": "Inbox",
      "summary_text": "Two messages",
    }) as fln.InboxStyleInformation;
    expect(inbox.lines, ["First", "Second"]);
    expect(inbox.contentTitle, "Inbox");
    expect(inbox.summaryText, "Two messages");
  });

  test("messaging retains participants, icon sources and timestamp instants",
      () {
    final style = parseStyle({
      "_type": "messaging",
      "person": {
        "name": "Me",
        "key": "self",
        "bot": true,
        "icon": {"_type": "file", "path": "/data/me.png"}
      },
      "conversation_title": "Chat",
      "group_conversation": true,
      "messages": [
        {
          "text": "Hello",
          "timestamp": DateTime.parse("2030-06-01T14:00:00+02:00"),
          "person": {
            "name": "Alex",
            "uri": "mailto:alex@example.com",
            "important": true,
            "icon": {"_type": "content_uri", "uri": "content://avatar/1"}
          },
        }
      ],
    }) as fln.MessagingStyleInformation;
    expect(style.person.key, "self");
    expect(style.person.bot, isTrue);
    expect((style.person.icon as fln.BitmapFilePathAndroidIcon).data,
        "/data/me.png");
    expect(style.conversationTitle, "Chat");
    expect(style.groupConversation, isTrue);
    final message = style.messages!.single;
    expect(message.text, "Hello");
    expect(message.timestamp.toUtc(), DateTime.utc(2030, 6, 1, 12));
    expect(message.person!.name, "Alex");
    expect(message.person!.important, isTrue);
    expect(message.person!.uri, "mailto:alex@example.com");
    expect(message.person!.icon, isA<fln.ContentUriAndroidIcon>());
    final empty = parseStyle({
      "_type": "messaging",
      "person": {"name": "Me"}
    }) as fln.MessagingStyleInformation;
    expect(empty.messages, isEmpty);
    expect(empty.groupConversation, isFalse);
    expect(parseStyle(null), isNull);
  });

  test("malformed nested style data produces a style-specific error", () {
    for (final value in [
      {
        "_type": "big_picture",
        "image": {"_type": "content_uri", "uri": "content://image/1"}
      },
      {
        "_type": "big_picture",
        "image": {"_type": "bytes", "data": "AQID"}
      },
      {
        "_type": "big_picture",
        "image": {"_type": "asset", "path": "a.png"}
      },
      {
        "_type": "big_picture",
        "image": {"path": "/a"}
      },
      {
        "_type": "messaging",
        "person": {"name": "Me"},
        "messages": [
          {
            "text": "Hello",
            "timestamp": "invalid",
            "person": {"name": "Alex"}
          }
        ]
      },
      {
        "_type": "messaging",
        "person": {"name": "Me"},
        "messages": "invalid"
      },
      {"_type": "big_text", "big_text": "Hello", "content_title": 42},
      {
        "_type": "inbox",
        "lines": [42]
      },
    ]) {
      expect(
          () => parseStyle(value),
          throwsA(isA<NotificationException>().having(
              (e) => e.code, "code", NotificationErrorCode.invalidArgument)));
    }
  });
}
