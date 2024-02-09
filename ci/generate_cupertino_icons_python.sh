url='https://raw.githubusercontent.com/flutter/flutter/stable/packages/flutter/lib/src/cupertino/icons.dart'
output_file="cupertino_icons_python.txt"

curl -s $url | python -c '
import re

for line in __import__("sys").stdin:
    match = re.search(r"const IconData ([a-z0-9_]+)", line)
    if match:
        print("{} = \"cupertino_{}\"".format(match.group(1).upper(), match.group(1)))
' >> "$output_file"