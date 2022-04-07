import copy
import dataclasses
import datetime
import time
from dataclasses import is_dataclass
from functools import partial
from typing import Any
from typing import Union

from beartype.typing import List
from flet import choicegroup
from flet import combobox
from flet import dropdown
from flet.button import Button
from flet.checkbox import Checkbox
from flet.choicegroup import ChoiceGroup
from flet.combobox import ComboBox
from flet.control import Control
from flet.control_event import ControlEvent
from flet.datepicker import DatePicker
from flet.dropdown import Dropdown
from flet.message import Message
from flet.panel import Panel
from flet.spinbutton import SpinButton
from flet.stack import Stack
from flet.text import Text
from flet.textbox import Textbox
from flet.toggle import Toggle

__all__ = ["Form"]


class Form(Stack):

    _step_for_floats = 0.1

    _float_button = partial(SpinButton, step=_step_for_floats)
    # _date_picker_with_edit = partial(DatePicker, allow_text_input=True)

    _standard_library_types = {
        "str": Textbox,
        "int": SpinButton,
        "float": _float_button,
        "Decimal": Textbox,
        "bool": Checkbox,
        "datetime": Textbox,
        "date": Textbox,
        "time": Textbox,
    }

    _pydantic_types = {
        "ConstrainedIntValue": SpinButton,
        "NegativeIntValue": SpinButton,
        "PositiveIntValue": SpinButton,
        "StrictIntValue": SpinButton,
        "ConstrainedFloatValue": _float_button,
        "NegativeFloatValue": _float_button,
        "PositiveFloatValue": _float_button,
        "StrictFloatValue": _float_button,
        "ConstrainedDecimalValue": _float_button,
        "StrictBoolValue": Checkbox,
        "EmailStrValue": Textbox,
        "PastDateValue": Textbox,
        "FutureDateValue": Textbox,
        # 'SecretStr': , not supported by flet yet
    }

    default_data_to_control_mapping = _standard_library_types
    default_data_to_control_mapping.update(_pydantic_types)

    # Alignments when not "top"
    _label_alignment_by_control_type = {
        DatePicker: "center",
        SpinButton: "center",
        Textbox: "center",
    }

    def __init__(
        self,
        value: Any,
        title: str = None,
        on_submit: callable = None,
        submit_button: Button = None,
        field_validation_default_error_message: str = "Check this value",
        form_validation_error_message: str = "Not all fields have valid values",
        autosave: bool = False,
        label_above: bool = False,
        label_alignment: str = "left",
        label_width: Union[int, str] = "30%",
        control_width: Union[int, str] = "100%",
        control_style: str = "normal",
        control_kwargs: dict = None,
        control_mapping: dict = None,
        toggle_for_bool: bool = False,
        padding: int = 20,
        gap: int = 10,
        width="min(600px, 90%)",
        threshold_for_dropdown=3,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.title = title
        self.field_validation_default_error_message = field_validation_default_error_message
        self.form_validation_error_message = form_validation_error_message
        self.autosave = autosave
        self.label_above = label_above
        self.label_alignment = label_alignment
        self.label_width = label_width
        self.control_width = control_width
        self.control_style = control_style
        self.control_kwargs = control_kwargs or {}
        self.threshold_for_dropdown = threshold_for_dropdown

        self.padding = padding
        self.gap = gap
        self.width = width

        self.data_to_control_mapping = self.default_data_to_control_mapping.copy()
        self.data_to_control_mapping.update(control_mapping or {})

        if toggle_for_bool:
            self.data_to_control_mapping["bool"] = Toggle
            self.data_to_control_mapping["StrictBoolValue"] = Toggle

        if type(value) is type:
            self._model = value
            try:
                self.value = self._model()
            except Exception as error:
                raise ValueError("Unable to instantiate form data with default values", error)
        else:
            self._model = type(value)
            self.value = value

        self.working_copy = self.autosave and self.value or copy.deepcopy(self.value)

        self._fields = {}
        self._messages = {}
        self._pydantic_fields = {}

        self.on_submit = getattr(submit_button, "on_click", on_submit)

        self.submit_button = submit_button or Button(text="OK", primary=True, icon="CheckMark")
        self.submit_button.on_click = self._submit

        self._form_not_valid_message = Message(value=self.form_validation_error_message, type="error", visible=False)

        self._create_controls()

    def _create_controls(self):
        title_controls = [Text(value=self.title, bold=True, size="xLarge")] if self.title else []
        input_controls = self._create_controls_for_annotations(self.working_copy, self._model, self.label_above)
        button_controls = [
            Stack(horizontal=True, horizontal_align="end", controls=[self._form_not_valid_message, self.submit_button])
        ]
        self.controls = title_controls + input_controls + button_controls

    def _create_controls_for_annotations(self, obj, cls, label_above, path: tuple = tuple()) -> List[Control]:
        return [
            self._create_control(attribute, attribute_type, getattr(obj, attribute), label_above, path)
            for attribute, attribute_type in cls.__annotations__.items()
        ]

    def _create_control(
        self,
        attribute: str,
        attribute_type: Any,
        value: Any,
        label_above: bool,
        path: tuple
    ) -> Control:

        # For unions, we consider only the first type annotation
        origin = getattr(attribute_type, "__origin__", None)
        if origin and origin == Union:
            attribute_type = attribute_type.__args__[0]

        control_data = ControlData(
            attribute=attribute,
            attribute_type=attribute_type,
            value=value,
            label_text=attribute.replace("_", " ").capitalize(),
            placeholder="",
            error_message=self.field_validation_default_error_message,
            kwargs=self.control_kwargs.get(attribute, {}),
        )

        control_data = self._apply_dataclass_overrides(control_data, path)
        control_data = self._apply_pydantic_overrides(control_data, path)

        # handle_change_func = partial(self._handle_field_submit_event, path + (attribute,))

        is_list = False

        if origin == list and len(attribute_type.__args__) == 1:
            actual_type = attribute_type.__args__[0]
            control_data.attribute_type = actual_type
            if type(actual_type).__name__ == "EnumMeta":
                control = self._create_choice_control(control_data, multiple=True)
            else:
                control = self._create_list_control(control_data)
                is_list = True
        elif type(attribute_type).__name__ == "EnumMeta":
            control = self._create_choice_control(control_data)
        elif self._is_complex_object(attribute_type):
            control = self._create_complex_control(control_data, path)
        else:
            control = self._create_basic_control(control_data)

        if self.control_style == "line":
            try:
                control.underlined = True
                control.borderless = True
            except AttributeError:
                pass

        self._fields[path + (attribute,)] = control

        controls = [control]

        if not self._is_complex_object(attribute_type):
            message = Message(value=control_data.error_message, type="error", visible=False)
            self._messages[path + (attribute,)] = message
            controls.append(message)

        control_stack = Stack(
            controls=controls,
            width=self.control_width,
            vertical_align="center",
        )

        if hasattr(control, "label"):
            control.label = None

        label_text = Text(
            value=control_data.label_text,
            width="100%",
            bold=True,
            align=self.label_alignment,
            vertical_align=self._label_alignment_by_control_type.get(type(control), "top"),
        )

        label_stack = Stack(horizontal=True, controls=[label_text])
        if not label_above:
            label_stack.width = self.label_width

        if is_list:
            label_stack.controls.append(Button(icon="Add", on_click=control.list_add))

        attribute_stack = Stack(
            horizontal_align="end",
            controls=[
                label_stack,
                control_stack,
            ],
        )
        if label_above:
            attribute_stack.gap = 0

        if not label_above:
            attribute_stack.horizontal = True

        return attribute_stack

    def _is_complex_object(self, object_type: type):
        return is_dataclass(object_type) or hasattr(object_type, "__fields__")

    def _apply_dataclass_overrides(self, control_data, path):
        custom_kwargs = {}
        if hasattr(self._model, "__dataclass_fields__"):
            dataclass_field = self.value.__dataclass_fields__.get(control_data.attribute)
            if dataclass_field:
                metadata = dataclass_field.metadata
                if metadata:
                    custom_kwargs = metadata.get('flet', {})

        if custom_kwargs:
            control_data.kwargs.update(custom_kwargs)

        return control_data

    def _apply_pydantic_overrides(self, control_data, path):
        pydantic_field = (
            hasattr(self._model, "__fields__") and self.value.__fields__.get(control_data.attribute) or None
        )

        if pydantic_field:
            self._pydantic_fields[path + (control_data.attribute,)] = pydantic_field

            label_text = pydantic_field.field_info.title
            if label_text:
                control_data.label_text = label_text

            placeholder = pydantic_field.field_info.description
            if placeholder:
                control_data.placeholder = placeholder
                control_data.error_message = placeholder

            extra = pydantic_field.field_info.extra
            if extra:
                control_data.kwargs.update(extra.get('flet', {}))

        return control_data

    def _create_basic_control(self, control_data):
        control_type = self.data_to_control_mapping.get(control_data.attribute_type.__name__, Textbox)
        control = control_type(value=control_data.value, **control_data.kwargs)
        if control_type in (DatePicker, Dropdown, Textbox):
            control.placeholder = control_data.placeholder
        return control

    def _create_choice_control(self, control_data, multiple=False):
        enum_type = control_data.attribute_type

        if multiple:
            return ComboBox(
                multi_select=True,
                options=[combobox.Option(key=option.value, text=option.value.title()) for option in enum_type],
                value=[enum_type(value).value for value in control_data.value],
            )

        if len(enum_type) > self.threshold_for_dropdown:
            control_type = Dropdown
            option_type = dropdown.Option
        else:
            control_type = ChoiceGroup
            option_type = choicegroup.Option

        value = enum_type(control_data.value).value

        return control_type(
            options=[option_type(key=option.value, text=option.value.title()) for option in enum_type],
            value=value,
        )

    def _create_complex_control(self, control_data, path):
        return Stack(
            width="100%",
            controls=self._create_controls_for_annotations(
                control_data.value, control_data.attribute_type, label_above=True, path=path + (control_data.attribute,)
            ),
        )

    def _create_list_control(self, control_data: "ControlData") -> "ListControl":
        if self._is_complex_object(control_data.attribute_type):
            return ListControl(
                value=control_data.value,
                attribute_type=control_data.attribute_type,
                form=self,
                simple=False,
                panel_width=self.width,
            )
        else:
            return ListControl(
                value=control_data.value,
                attribute_type=control_data.attribute_type,
                form=self,
            )

    def _handle_field_submit_event(self, attribute, event):
        self._validate_value(attribute)

    def _validate_value(self, attribute: str) -> bool:
        is_valid = True
        control = self._fields[attribute]
        message = self._messages[attribute]
        message.value = self.field_validation_default_error_message

        if type(control) is Stack:
            return True
        elif type(control) is DatePicker and type(control.value) is datetime.datetime:
            datetime_tuple = control.value.timetuple()
            if datetime_tuple[3:6] == (0, 0, 0):
                control.value = datetime.date(datetime_tuple[:3])

        pydantic_field = self._pydantic_fields.get(attribute)
        if pydantic_field:
            description = pydantic_field.field_info.description
            if description:
                message.value = description
            value, error = pydantic_field.validate(
                control.value,
                self.working_copy.dict(),
                loc=attribute,
                cls=self._model,
            )
            if error:
                is_valid = False
                message.value = str(error.exc).capitalize()
            else:
                # Validation can change the value, update control
                if type(value) is datetime.date:
                    value = value.isoformat()
                control.value = value

        if is_valid:
            obj = self.working_copy
            for attribute_name in attribute[:-1]:
                obj = getattr(obj, attribute_name)
            try:
                setattr(obj, attribute[-1], control.value)
            except ValueError:
                is_valid = False

        self._messages[attribute].visible = not is_valid
        self.page.update()
        return is_valid

    def _submit(self, e):
        if not all(self._validate_value(attribute) for attribute in self._fields):
            self.submit_button.primary = False
            self.submit_button.icon = "Cancel"
            self.page.update()
            time.sleep(5)
            self.submit_button.primary = True
            self.submit_button.icon = "CheckMark"
            self.page.update()
        else:
            if not self.autosave:
                self.value.__dict__.update(self.working_copy.__dict__)
            if self.on_submit:
                custom_event = ControlEvent(self.submit_button, "submit", None, self, self.page)
                self.on_submit(custom_event)


class ListControl(Stack):

    def __init__(self, value, attribute_type, form, simple=True, panel_width=None, gap=0, **kwargs):
        super().__init__(**kwargs)
        self.form = form
        self.simple = simple
        self.gap = gap
        self.value = value
        self.attribute_type = attribute_type
        self.panel_width = panel_width
        self.panel = None
        self.panel_holder = Stack()
        self.update()

    def update(self):
        if self.simple:
            self.controls = [
                Stack(
                    gap=2,
                    horizontal=True,
                    controls=[
                        self.get_value_control(item, index),
                        Button(height="100%", icon="Delete", on_click=partial(self.list_delete, index)),
                    ],
                )
                for index, item in enumerate(self.value)
            ]
        else:
            self.controls = [
                Stack(
                    gap=0,
                    horizontal=True,
                    # border_top="1px solid lightgray",
                    controls=[
                        Button(width="100%", text=str(item), action=True, on_click=partial(self.list_selection, item)),
                        Button(height="100%", icon="Delete", on_click=partial(self.list_delete, index)),
                        Button(height="100%", icon="ChevronRight", on_click=partial(self.list_selection, item)),
                    ],
                )
                for index, item in enumerate(self.value)
            ] + [self.panel_holder]

    def get_value_control(self, item: Any, index: int) -> Control:
        control_data = ControlData(
            attribute="",
            attribute_type=self.attribute_type,
            value=item,
            label_text="",
            placeholder="",
            error_message="",
            kwargs={},
        )
        control = self.form._create_basic_control(control_data)
        control.width = "100%"
        control.on_change = partial(self.list_change, index)
        return control

    def list_change(self, index, event):
        self.value[index] = event.control.value

    def list_selection(self, item, event):
        subform = Form(value=item, on_submit=self._handle_subform_submit_event)
        self.panel = Panel(
            open=True,
            type='custom',
            auto_dismiss=False,
            light_dismiss=True,
            title=type(item).__name__.capitalize(),
            controls=[subform],
            on_dismiss=self._handle_subform_dismiss_event
        )
        if self.panel_width:
            self.panel.width = self.panel_width
        self.panel_holder.controls.append(self.panel)
        self.panel_holder.update()

    def list_delete(self, index, event):
        del self.value[index]
        self.update()
        self.page.update()

    def list_add(self, event):
        self.value.append(self.attribute_type())
        self.update()
        self.page.update()
        self.list_selection(self.value[-1], event)

    def _handle_subform_submit_event(self, event):
        self.update()
        self.page.update()
        self._handle_subform_dismiss_event(event)

    def _handle_subform_dismiss_event(self, event):
        self.panel_holder.controls.pop()
        self.panel_holder.update()


@dataclasses.dataclass
class ControlData:
    attribute: str
    attribute_type: Any
    value: Any
    label_text: str
    placeholder: str
    error_message: str
    kwargs: dict
