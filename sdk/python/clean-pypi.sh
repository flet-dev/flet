# set PYPI_CLEANUP_PASSWORD with pypi.org password
#VER="0\.22\.0\.dev"
#VER="0\.21\.1"
pypi-cleanup -u flet -p flet -y -r $VER --do-it
pypi-cleanup -u flet -p flet-core -y -r $VER --do-it
pypi-cleanup -u flet -p flet-runtime -y -r $VER --do-it
pypi-cleanup -u flet -p flet-embed -y -r $VER --do-it
pypi-cleanup -u flet -p flet-pyodide -y -r $VER --do-it