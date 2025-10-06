#!/bin/bash

PYTHON_CMD="python3"
command -v $PYTHON_CMD >/dev/null 2>&1 || PYTHON_CMD="py"

echo " Ejecutando verificación de entorno..."
$PYTHON_CMD "/app/flask_app/utils/verify_env.py"
if [ $? -ne 0 ]; then
  echo " Verificación fallida. Revisa tu configuración antes de continuar."
  exit 1
fi

echo " Cargando variables de entorno desde .env..."
set -a
source .env
set +a

if [[ -z "$EARTHDATA_USERNAME" || -z "$EARTHDATA_PASSWORD" ]]; then
  echo " Credenciales Earthdata no definidas en .env"
  exit 1
fi

echo " Iniciando aplicación Flask..."
$PYTHON_CMD "/app/flask_app/app.py"
