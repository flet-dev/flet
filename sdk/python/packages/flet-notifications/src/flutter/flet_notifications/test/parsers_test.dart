import 'package:flet_notifications/src/parsers.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group("parseActions", () {
    test("null yields an empty list", () {
      expect(parseActions(null), isEmpty);
    });

    test("parses defaults", () {
      final actions = parseActions([
        {"id": "open", "title": "Open"},
      ]);
      expect(actions, hasLength(1));
      expect(actions.single.id, "open");
      expect(actions.single.title, "Open");
      expect(actions.single.destructive, isFalse);
      expect(actions.single.foreground, isTrue);
      expect(actions.single.cancelNotification, isTrue);
      expect(actions.single.input, isNull);
    });

    test("parses flags and nested input", () {
      final actions = parseActions([
        {
          "id": "reply",
          "title": "Reply",
          "destructive": true,
          "foreground": false,
          "cancel_notification": false,
          "input": {
            "label": "Type here",
            "choices": ["Yes", "No"],
            "allow_free_form_input": false,
            "allowed_mime_types": ["image/png"],
          },
        },
      ]);
      final action = actions.single;
      expect(action.destructive, isTrue);
      expect(action.foreground, isFalse);
      expect(action.cancelNotification, isFalse);
      final input = action.input!;
      expect(input.label, "Type here");
      expect(input.choices, ["Yes", "No"]);
      expect(input.allowFreeFormInput, isFalse);
      expect(input.allowedMimeTypes, {"image/png"});
    });

    test("rejects non-list input", () {
      expect(() => parseActions("nope"), throwsFormatException);
    });

    test("rejects action without id", () {
      expect(
        () => parseActions([
          {"title": "Open"},
        ]),
        throwsFormatException,
      );
    });

    test("rejects action without title", () {
      expect(
        () => parseActions([
          {"id": "open"},
        ]),
        throwsFormatException,
      );
    });

    test("rejects non-map entry", () {
      expect(() => parseActions(["open"]), throwsFormatException);
    });
  });

  group("parseInput", () {
    test("null yields null", () {
      expect(parseInput(null), isNull);
    });

    test("defaults", () {
      final input = parseInput({})!;
      expect(input.label, "");
      expect(input.choices, isEmpty);
      expect(input.allowFreeFormInput, isTrue);
      expect(input.allowedMimeTypes, isEmpty);
    });

    test("rejects non-map", () {
      expect(() => parseInput("nope"), throwsFormatException);
    });
  });
  group("parseStyle", () {
    test("null yields null", () {
      expect(parseStyle(null), isNull);
    });

    test("big_text", () {
      final style = parseStyle({"_type": "big_text", "big_text": "long"})!;
      expect(style.type, "big_text");
      expect(style.bigText, "long");
    });

    test("big_text without text throws", () {
      expect(() => parseStyle({"_type": "big_text"}), throwsFormatException);
    });

    test("big_picture requires an image", () {
      expect(
        () => parseStyle({"_type": "big_picture"}),
        throwsFormatException,
      );
      final style = parseStyle({
        "_type": "big_picture",
        "image": {"file_path": "/tmp/x.png"},
      })!;
      expect(style.image!.filePath, "/tmp/x.png");
    });

    test("inbox", () {
      final style = parseStyle({
        "_type": "inbox",
        "lines": ["a", "b"],
      })!;
      expect(style.lines, ["a", "b"]);
      expect(
        () => parseStyle({"_type": "inbox", "lines": []}),
        throwsFormatException,
      );
    });

    test("messaging with person and messages", () {
      final style = parseStyle({
        "_type": "messaging",
        "person": {"name": "Ada"},
        "messages": [
          {
            "text": "hi",
            "timestamp": "2030-01-01T10:00:00",
            "person": {"name": "Ada"},
          },
        ],
        "conversation_title": "Chat",
        "group_conversation": true,
      })!;
      expect(style.person!.name, "Ada");
      expect(style.messages.single.text, "hi");
      expect(style.conversationTitle, "Chat");
      expect(style.groupConversation, isTrue);
    });

    test("messaging without person throws", () {
      expect(() => parseStyle({"_type": "messaging"}), throwsFormatException);
    });

    test("unknown style type throws", () {
      expect(() => parseStyle({"_type": "carousel"}), throwsFormatException);
    });
  });

  group("parseIcon", () {
    test("null yields null", () {
      expect(parseIcon(null), isNull);
    });

    test("drawable source", () {
      expect(
        parseIcon({"drawable_resource": "ic_star"})!.drawableResource,
        "ic_star",
      );
    });

    test("requires exactly one source", () {
      expect(() => parseIcon({}), throwsFormatException);
      expect(
        () => parseIcon({"drawable_resource": "ic", "file_path": "/x"}),
        throwsFormatException,
      );
    });

    test("base64 data is decoded", () {
      // "hi" in base64
      final icon = parseIcon({"data_base64": "aGk="})!;
      expect(icon.data, [104, 105]);
    });
  });

  group("parsePerson", () {
    test("null yields null", () {
      expect(parsePerson(null), isNull);
    });

    test("defaults", () {
      final person = parsePerson({"name": "Bob"})!;
      expect(person.name, "Bob");
      expect(person.bot, isFalse);
      expect(person.important, isFalse);
    });

    test("requires a name", () {
      expect(() => parsePerson({"key": "x"}), throwsFormatException);
    });
  });
}
