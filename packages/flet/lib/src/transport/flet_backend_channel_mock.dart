import 'dart:math';

import 'package:flutter/foundation.dart';

import '../protocol/message.dart';
import 'flet_backend_channel.dart';

class FletMockBackendChannel implements FletBackendChannel {
  FletBackendChannelOnMessageCallback onMessage;
  FletBackendChannelOnDisconnectCallback onDisconnect;

  FletMockBackendChannel(
      {required String address,
      required this.onDisconnect,
      required this.onMessage});
  @override
  bool get isLocalConnection => true;

  @override
  int get defaultReconnectIntervalMs => 500;

  @override
  Future connect() async {
    await Future.delayed(Duration(seconds: 1)); // Simulating async operation
    debugPrint("Connected to the Mock Flet backend channel");
    //_scenario_line_chart_simple();
    _scenario_register();
    //_scenario_test_services();
    //_scenario_call_window_methods();
  }

  _scenario_register() async {
    onMessage(Message(action: MessageAction.registerClient, payload: {
      "id": 1,
      "patch": {
        "show_semantics_debugger": false,
        "theme_mode": "system",
        // "platform": "ios",
        // "adaptive": true,
        "fonts": {
          "Kanit":
              "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
          "Open Sans": "/fonts/OpenSans-Regular.ttf"
        },
        "offstage": {
          "_c": "Offstage",
          "_i": 8,
          "controls": [
            {"_c": "Text", "_i": 20, "text": "OFF1"}
          ]
        },
        "_user_services": {"_c": "ServiceRegistry", "_i": 10, "services": []},
        "_page_services": {"_c": "ServiceRegistry", "_i": 11, "services": []},
        "views": [
          {
            "_c": "View",
            "_i": 20,
            "route": "/",
            "controls": [
              {"_c": "Text", "_i": 3, "text": "Hello, world"},
              {"_c": "Text", "_i": 4, "text": "Second line"},
              {
                "_c": "Row",
                "_i": 5,
                "controls": [
                  {"_c": "Text", "_i": 6, "text": "1st in Row"},
                  {"_c": "Text", "_i": 7, "text": "2nd in Row"}
                ]
              }
            ]
          }
        ]
      }
    }));

    await Future.delayed(Duration(seconds: 3));

    onMessage(Message(action: MessageAction.patchControl, payload: {
      "id": 2,
      "patch": {"width": 300, "height": 300}
    }));
  }

  _scenario_line_chart_simple() async {
    onMessage(Message(action: MessageAction.registerClient, payload: {
      "id": 1,
      "patch": {
        "views": [
          {
            "_c": "View",
            "_i": 20,
            "route": "/",
            "controls": [
              {
                "_c": "LineChart",
                "_i": 30,
                "line_bars": [
                  {
                    "_c": "LineChartBarData",
                    "_i": 31,
                    "spots": [
                      {"x": 1, "y": 1},
                      {"x": 2, "y": 0.5},
                      {"x": 3, "y": 0.6},
                      {"x": 4, "y": 0.7},
                      {"x": 5, "y": 0.2},
                      {"x": 6, "y": 0.4}
                    ]
                  },
                  {
                    "_c": "LineChartBarData",
                    "_i": 32,
                    "spots": [
                      {"x": 1, "y": 0.8},
                      {"x": 2, "y": 0.45},
                      {"x": 3, "y": 0.55},
                      {"x": 4, "y": 0.65},
                      {"x": 5, "y": 0.1},
                      {"x": 6, "y": 0.3}
                    ]
                  }
                ]
              },
            ]
          }
        ]
      }
    }));

    var random = Random();

    for (int i = 7; i < 100; i++) {
      var y = random.nextDouble();
      await Future.delayed(Duration(milliseconds: 200));

      onMessage(Message(action: MessageAction.patchControl, payload: {
        "id": 30,
        "patch": {
          "line_bars": {
            //"\$d": [1],
            "0": {
              "spots": {
                "\$d": [0],
                //"0": {"y": 0.8},
                "5": {
                  "\$a": {"x": i, "y": y}
                }
              }
            },
            "1": {
              "spots": {
                "\$d": [0],
                //"0": {"y": 0.8},
                "5": {
                  "\$a": {"x": i, "y": y - 0.1}
                }
              }
            }
          }
        }
      }));
    }

    await Future.delayed(Duration(seconds: 2));

    onMessage(Message(action: MessageAction.patchControl, payload: {
      "id": 30,
      "patch": {"a": 1}
    }));
  }

