#!/bin/bash

# Script para ejecutar el optimizador de imágenes
# Autor: Raúl Caro Pastorino

# Obtener la ruta del script actual
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Verificar si existe el entorno virtual, si no, crearlo
if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv "$SCRIPT_DIR/.venv"

    # Activar el entorno virtual
    source "$SCRIPT_DIR/.venv/bin/activate"

    # Instalar dependencias
    echo "Instalando dependencias..."
    pip install --upgrade pip
    pip install -r "$SCRIPT_DIR/requirements.txt"
else
    # Activar el entorno virtual
    source "$SCRIPT_DIR/.venv/bin/activate"
fi

# Ejecutar el script de Python con los argumentos proporcionados
python "$SCRIPT_DIR/image_optimizer.py" "$@"

# Desactivar el entorno virtual
deactivate

exit 0
