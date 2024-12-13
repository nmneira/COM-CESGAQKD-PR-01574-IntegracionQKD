#!/bin/bash

# Ruta del archivo que contiene las claves
QKD_FILE="/mnt/c/Users/nmneira/OneDrive - gradiant.org/Backup/Desktop/qkd/gu-a-cerberis-xgr-qkd/scripts/wsl/claves_qkd.txt"

#Leer la primera línea del archivo (clave) y almacenarla en una variable
KEY=$(head -n 1 "$QKD_FILE")

# Actualizar el archivo ipsecrets.conf
echo "%any : PSK \"$KEY\"" > /etc/ipsec.secrets