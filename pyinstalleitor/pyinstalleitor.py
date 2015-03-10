#-*- coding: utf-8 -*-
'''
Created on 15/02/2012

Crea un entorno gráfico para hacer ejecutables de programas python con pyinstaller
'''

from easygui import *
import sys
import os
import shutil

PYINSTALLER_PATH = diropenbox('Selecciona la carpeta donde está Pyinstaller')
# Si el usuario cancela --> None
if PYINSTALLER_PATH == None:
    sys.exit()

ruta_app = fileopenbox('Selecciona el archivo principal de la aplicación')
RUTA_APLICACION, NOMBRE_APLICACION = os.path.split(ruta_app)

PYTHON_PATH = diropenbox('Selecciona la carpeta donde está Python (Cancelar si está en el path')
if PYTHON_PATH:
    PYTHON_PATH = os.path.join(PYTHON_PATH, 'python')
else:
    PYTHON_PATH = 'python'

# Cambiar al directorio de la aplicación
os.chdir(RUTA_APLICACION)

# 0. Ejecutar Configure.py
# Ejecutar llamadas al sistema
os.system(PYTHON_PATH + ' ' + os.path.join(PYINSTALLER_PATH, 'Configure.py'))

# 1. Crear spec (Makespec.py)
os.system(PYTHON_PATH + ' ' + os.path.join(PYINSTALLER_PATH, 'Makespec.py') + ' ' + NOMBRE_APLICACION)

# 2- Construir ejecutable: Build.py
nombre_spec = os.path.splitext(NOMBRE_APLICACION)[0] + '.spec'
os.system(PYTHON_PATH + ' ' + os.path.join(PYINSTALLER_PATH, 'Build.py') + ' ' + nombre_spec)

shutil.copytree(os.path.join(RUTA_APLICACION, 'data'), os.path.join('dist', os.path.splitext(NOMBRE_APLICACION)[0], 'data'))