# set PYPI_CLEANUP_PASSWORD with pypi.org password
VER="0\.25\.0\.dev"
#VER="0\.21\.1"
pypi-cleanup -u flet -p flet -y -r $VER --do-it
pypi-cleanup -u flet -p flet-cli -y -r $VER --do-it
pypi-cleanup -u flet -p flet-desktop -y -r $VER --do-it
pypi-cleanup -u flet -p flet-web -y -r $VER --do-it