#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para optimizar imágenes de forma recursiva en un directorio.

Este script escanea recursivamente todos los directorios y subdirectorios
para comprimir las imágenes lo máximo posible, manteniendo el nombre y
ubicación original.

Autor: Raúl Caro Pastorino
"""

import os
import sys
import argparse
from pathlib import Path
from PIL import Image
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Formatos de imagen soportados
SUPPORTED_FORMATS = ['webp', 'png', 'jpg', 'jpeg']
SUPPORTED_OUTPUT_FORMATS = ['webp', 'png', 'jpg']

def parse_arguments():
    """
    Parsea los argumentos de línea de comandos.

    Returns:
        argparse.Namespace: Objeto con los argumentos parseados.
    """
    parser = argparse.ArgumentParser(description='Optimiza imágenes de forma recursiva en un directorio.')
    parser.add_argument('directory', type=str, help='Directorio a procesar recursivamente')
    parser.add_argument('-f', '--format', type=str, choices=SUPPORTED_OUTPUT_FORMATS, 
                        help='Formato de salida (webp, png, jpg). Si no se especifica, se mantiene el formato original.')
    parser.add_argument('-w', '--width', type=int, help='Ancho máximo de la imagen. Se mantiene la relación de aspecto.')
    parser.add_argument('-a', '--height', type=int, help='Alto máximo de la imagen. Se mantiene la relación de aspecto.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Muestra información detallada del proceso')

    args = parser.parse_args()

    # Verificar que no se especifiquen tanto ancho como alto
    if args.width and args.height:
        parser.error("No se pueden especificar tanto el ancho (-w) como el alto (-a) a la vez.")

    # Verificar que el directorio existe
    if not os.path.isdir(args.directory):
        parser.error(f"El directorio '{args.directory}' no existe.")

    return args

def get_new_dimensions(image, max_width=None, max_height=None):
    """
    Calcula las nuevas dimensiones de la imagen manteniendo la relación de aspecto.

    Args:
        image (PIL.Image): Imagen a redimensionar.
        max_width (int, optional): Ancho máximo.
        max_height (int, optional): Alto máximo.

    Returns:
        tuple: Nuevas dimensiones (ancho, alto).
    """
    width, height = image.size

    if max_width and width > max_width:
        new_width = max_width
        new_height = int(height * (max_width / width))
        return (new_width, new_height)

    if max_height and height > max_height:
        new_height = max_height
        new_width = int(width * (max_height / height))
        return (new_width, new_height)

    return (width, height)  # Sin cambios

def optimize_image(image_path, output_format=None, max_width=None, max_height=None, verbose=False):
    """
    Optimiza una imagen, cambiando su formato y/o tamaño si es necesario.

    Args:
        image_path (str): Ruta de la imagen a optimizar.
        output_format (str, optional): Formato de salida.
        max_width (int, optional): Ancho máximo.
        max_height (int, optional): Alto máximo.
        verbose (bool, optional): Mostrar información detallada.

    Returns:
        bool: True si la optimización fue exitosa, False en caso contrario.
    """
    try:
        # Abrir la imagen
        image = Image.open(image_path)

        # Determinar el formato de salida
        original_format = image.format.lower() if image.format else 'jpeg'
        target_format = output_format if output_format else original_format

        # Normalizar formato jpg/jpeg
        if target_format.lower() == 'jpg':
            target_format = 'jpeg'

        # Calcular nuevas dimensiones si es necesario
        new_dimensions = get_new_dimensions(image, max_width, max_height)
        resized = new_dimensions != image.size

        if resized:
            image = image.resize(new_dimensions, Image.LANCZOS)

        # Preparar opciones de guardado según el formato
        save_options = {}
        if target_format.lower() == 'jpeg':
            save_options = {'quality': 85, 'optimize': True}
        elif target_format.lower() == 'png':
            save_options = {'optimize': True}
        elif target_format.lower() == 'webp':
            save_options = {'quality': 85, 'method': 6}

        # Guardar la imagen optimizada
        image.save(image_path, format=target_format.upper(), **save_options)

        if verbose:
            logger.info(f"Optimizada: {image_path} - Formato: {target_format.upper()}" + 
                       (f" - Redimensionada a {new_dimensions}" if resized else ""))

        return True
    except Exception as e:
        logger.error(f"Error al optimizar {image_path}: {str(e)}")
        return False

def process_directory(directory, output_format=None, max_width=None, max_height=None, verbose=False):
    """
    Procesa recursivamente un directorio y optimiza todas las imágenes encontradas.

    Args:
        directory (str): Directorio a procesar.
        output_format (str, optional): Formato de salida.
        max_width (int, optional): Ancho máximo.
        max_height (int, optional): Alto máximo.
        verbose (bool, optional): Mostrar información detallada.

    Returns:
        tuple: (total_images, successful_optimizations)
    """
    total_images = 0
    successful_optimizations = 0

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1].lower().replace('.', '')

            # Verificar si es una imagen soportada
            if file_extension in SUPPORTED_FORMATS:
                total_images += 1
                if optimize_image(file_path, output_format, max_width, max_height, verbose):
                    successful_optimizations += 1

    return total_images, successful_optimizations

def main():
    """Función principal del script."""
    args = parse_arguments()

    if args.verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)

    logger.info(f"Iniciando optimización de imágenes en: {args.directory}")
    logger.info(f"Formato de salida: {args.format if args.format else 'Original'}")
    if args.width:
        logger.info(f"Ancho máximo: {args.width}px")
    if args.height:
        logger.info(f"Alto máximo: {args.height}px")

    total, successful = process_directory(
        args.directory, 
        args.format, 
        args.width, 
        args.height,
        args.verbose
    )

    logger.info(f"Proceso completado. Imágenes procesadas: {successful}/{total}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
