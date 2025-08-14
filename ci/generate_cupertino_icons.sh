url='https://raw.githubusercontent.com/flutter/flutter/refs/heads/stable/packages/flutter/lib/src/cupertino/icons.dart'
output_file="sdk/python/packages/flet/src/flet/controls/cupertino/cupertino_icons_generated.py"
set_id="2"

uv run --with requests ci/generate_icons.py $url $output_file $set_id
