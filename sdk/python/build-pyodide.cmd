cd packages\flet-core
poetry build
cd ..\..

cd packages\flet-pyodide
poetry build
cd ..\..

copy packages\flet-core\dist\*.whl ..\..\client\build\web\python
copy packages\flet-pyodide\dist\*.whl ..\..\client\build\web\python