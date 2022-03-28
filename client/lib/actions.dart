import 'protocol/append_control_props_request.dart';
import 'protocol/clean_control_payload.dart';
import 'protocol/page_controls_batch_payload.dart';
import 'protocol/remove_control_payload.dart';
import 'protocol/replace_page_controls_payload.dart';
import 'protocol/update_control_props_payload.dart';
import 'protocol/add_page_controls_payload.dart';
import 'protocol/app_become_inactive_payload.dart';
import 'protocol/register_webclient_response.dart';
import 'protocol/session_crashed_payload.dart';
import 'protocol/signout_payload.dart';

class RegisterWebClientAction {
  final RegisterWebClientResponse payload;
  RegisterWebClientAction(this.payload);
}

class AppBecomeInactiveAction {
  final AppBecomeInactivePayload payload;
  AppBecomeInactiveAction(this.payload);
}

class SessionCrashedAction {
  final SessionCrashedPayload payload;
  SessionCrashedAction(this.payload);
}

class SignoutAction {
  final SignoutPayload payload;
  SignoutAction(this.payload);
}

class AddPageControlsAction {
  final AddPageControlsPayload payload;
  AddPageControlsAction(this.payload);
}

class ReplacePageControlsAction {
  final ReplacePageControlsPayload payload;
  ReplacePageControlsAction(this.payload);
}

class PageControlsBatchAction {
  final PageControlsBatchPayload payload;
  PageControlsBatchAction(this.payload);
}

class UpdateControlPropsAction {
  final UpdateControlPropsPayload payload;
  UpdateControlPropsAction(this.payload);
}

class AppendControlPropsAction {
  final AppendControlPropsPayload payload;
  AppendControlPropsAction(this.payload);
}

class CleanControlAction {
  final CleanControlPayload payload;
  CleanControlAction(this.payload);
}

class RemoveControlAction {
  final RemoveControlPayload payload;
  RemoveControlAction(this.payload);
}
