# set PYPI_CLEANUP_PASSWORD with pypi.org password
VER="0.19.0.dev"
pypi-cleanup -u flet -p flet -y -r $VER --do-it
pypi-cleanup -u flet -p flet-core -y -r $VER --do-it
pypi-cleanup -u flet -p flet-runtime -y -r $VER --do-it
pypi-cleanup -u flet -p flet-embed -y -r $VER --do-it
pypi-cleanup -u flet -p flet-fastapi -y -r $VER --do-it
pypi-cleanup -u flet -p flet-pyodide -y -r $VER --do-it