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

def actualizar_lista():
        employee_list.controls.clear()
        for emp in data:
            employee_list.controls.append(
                ft.Row(
                    controls=[
                        ft.Text(emp["id"]),
                        ft.Text(emp["name"]),
                        ft.Text(emp["position"]),
                        ft.Text(emp["salary"]),
                        ft.Text(emp["nit"]),
                        ft.IconButton(ft.icons.EDIT, on_click=lambda e, emp=emp: edit_employee(emp)),
                        ft.IconButton(ft.icons.DELETE, on_click=lambda e, emp=emp: delete_employee(emp))
                    ]
                )
            )
        page.update()

    def edit_employee(emp):
        name_field.value = emp["name"]
        position_field.value = emp["position"]
        salary_field.value = emp["salary"][1:]  # Eliminar "Q" antes de mostrar el salario
        nit_field.value = emp["nit"]
        save_button.visible = True
        add_button.visible = False
        page.update()
        save_button.on_click = lambda e, emp=emp: save_edit(emp)

    def save_edit(emp):
        emp["name"] = name_field.value
        emp["position"] = position_field.value
        emp["salary"] = "Q" + salary_field.value  # Agregar "Q" al salario
        emp["nit"] = nit_field.value
        aguardar_datos(data)
        actualizar_lista()
        name_field.value = ""
        position_field.value = ""
        salary_field.value = ""
        nit_field.value = ""
        save_button.visible = False
        add_button.visible = True
        page.update()

    def delete_employee(emp):
        data.remove(emp)
        aguardar_datos(data)
        actualizar_lista()

    def show_json(e):
        json_output.value = json.dumps(data, indent=4)
        page.update()

    page.title = "Gestión de Personal"

    name_field = ft.TextField(label="Nombre")
    position_field = ft.TextField(label="Posición")
    salary_field = ft.TextField(label="Salario")
    nit_field = ft.TextField(label="NIT")

    nit_error = ft.Text("Ingresa tu número de NIT",color="Green")
    salary_error = ft.Text("Ingresa el salario en números", color="Green")