  _scenario_test_services() async {
    onMessage(Message(action: MessageAction.patchControl, payload: {
      "id": 11,
      "patch": {
        "services": {
          0: {
            "\$a": {"_c": "Clipboard", "_i": 31, "var1": "a"}
          }
        }
      }
    }));

    await Future.delayed(Duration(seconds: 2));

    onMessage(Message(action: MessageAction.patchControl, payload: {
      "id": 31,
      "patch": {"var1": "b", "var2": "c"}
    }));

    await Future.delayed(Duration(seconds: 2));

    onMessage(Message(action: MessageAction.invokeControlMethod, payload: {
      "id": 31,
      "name": "get",
      "args": {"a": 1, "b": false}
    }));

    await Future.delayed(Duration(seconds: 2));

    onMessage(Message(action: MessageAction.patchControl, payload: {
      "id": 10,
      "patch": {
        "services": {
          "\$d": [0]
        }
      }
    }));

    // onMessage(Message(
    //     action: MessageAction.invokeControlMethod,
    //     payload: {"id": 9, "name": "close", "args": {}}));
  }

  scenario_call_window_methods() async {
    onMessage(Message(
        action: MessageAction.invokeControlMethod,
        payload: {"id": 9, "name": "to_front", "args": {}}));

    await Future.delayed(Duration(seconds: 3));

    onMessage(Message(
        action: MessageAction.invokeControlMethod,
        payload: {"id": 9, "name": "close", "args": {}}));
  }

  scenario_1() async {
    onMessage(Message(action: MessageAction.patchControl, payload: {
      "id": 1,
      "patch": {
        "title": "Hello, title!",
        //"theme_mode": "light",
        "window": {"width": 1024},
        "views": {
          "0": {
            "controls": {
              "0": {"text": "Hello, world!!!"}
            }
          }
        }
      }
    }));

    await Future.delayed(Duration(seconds: 3));

    onMessage(Message(action: MessageAction.patchControl, payload: {
      "id": 1,
      "patch": {
        "fonts": {
          "aboreto":
              "https://github.com/google/fonts/raw/refs/heads/main/ofl/aboreto/Aboreto-Regular.ttf",
          "\$d": ["Open Sans"]
        },
        // "offstage": {
        //   "controls": {
        //     1: {
        //       "\$a": {"_c": "Text", "_i": 21, "text": "OFF2"}
        //     }
        //   }
        // },
        "views": {
          "0": {
            "controls": {
              "\$d": [0]
            }
          }
        }
      }
    }));

    await Future.delayed(Duration(seconds: 3));

    onMessage(Message(action: MessageAction.patchControl, payload: {
      "id": 8,
      "patch": {
        "controls": {
          1: {
            "\$a": {"_c": "Text", "_i": 21, "text": "ON2"}
          }
        }
      }
    }));

    await Future.delayed(Duration(seconds: 3));

    onMessage(Message(action: MessageAction.patchControl, payload: {
      "id": 5,
      "patch": {
        "controls": {
          "\$d": [1]
        }
      }
    }));
  }

  @override
  void send(Message message) {
    debugPrint("Send message: ${message.toJson()}");
  }

  @override
  void disconnect() {
    debugPrint("Disconnected from the Mock Flet backend channel");
  }
}
