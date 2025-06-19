from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control

__all__ = ["AdaptiveControl"]


@control(kw_only=True)
class AdaptiveControl(Control):
    """
    Adaptive controls are either Material design controls that have their Cupertino
    analogs or container controls.
    """
    adaptive: Optional[bool] = None
    """
    `adaptive` property can be specified for a control in the following cases:
    
    * A control has matching Cupertino control with similar functionality/presentation 
    and graphics as expected on iOS/macOS. In this case, if `adaptive` is `True`, 
    either Material or Cupertino control will be created depending on the target 
    platform.  

    These controls have their Cupertino analogs and `adaptive` property:    
        * [`AlertDialog`](https://flet.dev/docs/controls/alertdialog)
        * [`AppBar`](https://flet.dev/docs/controls/appbar)
        * [`Checkbox`](https://flet.dev/docs/controls/checkbox)
        * [`ListTile`](https://flet.dev/docs/controls/listtile)
        * [`NavigationBar`](https://flet.dev/docs/controls/navigationbar)
        * [`Radio`](https://flet.dev/docs/controls/radio)
        * [`Slider`](https://flet.dev/docs/controls/slider)
        * [`Switch`](https://flet.dev/docs/controls/switch)

    * A control has child controls. In this case `adaptive` property value is passed on 
    to its children that don't have their `adaptive` property set. 

    The following container controls have `adaptive` property: 
        * [`Card`](https://flet.dev/docs/controls/card)
        * [`Column`](https://flet.dev/docs/controls/column)
        * [`Container`](https://flet.dev/docs/controls/container)
        * [`Dismissible`](https://flet.dev/docs/controls/dismissible)
        * [`ExpansionPanel`](https://flet.dev/docs/controls/expansionpanel)
        * [`FletApp`](https://flet.dev/docs/controls/fletapp)
        * [`GestureDetector`](https://flet.dev/docs/controls/gesturedetector)
        * [`GridView`](https://flet.dev/docs/controls/gridview)
        * [`ListView`](https://flet.dev/docs/controls/listview)
        * [`Page`](https://flet.dev/docs/controls/page)
        * [`Row`](https://flet.dev/docs/controls/row)
        * [`SafeArea`](https://flet.dev/docs/controls/safearea)
        * [`Stack`](https://flet.dev/docs/controls/stack)
        * [`Tabs`](https://flet.dev/docs/controls/tabs)
        * [`View`](https://flet.dev/docs/controls/view)
    """
