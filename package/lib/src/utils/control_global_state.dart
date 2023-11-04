class ControlsGlobalState {
  final Map<String, ControlGlobalStateValue> _state = {};

  dynamic get(String controlId, String key) {
    return _state["$controlId $key"]?.value;
  }

  set(String controlId, String key, dynamic value, int widgetHashCode) {
    String gkey = "$controlId $key";
    ControlGlobalStateValue? state = _state[gkey];
    if (state == null) {
      state = ControlGlobalStateValue();
      _state[gkey] = state;
    }
    state.value = value;
    state.widgetHashCodes.add(widgetHashCode);
  }

  remove(String controlId, String key, int widgetHashCode) {
    String gkey = "$controlId $key";
    ControlGlobalStateValue? state = _state[gkey];
    if (state != null) {
      state.widgetHashCodes.remove(widgetHashCode);
      if (state.widgetHashCodes.isEmpty) {
        _state.remove(gkey);
      }
    }
  }
}

class ControlGlobalStateValue {
  dynamic value;
  final Set<int> widgetHashCodes = {};
}
