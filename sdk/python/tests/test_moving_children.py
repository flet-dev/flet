import random

import flet as ft


def test_moving_children():
    c = ft.Stack()
    c._Control__uid = "0"
    for i in range(0, 10):
        c.controls.append(ft.Container())
        c.controls[i]._Control__uid = f"_{i}"

    index = []
    added_controls = []
    commands = []
    c.build_update_commands(index, added_controls, commands, False)

    def replace_controls(c):
        random.shuffle(c.controls)
        commands.clear()

        # print("=======")
        r = set()
        for ctrl in c.controls:
            # print(ctrl._Control__uid)
            r.add(ctrl._Control__uid)
        c.build_update_commands(index, added_controls, commands, False)
        for cmd in commands:
            if cmd.name == "add":
                for sub_cmd in cmd.commands:
                    # print("add", sub_cmd.attrs["id"], "at", cmd.attrs["at"])
                    r.add(sub_cmd.attrs["id"])
            elif cmd.name == "remove":
                for v in cmd.values:
                    # print("remove", v)
                    r.remove(v)
        # print(r)
        assert len(r) == len(c.controls)

    for i in range(0, 20):
        replace_controls(c)
