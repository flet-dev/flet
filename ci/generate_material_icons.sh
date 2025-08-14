url='https://raw.githubusercontent.com/flutter/flutter/refs/heads/stable/packages/flutter/lib/src/material/icons.dart'
output_file="sdk/python/packages/flet/src/flet/controls/material/icons_generated.py"
class_name="Icons"
set_id="1"

uv run --with requests ci/generate_icons.py $url $output_file $class_name $set_id
