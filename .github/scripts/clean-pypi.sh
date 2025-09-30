# set PYPI_CLEANUP_PASSWORD with pypi.org password

VER="0\.70\.0\.dev(?!5399)"
uv tool install pypi-cleanup
uvx pypi-cleanup -u flet -p flet -y -r $VER --do-it
uvx pypi-cleanup -u flet -p flet-cli -y -r $VER --do-it
uvx pypi-cleanup -u flet -p flet-desktop -y -r $VER --do-it
uvx pypi-cleanup -u flet -p flet-desktop-light -y -r $VER --do-it
uvx pypi-cleanup -u flet -p flet-web -y -r $VER --do-it
