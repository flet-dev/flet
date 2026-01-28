---
title: ToDo Tutorial
examples: ../../examples/tutorials/todo
---

In this tutorial we will show you, step-by-step, how to create a To-Do app in Python using Flet framework and then publish it as a desktop, mobile or web app. The app is a single-file console program of just
[163 lines (formatted!) of Python code](https://github.com/flet-dev/flet/blob/main/sdk/python/examples/apps/todo/todo.py),
yet it is a multi-platform application with rich, responsive UI:

{{ image("../examples/tutorials/todo/media/complete-demo-web.gif", alt="complete-demo-web.gif", width="80%") }}


You can see the live demo [here](https://examples.flet.dev/todo/).

We chose a To-Do app for the tutorial, because it covers all of the basic concepts you would need to create a Flet app: building a page layout, adding controls, handling events, displaying and editing lists, making reusable UI components, and publishing options.

The tutorial consists of the following steps:

* [Getting started with Flet](#getting-started-with-flet)
* [Adding page controls and handling events](#adding-page-controls-and-handling-events)
* [View, edit and delete list items](#view-edit-and-delete-list-items)
* [Filtering list items](#filtering-list-items)
* [Final touches](#final-touches)
* [Publishing the app](#publishing-the-app)

## Getting started with Flet

To create a multi-platform app in Python with Flet, you don't need to know HTML,
CSS or JavaScript, but you do need a basic knowledge of Python and object-oriented
programming.

Before you can create your first Flet app, you need to
[setup your development environment](../getting-started/installation.md), which requires Python 3.10 or above and `flet` package.

Once you have Flet installed, let's [create](../getting-started/create-flet-app.md) a simple hello-world app.

Create `hello.py` with the following contents:

```python title="hello.py"
--8<-- "{{ examples }}/hello.py"
```

Run this app and you will see a new window with a greeting:

{{ image("../examples/tutorials/todo/media/hello-world.png", alt="hello-world", width="80%") }}


## Adding page controls and handling events

To start, we'll need a [`TextField`][flet.TextField] for entering a task name, and "+"
[`FloatingActionButton`][flet.FloatingActionButton] with an event handler that will display a [`Checkbox`][flet.Checkbox] with a new task.

Create `todo.py` with the following contents:

```python title="todo.py"
--8<-- "{{ examples }}/step_1.py"
```

Run the app and you should see a page like this:

{{ image("../examples/tutorials/todo/media/app-1.png", alt="app-1", width="80%") }}


### Page layout

Now let's make the app look nice! We want the entire app to be at the top center of the page, taking up 600 px width. The TextField and the "+" button should be aligned horizontally, and take up full app width:

{{ image("../examples/tutorials/todo/media/diagram-1.svg", alt="diagram-1", width="80%") }}


[`Row`][flet.Row]  is a control that is used to lay its children controls out horizontally on a page.
[`Column`][flet.Column] is a control that is used to lay its children controls out vertically on a page.

Replace `todo.py` contents with the following:

```python title="hello.py"
--8<-- "{{ examples }}/step_2.py"
```

Run the app and you should see a page like this:

{{ image("../examples/tutorials/todo/media/app-2.png", alt="app-2", width="80%") }}


### Reusable UI components

While we could continue writing our app in the `main` function, the best practice would be to create a [reusable UI component](../cookbook/custom-controls.md). Imagine you are working on an app header, a side menu, or UI that will be a part of a larger project. Even if you can't think of such uses right now, we still recommend creating all your Flet apps with composability and reusability in mind.

To make a reusable To-Do app component, we are going to encapsulate its state and presentation logic in a separate class:

```python title="todo.py"
--8<-- "{{ examples }}/step_3.py"
```

/// details | Try this out!
    type: example
Try adding two `TodoApp` components to the page:

```python
# create application instance
app1 = TodoApp()
app2 = TodoApp()

# add application's root control to the page
page.add(app1, app2)
```
///

## View, edit and delete list items

In the [previous step](#adding-page-controls-and-handling-events), we created a basic To-Do app with task items shown as checkboxes.
Let's improve the app by adding "Edit" and "Delete" buttons next to a task name. The "Edit" button will switch a task item to edit mode.

{{ image("../examples/tutorials/todo/media/diagram-2.svg", alt="diagram-2", width="80%") }}


Each task item is represented by two rows: `display_view` row with Checkbox, "Edit" and "Delete" buttons and `edit_view` row with TextField and "Save" button. `view` column serves as a container for both `display_view` and `edit_view` rows.

To encapsulate task item views and actions, we introduced a new `Task` class.

Additionally, we changed `TodoApp` class to create and hold `Task` instances when the "Add" button is clicked.

For "Delete" task operation, we implemented `task_delete()` method in `TodoApp` class which accepts task control instance as a parameter.

Then, we passed a reference to `task_delete` method into Task constructor and called it on "Delete" button event handler.

```python title="todo.py"
--8<-- "{{ examples }}/step_4.py"
```

Run the app and try to edit and delete tasks:

{{ image("../examples/tutorials/todo/media/view-edit-delete.gif", alt="view-edit-delete", width="80%") }}


## Filtering list items

We already have a functional To-Do app where we can create, edit, and delete tasks.
To be even more productive, we want to be able to filter tasks by their status.

Copy the entire code for this step from [here](https://github.com/flet-dev/flet/blob/main/sdk/python/examples/tutorials/todo/todo.py).
Below we will explain the changes we've done to implement filtering.

`Tabs` control is used to display filter:

```python title="todo.py"
# ...

class TodoApp(ft.Column):
    # application's root control is a Column containing all other controls
    def init(self):
        self.new_task = ft.TextField(hint_text="Whats needs to be done?", expand=True)
        self.tasks = ft.Column()

        self.filter = ft.TabBar(
            scrollable=False,
            tabs=[
                ft.Tab(label="all"),
                ft.Tab(label="active"),
                ft.Tab(label="completed"),
            ],
        )

        self.filter_tabs = ft.Tabs(
            length=3,
            selected_index=0,
            on_change=lambda e: self.update(),
            content=self.filter,
        )

    # ...
```

To display different lists of tasks depending on their statuses, we could maintain three lists with "All", "Active" and "Completed" tasks. We, however, chose an easier approach where we maintain the same list and only change a task's visibility depending on its status.

In `TodoApp` class we overrided [`before_update()`](../cookbook/custom-controls.md#before_update) method alled every time when the control is being updated. It iterates through all the tasks and updates their `visible` property depending on the status of the task:

```python title="todo.py"
class TodoApp(ft.Column):

    # ...

    def before_update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        for task in self.tasks.controls:
            task.visible = (
                status == "all"
                or (status == "active" and task.completed == False)
                or (status == "completed" and task.completed)
            )
```

Filtering should occur when we click on a tab or change a task status. `TodoApp.before_update()` method is called when Tabs selected value is changed or Task item checkbox is clicked:

```python title="todo.py"
class TodoApp(ft.Column):

    # ...

    def tabs_changed(self, e):
        self.update()

    def task_status_change(self, e):
        self.update()


    def add_clicked(self, e):
        task = Task(
            task_name=self.new_task.value,
            on_status_change=self.task_status_change,
            on_delete=self.task_delete,
        )
        self.tasks.controls.append(task)
        self.new_task.value = ""
        self.update()
    # ...

class Task(ft.Column):
    task_name: str = ""
    on_status_change: Callable[[], None] = field(default=lambda: None)
    on_delete: Callable[["Task"], None] = field(default=lambda task: None)

    # ...

    def status_changed(self, e):
        self.completed = self.display_task.value
        self.task_status_change()
```

Run the app and try filtering tasks by clicking on the tabs:

{{ image("../examples/tutorials/todo/media/filtering.gif", alt="filtering", width="80%") }}

Our Todo app is almost complete now. As a final touch, we will add a footer (`Column` control) displaying the number of incomplete tasks (`Text` control) and a "Clear completed" button.

/// details | Full code
    type: example
```python
--8<-- "../../examples/tutorials/todo/todo.py"
```
///

{{ image("../examples/tutorials/todo/media/app-4.png", alt="app-4", width="80%") }}


## Publishing the app

Congratulations! You have created your first Python app with Flet, and it looks awesome!

Now it's time to share your app with the world!

[Follow these instructions](../publish/index.md) to publish your Flet app as a mobile, desktop or web app.

## Summary

In this tutorial, you have learnt how to:

* Create a simple Flet app;
* Work with [Reusable UI components](../cookbook/custom-controls.md);
* Design UI layout using [`Column`][flet.Column] and [`Row`][flet.Row] controls;
* Work with lists: view, edit and delete items, filtering;
* [Publish](../publish/index.md) your Flet app to multiple platforms;

For further reading you can explore [controls](../controls/index.md) and [examples](https://github.com/flet-dev/flet/tree/main/sdk/python/examples).
