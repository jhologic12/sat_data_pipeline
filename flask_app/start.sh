#!/bin/bash
PROJECT_ROOT="$(dirname "$0")/.."
echo " Ejecutando verificación de entorno..."
py "$PROJECT_ROOT/flask_app/utils/verify_env.py"
if [ $? -ne 0 ]; then
  echo " Verificación fallida. Revisa tu configuración antes de continuar."
  exit 1
fi

echo " Iniciando aplicación Flask..."
py "$PROJECT_ROOT/flask_app/app.py"