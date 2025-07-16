#!/bin/bash

set -e

echo "=== Mise à jour du système ==="
sudo apt-get update -y && sudo apt-get upgrade -y

echo "=== Installation de Python3 et pip si nécessaire ==="
sudo apt-get install -y python3 python3-venv python3-pip

echo "=== Création de l'environnement virtuel ==="
python3 -m venv venv

echo "=== Activation de l'environnement virtuel ==="
source venv/bin/activate

echo "=== Installation des dépendances Python ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Setup terminé ==="
