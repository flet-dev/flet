abstract class FletControlBackend {
  void updateControlState(String controlId, Map<String, String> props,
      {bool client = true, bool server = true});

  void triggerControlEvent(String controlId, String eventName,
      [String? eventData]);

  void subscribeMethods(String controlId,
      Future<String?> Function(String, Map<String, String>) methodHandler);

  void unsubscribeMethods(String controlId);
}
