import flet as ft
import json
import os

# Nombre del archivo JSON para almacenar los datos
JSON_FILE = "personal_data.json"

# Función para cargar datos desde el archivo JSON
def load_data():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as file:
            return json.load(file)
    return []

# Función para guardar datos en el archivo JSON
def aguardar_datos(data):
    with open(JSON_FILE, "w") as file:
        json.dump(data, file, indent=4)

def main(page: ft.Page):
    data = load_data()