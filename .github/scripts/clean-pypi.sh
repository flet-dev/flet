# set PYPI_CLEANUP_PASSWORD with pypi.org password

VER="0\.70\.0\.dev(?!6907)"
uv tool install pypi-cleanup
uvx pypi-cleanup -u flet -p flet -y -r $VER --do-it
uvx pypi-cleanup -u flet -p flet-cli -y -r $VER --do-it
uvx pypi-cleanup -u flet -p flet-desktop -y -r $VER --do-it
uvx pypi-cleanup -u flet -p flet-desktop-light -y -r $VER --do-it
uvx pypi-cleanup -u flet -p flet-web -y -r $VER --do-it

# modules
uvx pypi-cleanup -u flet -p flet-ads -y -r $VER --do-it
uvx pypi-cleanup -u flet -p flet-audio -y -r $VER --do-it
uvx pypi-cleanup -u flet -p flet-audio-recorder -y -r $VER --do-it
uvx pypi-cleanup -u flet -p flet-charts -y -r $VER --do-it
uvx pypi-cleanup -u flet -p flet-datatable2 -y -r $VER --do-it
uvx pypi-cleanup -u flet -p flet-flashlight -y -r $VER --do-it
uvx pypi-cleanup -u flet -p flet-geolocator -y -r $VER --do-it
uvx pypi-cleanup -u flet -p flet-lottie -y -r $VER --do-it
uvx pypi-cleanup -u flet -p flet-map -y -r $VER --do-it
uvx pypi-cleanup -u flet -p flet-permission-handler -y -r $VER --do-it
uvx pypi-cleanup -u flet -p flet-rive -y -r $VER --do-it
uvx pypi-cleanup -u flet -p flet-video -y -r $VER --do-it
uvx pypi-cleanup -u flet -p flet-webview -y -r $VER --do-it
