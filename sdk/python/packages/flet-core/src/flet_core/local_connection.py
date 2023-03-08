import logging
from typing import List

import flet_core
from flet_core.connection import Connection
from flet_core.protocol import *

logger = logging.getLogger(flet_core.__name__)


class LocalConnection(Connection):
    def __init__(self):
        super().__init__()
        self._control_id = 1
        self._client_details = None

    def _create_register_web_client_response(self):
        assert self._client_details
        return ClientMessage(
            ClientActions.REGISTER_WEB_CLIENT,
            RegisterWebClientResponsePayload(
                session=SessionPayload(
                    id=self._client_details.sessionId,
                    controls={
                        "page": {
                            "i": "page",
                            "t": "page",
                            "p": "",
                            "c": [],
                            "route": self._client_details.pageRoute,
                            "width": self._client_details.pageWidth,
                            "height": self._client_details.pageHeight,
                            "windowwidth": self._client_details.windowWidth,
                            "windowheight": self._client_details.windowHeight,
                            "windowtop": self._client_details.windowTop,
                            "windowleft": self._client_details.windowLeft,
                            "pwa": self._client_details.isPWA,
                            "web": self._client_details.isWeb,
                            "platform": self._client_details.platform,
                        }
                    },
                ),
                appInactive=False,
                error="",
            ),
        )

    def _create_session_handler_arg(self):
        assert self._client_details
        return PageSessionCreatedPayload(
            pageName=self._client_details.pageName,
            sessionID=self._client_details.sessionId,
        )

    def _create_page_event_handler_arg(self, msg: ClientMessage):
        assert self._client_details
        web_event = PageEventFromWebPayload(**msg.payload)
        return PageEventPayload(
            pageName=self._client_details.pageName,
            sessionID=self._client_details.sessionId,
            eventTarget=web_event.eventTarget,
            eventName=web_event.eventName,
            eventData=web_event.eventData,
        )

    def _create_update_control_props_handler_arg(self, msg: ClientMessage):
        assert self._client_details
        return PageEventPayload(
            pageName=self._client_details.pageName,
            sessionID=self._client_details.sessionId,
            eventTarget="page",
            eventName="change",
            eventData=json.dumps(msg.payload["props"], separators=(",", ":")),
        )

    def _process_command(self, command: Command):
        logger.debug("_process_command: {}".format(command))
        if command.name == "get":
            return self._process_get_command(command.values)
        elif command.name == "add":
            return self._process_add_command(command)
        elif command.name == "set":
            return self._process_set_command(command.values, command.attrs)
        elif command.name == "remove":
            return self._process_remove_command(command.values)
        elif command.name == "clean":
            return self._process_clean_command(command.values)
        elif command.name == "invokeMethod":
            return self._process_invoke_method_command(command.values, command.attrs)
        elif command.name == "error":
            return self._process_error_command(command.values)
        raise Exception("Unsupported command: {}".format(command.name))

    def _process_add_command(self, command: Command):

        top_parent_id = command.attrs.get("to", "page")
        top_parent_at = int(command.attrs.get("at", "-1"))

        batch: List[Command] = []
        if len(command.values) > 0:
            batch.append(command)

        for sub_cmd in command.commands:
            sub_cmd.name = "add"
            batch.append(sub_cmd)

        ids = []
        controls = []
        controls_idx = {}

        i = 0
        for cmd in batch:
            assert len(cmd.values) > 0, "control type is not specified"
            control_type = cmd.values[0].lower()

            parent_id = ""
            parent_at = -1

            # find nearest parentID
            pi = i - 1
            while pi >= 0:
                if batch[pi].indent < cmd.indent:
                    parent_id = batch[pi].attrs.get("id", "")
                    break
                pi -= 1

            # parent wasn't found - use the topmost one
            if parent_id == "":
                parent_id = top_parent_id
                parent_at = top_parent_at

            id = cmd.attrs.get("id", "")
            if not id:
                id = "_{}".format(self._control_id)
                self._control_id += 1
                cmd.attrs["id"] = id

            ids.append(id)

            control = {"t": control_type, "i": id, "p": parent_id, "c": []}
            controls.append(control)
            controls_idx[id] = control

            if parent_at != -1:
                control["at"] = str(parent_at)
                top_parent_at += 1

            parent_control = controls_idx.get(parent_id)
            if parent_control:
                if parent_at != -1:
                    parent_control["c"].insert(parent_at, id)
                else:
                    parent_control["c"].append(id)

            system_attrs = ["id", "to", "from", "at", "t", "p", "i", "c"]
            for k, v in cmd.attrs.items():
                if k not in system_attrs and v:
                    control[k] = v

            i += 1

        return " ".join(ids), ClientMessage(
            ClientActions.ADD_PAGE_CONTROLS, AddPageControlsPayload(controls=controls)
        )

    def _process_set_command(self, values, attrs):
        assert len(values) == 1, '"set" command has wrong number of values'
        props = {"i": values[0]}
        for k, v in attrs.items():
            props[k] = v

        return "", ClientMessage(
            ClientActions.UPDATE_CONTROL_PROPS, UpdateControlPropsPayload(props=[props])
        )

    def _process_remove_command(self, values):
        assert len(values) > 0, '"remove" command has wrong number of values'
        return "", ClientMessage(
            ClientActions.REMOVE_CONTROL, RemoveControlPayload(ids=values)
        )

    def _process_clean_command(self, values):
        assert len(values) > 0, '"clean" command has wrong number of values'
        return "", ClientMessage(
            ClientActions.CLEAN_CONTROL, CleanControlPayload(ids=values)
        )

    def _process_error_command(self, values):
        assert len(values) == 1, '"error" command has wrong number of values'
        return "", ClientMessage(
            ClientActions.SESSION_CRASHED, SessionCrashedPayload(message=values[0])
        )

    def _process_invoke_method_command(self, values, attrs):
        # "invokeMethod", values=[method_id, method_name], attrs=arguments
        assert len(values) == 2, '"invokeMethod" command has wrong number of values'
        return "", ClientMessage(
            ClientActions.INVOKE_METHOD,
            InvokeMethodPayload(
                methodId=values[0], methodName=values[1], arguments=attrs
            ),
        )

    def _process_get_command(self, values: List[str]):
        assert len(values) == 2, '"get" command has wrong number of values'
        assert self._client_details
        ctrl_id = values[0]
        prop_name = values[1]
        r = ""
        if ctrl_id == "page":
            if prop_name == "route":
                r = self._client_details.pageRoute
            elif prop_name == "pwa":
                r = self._client_details.isPWA
            elif prop_name == "web":
                r = self._client_details.isWeb
            elif prop_name == "platform":
                r = self._client_details.platform
            elif prop_name == "width":
                r = self._client_details.pageWidth
            elif prop_name == "height":
                r = self._client_details.pageHeight
            elif prop_name == "windowWidth":
                r = self._client_details.windowWidth
            elif prop_name == "windowHeight":
                r = self._client_details.windowHeight
            elif prop_name == "windowTop":
                r = self._client_details.windowTop
            elif prop_name == "windowLeft":
                r = self._client_details.windowLeft
        return r, None
