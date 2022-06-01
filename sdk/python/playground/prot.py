import json
import logging
import os
import sys

import flet
from flet.protocol import *


class CommandEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Command):
            return {
                "i": obj.indent,
                "n": obj.name,
                "v": obj.values,
                "a": obj.attrs,
                "c": obj.commands,
            }
        return json.JSONEncoder.default(self, obj)


cmd_3 = Command(0, "get", ["value5"], {"e": 5}, [])
cmd_1 = Command(0, "set", ["value1", "value2"], {"c": 3, "d": 4}, [cmd_3])
cmd = Command(0, "add", [], {"a": 1, "b": 3}, [cmd_1])

j = json.dumps(cmd, cls=CommandEncoder)
print(j)

print(sys.argv[0])
pathname = os.path.dirname(sys.argv[0])
print("path =", pathname)
print("full path =", os.path.abspath(pathname))
