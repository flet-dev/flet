url='https://raw.githubusercontent.com/flutter/flutter/stable/packages/flutter/lib/src/material/icons.dart'
output_file="material-icons.txt"

echo "Map<String, IconData> materialIcons = {" > "$output_file"

curl -s $url | python -c '
import re

for line in __import__("sys").stdin:
    match = re.search(r"const IconData ([a-z0-9_]+)", line)
    if match:
        print("\"{}\": Icons.{}, ".format(match.group(1), match.group(1)))
' >> "$output_file"

echo "};" >> "$output_file"