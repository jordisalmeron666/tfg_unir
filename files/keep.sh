#!/bin/bash
# Añade un archivo .gitkeep en todos los subfolders del directorio actual

find . -type d -exec touch {}/.gitkeep \;
echo "Archivos .gitkeep añadidos en todos los subfolders del directorio actual"