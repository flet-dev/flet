---
title: "Animations"
---

import {CodeExample, Image} from '@site/src/components/crocodocs';

## Implicit animations

With implicit animations, you can animate a control property by setting a target value; whenever that target
value changes, the control animates the property from the old value to the new one.

Animation produces interpolated values between the old and the new value over the given *duration*.

By default, the animation is *linearly* increasing the animation value, however, a *curve* can be
applied to the animation which changes the value according to the provided curve.
For example, [`AnimationCurve.EASE_OUT_CUBIC`](../types/animationcurve.md#flet.AnimationCurve-EASE_OUT_CUBIC) curve increases the animation value quickly at the
beginning of the animation and then slows down until the target value is reached:

<video controls>
  <source src="https://flutter.github.io/assets-for-api-docs/assets/animation/curve_ease_out_cubic.mp4"/>
</video>

[`LayoutControl`](../controls/layoutcontrol.md) (and its subclasses) provides a number of `animate_{something}`
properties, described below, to enable implicit animation of its appearance:

* `animate_opacity`
* `animate_rotation`
* `animate_scale`
* `animate_offset`
* `animate_position`
* `animate` (`Container`)

`animate_*` properties could have one of the following values:

* Instance of [`Animation`](../types/animation.md) - allows configuring the duration and the curve of the
* animation, for example `animate_rotation=Animation(duration=300, curve=AnimationCurve.BOUNCE_OUT)`.
  See [this](https://api.flutter.dev/flutter/animation/Curves-class.html) Flutter docs on animation curves for possible values. Default is [`AnimationCurve.LINEAR`](../types/animationcurve.md#flet.AnimationCurve-LINEAR).
* `int` value - enables animation with specified duration in milliseconds and [`AnimationCurve.LINEAR`](../types/animationcurve.md#flet.AnimationCurve-LINEAR) curve.
* `bool` value - enables animation with the duration of 1000 milliseconds and [`AnimationCurve.LINEAR`](../types/animationcurve.md#flet.AnimationCurve-LINEAR) curve.

### Opacity animation

Setting control's `animate_opacity` to either `True`, number or an instance of `Animation` class (see above)
enables implicit animation of [`Control.opacity`](../controls/control.md#flet.Control-opacity) property.

<CodeExample path="controls/layout_control/animate_opacity.py" language="python" />

<Image src="../examples/controls/layout_control/media/animate_opacity.gif" alt="animate-opacity" width="55%" />

### Rotation animation

Setting control's `animate_rotation` to either `True`, number or an instance of `Animation` class (see above)
enables implicit animation of [`LayoutControl.rotate`](../controls/layoutcontrol.md#flet.LayoutControl-rotate) property.

<CodeExample path="controls/layout_control/animate_rotation.py" language="python" />

<Image src="../examples/controls/layout_control/media/animate_rotation.gif" alt="animate-rotation" width="55%" />

### Scale animation

Setting control's `animate_scale` to either `True`, number or an instance of `Animation` class (see above)
enables implicit animation of [`LayoutControl.scale`](../controls/layoutcontrol.md#flet.LayoutControl-scale) property.

<CodeExample path="controls/layout_control/animate_scale.py" language="python" />

<Image src="../examples/controls/layout_control/media/animate_scale.gif" alt="animate-scale" width="55%" />

### Offset animation

Setting control's `animate_offset` to either `True`, number or an instance of `Animation` class (see above)
enables implicit animation of [`LayoutControl.offset`](../controls/layoutcontrol.md#flet.LayoutControl-offset) property.

`offset` property is an instance of `Offset` class which specifies horizontal `x` and vertical `y`
offset of a control scaled to control's size. For example, an offset `Offset(-0.25, 0)` will result in
a horizontal translation of one quarter the width of the control.

Offset animation is used for various sliding effects:

<CodeExample path="controls/layout_control/animate_offset.py" language="python" />

<Image src="../examples/controls/layout_control/media/animate_offset.gif" alt="animate-offset" width="55%" />

### Position animation

Setting control's `animate_position` to either `True`, number or an instance of `Animation` class
(see above) enables implicit animation of the following `LayoutControl` properties:
[`left`](../controls/layoutcontrol.md#flet.LayoutControl-left), [`right`](../controls/layoutcontrol.md#flet.LayoutControl-right),
[`bottom`](../controls/layoutcontrol.md#flet.LayoutControl-bottom), [`top`](../controls/layoutcontrol.md#flet.LayoutControl-top).

Note:
    Positioning is effective only if the control is a descendant of one of the following:

    - [`Stack`](../controls/stack.md) control
    - [`Page.overlay`](../controls/page.md) list

<CodeExample path="controls/layout_control/animate_position.py" language="python" />

<Image src="../examples/controls/layout_control/media/animate_position.gif" alt="animate-position" width="55%" />

### Animate

Setting [`Container.animate`](../controls/container.md#flet.Container-animate) to [`AnimationValue`](../types/aliases.md#flet.AnimationValue)
enables implicit animation of container properties such as size, background color, border style, gradient.

<CodeExample path="controls/container/animate_1.py" language="python" />

<Image src="../examples/controls/container/media/animate_1.gif" alt="animate" width="55%" />

### Animated content switcher

[`AnimatedSwitcher`](../controls/animatedswitcher.md)  allows animated transition between two controls ('new' and 'old').

```python
import time

import flet as ft

def main(page: ft.Page):
    i = ft.Image(src="https://picsum.photos/150/150", width=150, height=150)

    def animate(e):
        sw.content = ft.Image(
            src=f"https://picsum.photos/150/150?{time.time()}", width=150, height=150
        )
        page.update()

    sw = ft.AnimatedSwitcher(
        i,
        transition=ft.AnimatedSwitcherTransition.SCALE,
        duration=500,
        reverse_duration=500,
        switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
        switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
    )

    page.add(
        sw,
        ft.Button("Animate!", on_click=animate),
    )

ft.run(main)
```

<Image src="../assets/cookbook/animations/animated-switcher.gif" alt="animated-switcher" width="55%" />

### Animation end callback

[`LayoutControl`](../controls/layoutcontrol.md) also has an
[`on_animation_end`](../controls/layoutcontrol.md#flet.LayoutControl-on_animation_end) event handler, which is called
when an animation is complete. It can be used to chain multiple animations.

Event's [`data`](../types/event.md#flet.Event-data) field/property contains the name of animation:

* `"opacity"`
* `"rotation"`
* `"scale"`
* `"offset"`
* `"position"`
* `"container"`

For example:

```python
ft.Container(
    content=ft.Text("Animate me!"),
    animate=ft.Animation(1000, ft.AnimationCurve.BOUNCE_OUT),
    on_animation_end=lambda e: print("Container animation end:", e.data)
)
```
