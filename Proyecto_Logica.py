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
def validar_numeros(valor, campo):
        if not valor.isdigit():
            return f"⚠ Ingresa solo números en {campo}"
        return None

    def validar_flotante(valor, campo):
        try:
            float(valor)
            return None
        except ValueError:
            return f"⚠ Ingresa un número válido en {campo}"

    def agregar_empleado(e):
        # Limpiar mensajes de error
        nit_error.value = ""
        salary_error.value = ""
        
        # Verificar si los campos no están vacíos y si contienen solo números
        errores = []
        if name_field.value.strip() and position_field.value.strip() and salary_field.value.strip() and nit_field.value.strip():
            nit_error_msg = validar_numeros(nit_field.value, "NIT")
            salary_error_msg = validar_flotante(salary_field.value.replace(',', ''), "Salario")

            if nit_error_msg:
                nit_error.value = nit_error_msg
                errores.append(nit_error_msg)
            if salary_error_msg:
                salary_error.value = salary_error_msg
                errores.append(salary_error_msg)

            if errores:
                message_text.value = "⚠ Corrige los errores e intenta de nuevo"
                message_text.color = "red"
                page.update()
                return
            
            # Verificar si el NIT ya existe
            for emp in data:
                if emp["nit"] == nit_field.value:
                    message_text.value = "⚠ Este empleado ya ha sido registrado"
                    message_text.color = "red"  # Color rojo para mensaje de error
                    page.update()
                    return

            nuevo_empleado = {
                "id": str(len(data) + 1),
                "name": name_field.value,
                "position": position_field.value,
                "salary": "Q" + salary_field.value,  # Agregar "Q" al salario
                "nit": nit_field.value
            }
            data.append(nuevo_empleado)
            aguardar_datos(data)
            actualizar_lista()
            name_field.value = ""
            position_field.value = ""
            salary_field.value = ""
            nit_field.value = ""
            name_field.focus()
            message_text.value = "Empleado añadido exitosamente"
            message_text.color = "green"  # Color verde para mensaje de éxito
            page.update()  # Actualizar la página para que se muestre el mensaje
        else:
            message_text.value = "⚠ No puedes agregar campos vacíos"
            message_text.color = "yellow"  # Color amarillo para mensaje de error
            page.update()  # Actualizar la página para que se muestre el mensaje
