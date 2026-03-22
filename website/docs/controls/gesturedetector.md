---
class_name: "flet.GestureDetector"
examples: "../../examples/controls/gesture_detector"
example_images: "../examples/controls/gesture_detector/media"
title: "GestureDetector"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/utility/gesturedetector)

[Solitaire game tutorial](https://flet.dev/docs/tutorials/python-solitaire)

### Handling events

<CodeExample path={frontMatter.examples + '/handling_events.py'} language="python" />

### Draggable containers

The following example demonstrates how a control can be freely dragged inside a Stack.

The sample also shows that GestureDetector can have a child control (blue container) as well as be nested
inside another control (yellow container) giving the same results.

<CodeExample path={frontMatter.examples + '/draggable_containers.py'} language="python" />

<Image src={frontMatter.example_images + '/draggable_containers.gif'} alt="draggable-containers" width="55%" />

### Window drag area

<CodeExample path={frontMatter.examples + '/window_drag_area.py'} language="python" />

### Mouse Cursors

<CodeExample path={frontMatter.examples + '/mouse_cursors.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />
