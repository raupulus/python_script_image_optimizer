# Optimizador de Imágenes

Este script de Python está diseñado para optimizar imágenes de forma recursiva en un directorio, comprimiendo las imágenes lo máximo posible mientras mantiene su nombre y ubicación original.

## Características

- Escaneo recursivo de directorios y subdirectorios
- Compresión de imágenes para reducir su tamaño
- Conversión opcional de formato (webp, png, jpg)
- Redimensionamiento opcional manteniendo la relación de aspecto
- Procesamiento por lotes de múltiples imágenes

## Requisitos

- Python 3.x
- Pillow (PIL Fork)

## Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/raupulus/python_script_image_optimizer.git
cd python_script_image_optimizer
```

2. Ejecuta el script `run_optimizer.sh` que creará automáticamente un entorno virtual e instalará las dependencias necesarias:

```bash
chmod +x run_optimizer.sh
./run_optimizer.sh -h
```

## Uso

El script se puede ejecutar directamente usando el script bash proporcionado:

```bash
./run_optimizer.sh [directorio] [opciones]
```

### Opciones disponibles:

- `-f, --format`: Formato de salida (webp, png, jpg). Si no se especifica, se mantiene el formato original.
- `-w, --width`: Ancho máximo de la imagen. Se mantiene la relación de aspecto.
- `-a, --height`: Alto máximo de la imagen. Se mantiene la relación de aspecto.
- `-v, --verbose`: Muestra información detallada del proceso.

### Ejemplos de uso:

1. Optimizar todas las imágenes en un directorio manteniendo su formato original:

```bash
./run_optimizer.sh ~/Imágenes/
```

2. Convertir todas las imágenes a formato WebP:

```bash
./run_optimizer.sh ~/Imágenes/ -f webp
```

3. Redimensionar todas las imágenes para que tengan un ancho máximo de 1200px:

```bash
./run_optimizer.sh ~/Imágenes/ -w 1200
```

4. Convertir a PNG y establecer una altura máxima de 800px:

```bash
./run_optimizer.sh ~/Imágenes/ -f png -a 800
```

5. Mostrar información detallada durante el proceso:

```bash
./run_optimizer.sh ~/Imágenes/ -v
```

## Cómo funciona

1. El script recorre recursivamente el directorio especificado buscando archivos de imagen.
2. Para cada imagen encontrada:
   - La carga utilizando la biblioteca Pillow
   - Aplica la conversión de formato si se especificó
   - Redimensiona la imagen si se especificó un ancho o alto máximo
   - Guarda la imagen optimizada en la misma ubicación, sobrescribiendo el archivo original

## Entorno Virtual

El script `run_optimizer.sh` gestiona automáticamente el entorno virtual:

1. Verifica si existe un entorno virtual en la carpeta `.venv`
2. Si no existe, lo crea e instala las dependencias necesarias
3. Activa el entorno virtual antes de ejecutar el script
4. Desactiva el entorno virtual al finalizar

Si prefieres gestionar manualmente el entorno virtual:

```bash
# Crear entorno virtual
python3 -m venv .venv

# Activar entorno virtual
source .venv/bin/activate  # En Linux/Mac
# o
.venv\Scripts\activate     # En Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el script
python image_optimizer.py [directorio] [opciones]

# Desactivar entorno virtual cuando termines
deactivate
```

## Notas importantes

- El script sobrescribe los archivos originales, por lo que es recomendable hacer una copia de seguridad antes de ejecutarlo.
- No se pueden especificar tanto el ancho como el alto a la vez, ya que esto podría distorsionar la imagen.
- Solo se procesan los formatos de imagen soportados: webp, png, jpg, jpeg.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## Autor

Raúl Caro Pastorino
