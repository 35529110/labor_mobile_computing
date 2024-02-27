#!/bin/bash

# Definiert das Zielverzeichnis auf dem Server
TARGET_DIR="/var/www/html/"

# Geht von Laborverzeichnis aus
LAB_DIR="."

# Findet alle HTML-Dateien im Laborverzeichnis und dessen Unterverzeichnissen
# und kopiert sie in das Zielverzeichnis auf dem Server
find $LAB_DIR -type f -name "*.html" -exec scp {} root@granelts.de:$TARGET_DIR \;

echo "Alle HTML-Dateien wurden hochgeladen."
