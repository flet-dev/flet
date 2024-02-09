url='https://raw.githubusercontent.com/flutter/flutter/master/packages/flutter/lib/src/material/icons.dart'
output_file="material_icons_python.txt"

curl -s $url | python -c '
import re

for line in __import__("sys").stdin:
    match = re.search(r"const IconData ([a-z0-9_]+)", line)
    if match:
        print("{} = \"{}\"".format(match.group(1).upper(), match.group(1)))
' >> "$output_file"